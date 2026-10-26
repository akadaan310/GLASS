package org.glass.unison;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.text.InputType;
import android.view.Gravity;
import android.view.View;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import java.util.Locale;
import java.util.UUID;
import java.util.concurrent.atomic.AtomicBoolean;

/** Standalone GLASS listening APK. Starts SILENT and idle.
 * Local microphone PCM gets bounded DSP traces; on-device OS recognition is
 * an alternative capture mode when installed. Never silently uses cloud ASR.
 * Network access is only for explicitly enabled numeric GLASS-LIVE events.
 */
public final class GlassActivity extends Activity {
    private static final int MIC_REQUEST=9101, WAV_REQUEST=9102;
    private final Handler ui=new Handler(Looper.getMainLooper());
    private final AtomicBoolean capturing=new AtomicBoolean(false);
    private TraceMath math;
    private LanguageClock clock;
    private OfflineRecognizer offline;
    private EventPublisher publisher;
    private InkSurface ink;
    private AudioRecord record;
    private Thread captureThread;
    private TextView status, prompt, details, networkStatus;
    private EditText endpoint, room, secret;
    private Button listenButton, recognizeButton, stopButton, streamButton, arButton, enButton, otherButton;
    private boolean streamEnabled=false, paused=true, asrMode=false, importing=false;
    private String asrDetected="unknown";
    private double asrQuality=0;
    private long lastUiNs=0;

    @Override public void onCreate(Bundle savedState){
        super.onCreate(savedState);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        getWindow().setStatusBarColor(Color.rgb(7,12,19));
        getWindow().setNavigationBarColor(Color.rgb(7,12,19));
        math=new TraceMath();clock=new LanguageClock();
        publisher=new EventPublisher(s->runOnUiThread(()->setNetwork(s)));
        offline=new OfflineRecognizer(this,new OfflineRecognizer.Listener(){
            public void status(String text){runOnUiThread(()->setStatus(text));}
            public void energy(double hint){runOnUiThread(()->ink.ingestOsRms(hint));}
            public void language(String detected,double quality){
                asrDetected=detected;asrQuality=quality;
                runOnUiThread(()->ink.setLanguage(detected+" / on-device hint"));
            }
            public void localResult(String recognized,String detected,double quality){
                runOnUiThread(()->{
                    // No user text in the publisher, Android log or web stream.
                    String safeLocal=recognized.length()>100?recognized.substring(0,100)+"…":recognized;
                    setStatus("ON DEVICE • "+(safeLocal.isEmpty()?"No text recognized":safeLocal));
                    LanguageClock.Candidate c=clock.proposeFromOnDevice(detected,quality);
                    showCandidate(c);
                });
            }
        });
        buildUi();
        setStatus("MICROPHONE OFF. Nothing is recording, playing or streaming.");
        setNetwork("NETWORK OFF / authorization required");
    }
    private static String format(double x){return String.format(Locale.ROOT,"%.2f",x);}
    private TextView label(String title,int size,int color){
        TextView t=new TextView(this);t.setText(title);t.setTextSize(size);
        t.setTextColor(color);t.setPadding(dp(2),dp(5),dp(2),dp(5));
        return t;
    }
    private int dp(float x){return (int)(x*getResources().getDisplayMetrics().density+.5f);}
    private Button button(String name){
        Button b=new Button(this);
        b.setText(name);b.setAllCaps(false);b.setTextSize(12);
        b.setMinHeight(dp(40));b.setPadding(dp(5),0,dp(5),0);
        return b;
    }
    private void rowAdd(LinearLayout row,View... children){
        for(View child:children)row.addView(child,new LinearLayout.LayoutParams(0,dp(48),1));
    }
    private void setStatus(String text){
        if(status!=null)status.setText(text);
    }
    private void setNetwork(String text){
        if(networkStatus!=null)networkStatus.setText(text);
    }
    private void buildUi(){
        int bg=Color.rgb(7,12,19),muted=Color.rgb(156,170,187),gold=Color.rgb(229,184,109);
        LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setBackgroundColor(bg);
        root.setPadding(dp(12),dp(10),dp(12),dp(10));
        TextView title=label("GLASS  ·  UNISON LIVE",19,gold);
        root.addView(title);
        root.addView(label("MIC LOCAL / NO AUDIO PLAYBACK / EXPLICIT STREAM",10,muted));
        ink=new InkSurface(this);
        root.addView(ink,new LinearLayout.LayoutParams(-1,0,1));
        status=label("",12,Color.WHITE);
        status.setMaxLines(2);
        root.addView(status);
        prompt=label("Choose a listening mode. Language remains UNKNOWN until supported by evidence.",12,gold);
        prompt.setMaxLines(3);root.addView(prompt);
        LinearLayout choices=new LinearLayout(this);
        choices.setOrientation(LinearLayout.HORIZONTAL);
        arButton=button("عربي ✓");enButton=button("English ✓");otherButton=button("Other ✓");
        rowAdd(choices,arButton,enButton,otherButton);
        root.addView(choices);setChoices(false);
        arButton.setOnClickListener(v->confirm("ar"));
        enButton.setOnClickListener(v->confirm("en"));
        otherButton.setOnClickListener(v->confirm("other"));
        LinearLayout actions=new LinearLayout(this);actions.setOrientation(LinearLayout.HORIZONTAL);
        listenButton=button("▶ Listen PCM");
        recognizeButton=button("Offline ASR");
        stopButton=button("■ Stop");
        rowAdd(actions,listenButton,recognizeButton,stopButton);root.addView(actions);
        listenButton.setOnClickListener(v->requestStart(false));
        recognizeButton.setOnClickListener(v->requestStart(true));
        stopButton.setOnClickListener(v->stopAll());
        LinearLayout actions2=new LinearLayout(this);actions2.setOrientation(LinearLayout.HORIZONTAL);
        Button importButton=button("Analyze WAV");
        Button configButton=button("Event stream");
        rowAdd(actions2,importButton,configButton);root.addView(actions2);
        importButton.setOnClickListener(v->openWav());
        configButton.setOnClickListener(v->showNetworkDialog());
        networkStatus=label("",10,muted);networkStatus.setMaxLines(2);root.addView(networkStatus);
        details=label("DSP reports sound envelopes and candidate pauses. Full MUQRI CTC/tajwīd scoring is not installed in this APK.",10,muted);
        details.setMaxLines(3);root.addView(details);
        setContentView(root);
    }
    private void setChoices(boolean visible){
        for(Button b:new Button[]{arButton,enButton,otherButton}){b.setEnabled(visible);b.setAlpha(visible?1f:.35f);}
    }
    private boolean micGranted(){
        return Build.VERSION.SDK_INT<23 || checkSelfPermission(Manifest.permission.RECORD_AUDIO)==PackageManager.PERMISSION_GRANTED;
    }
    private void requestStart(boolean asr){
        if(!micGranted()){
            asrMode=asr;
            requestPermissions(new String[]{Manifest.permission.RECORD_AUDIO},MIC_REQUEST);
            return;
        }
        if(asr)startAsr();else startPcm();
    }
    @Override public void onRequestPermissionsResult(int requestCode,String[] permissions,int[] grants){
        super.onRequestPermissionsResult(requestCode,permissions,grants);
        if(requestCode==MIC_REQUEST){
            if(grants.length>0&&grants[0]==PackageManager.PERMISSION_GRANTED)requestStart(asrMode);
            else setStatus("Microphone permission denied; capture stays OFF.");
        }
    }
    private void startPcm(){
        stopCaptureOnly();asrMode=false;
        int min=AudioRecord.getMinBufferSize(TraceMath.SAMPLE_RATE,
            AudioFormat.CHANNEL_IN_MONO,AudioFormat.ENCODING_PCM_16BIT);
        if(min<=0){setStatus("PCM16 capture unavailable on this device.");return;}
        AudioRecord candidate=null;
        try{
            candidate=new AudioRecord(MediaRecorder.AudioSource.VOICE_RECOGNITION,
                TraceMath.SAMPLE_RATE,AudioFormat.CHANNEL_IN_MONO,
                AudioFormat.ENCODING_PCM_16BIT,Math.max(min,4096));
            if(candidate.getState()!=AudioRecord.STATE_INITIALIZED)
                throw new IllegalStateException("AudioRecord initialization failed");
            record=candidate;capturing.set(true);paused=false;record.startRecording();
            ink.setMode(true);ink.setLanguage("AWAITING YOUR CONFIRMATIONS");
            publisher.state("started");
            setStatus("LOCAL PCM CAPTURE / sound is not saved or played.");
            captureThread=new Thread(this::captureLoop,"glass-local-pcm");
            captureThread.setDaemon(true);captureThread.start();
        }catch(Exception e){
            capturing.set(false);paused=true;
            if(candidate!=null){try{candidate.release();}catch(Exception ignored){}}
            record=null;ink.setMode(false);setStatus("Microphone unavailable: "+e.getClass().getSimpleName());
        }
    }
    private void captureLoop(){
        short[] buffer=new short[1024];AudioRecord input=record;
        while(capturing.get()&&input!=null){
            int n;
            try{n=input.read(buffer,0,buffer.length,AudioRecord.READ_BLOCKING);}
            catch(Exception e){break;}
            if(n<128)continue;
            TraceMath.Frame frame;
            try{frame=math.process(buffer,n);}
            catch(IllegalArgumentException error){continue;}
            ink.ingest(frame);
            publisher.trace(frame);
            LanguageClock.Candidate c=clock.onFrame(frame);
            if(c!=null){
                publisher.proposed(c,clock.threshold(),clock.confirmations());
                ui.post(()->showCandidate(c));
            }
            long now=System.nanoTime();
            if(now-lastUiNs>600_000_000L){
                lastUiNs=now;
                ui.post(()->details.setText(
                    "SOURCE: PCM16 16k · RMS "+format(frame.rms)+" · flux "+format(frame.flux)+
                    " · centroid "+Math.round(frame.centroidHz)+"Hz · language clock "+clock.confirmations()+"/30"));
            }
        }
        ui.post(()->{if(!capturing.get()){ink.setMode(false);}});
    }
    private void startAsr(){
        stopCaptureOnly();asrMode=true;
        if(!offline.supported()){
            setStatus("No installed on-device speech recognizer; no cloud fallback.");
            ink.setMode(false);return;
        }
        try{
            offline.start();paused=false;ink.setMode(true);
            ink.setStatus("ON-DEVICE RECOGNITION / no audio upload");
            publisher.state("started");
        }catch(Exception e){ink.setMode(false);setStatus("Offline recognition unavailable.");}
    }
    private void showCandidate(LanguageClock.Candidate c){
        if(c==null)return;
        String guess=c.language.equals("unknown")?"UNKNOWN":c.language.toUpperCase(Locale.ROOT);
        String label=c.possibleSwitch?"Possible language switch: ":"Phrase language candidate: ";
        prompt.setText(label+guess+" (hint "+format(c.confidence)+", threshold "+
            format(clock.threshold())+"). Confirm: Arabic, English, or Other. "+clock.confirmations()+"/30.");
        setChoices(true);
        ink.setLanguage(guess+" · "+c.reason);
    }
    private void confirm(String language){
        if(clock.pending()==null){setChoices(false);return;}
        clock.confirm(language);
        publisher.confirmed(language,clock.confirmations(),clock.switches(),clock.disagreements());
        setChoices(false);
        prompt.setText("CONFIRMED "+language.toUpperCase(Locale.ROOT)+
            " · "+clock.confirmations()+" examples · "+clock.switches()+" confirmed switches"+
            " · "+clock.disagreements()+" disagreements.");
        ink.setLanguage(language.toUpperCase(Locale.ROOT)+" / confirmed");
    }
    private void stopCaptureOnly(){
        capturing.set(false);
        AudioRecord old=record;record=null;
        if(old!=null){
            try{old.stop();}catch(Exception ignored){}
            // Release after reads have observed capture stop.
            if(captureThread!=null && captureThread!=Thread.currentThread()){
                try{captureThread.join(250);}catch(InterruptedException ignored){Thread.currentThread().interrupt();}
            }
            try{old.release();}catch(Exception ignored){}
        }
        offline.stop();ink.setMode(false);
        paused=true;
    }
    private void stopAll(){
        stopCaptureOnly();
        publisher.state("stopped");
        publisher.disable();streamEnabled=false;
        prompt.setText("Listening stopped; no recording, playback or network publishing.");
        setStatus("MICROPHONE OFF.");setChoices(false);
    }
    private void openWav(){
        stopCaptureOnly();
        Intent pick=new Intent(Intent.ACTION_OPEN_DOCUMENT);
        pick.setType("audio/wav");pick.addCategory(Intent.CATEGORY_OPENABLE);
        startActivityForResult(pick,WAV_REQUEST);
    }
    @Override protected void onActivityResult(int request,int result,Intent data){
        super.onActivityResult(request,result,data);
        if(request==WAV_REQUEST&&result==RESULT_OK&&data!=null&&data.getData()!=null){
            setStatus("Read-only WAV import; sound is NOT played.");
            importing=true;
            new Thread(()->{
                try{
                    int count=WavImport.analyze(getContentResolver(),data.getData(),math,f->{
                        ink.ingest(f);publisher.trace(f);
                        LanguageClock.Candidate c=clock.onFrame(f);
                        if(c!=null){publisher.proposed(c,clock.threshold(),clock.confirmations());
                            ui.post(()->showCandidate(c));}
                    });
                    runOnUiThread(()->setStatus("WAV analyzed locally: "+count+" frames. Never played."));
                }catch(Exception e){runOnUiThread(()->setStatus("WAV not supported: "+e.getMessage()));}
                finally{importing=false;}
            },"glass-wav-import").start();
        }
    }
    private void showNetworkDialog(){
        LinearLayout fields=new LinearLayout(this);fields.setOrientation(LinearLayout.VERTICAL);
        fields.setPadding(dp(12),dp(8),dp(12),dp(8));
        endpoint=new EditText(this);endpoint.setSingleLine(true);
        endpoint.setHint("https://your-project.vercel.app/api/glass/publish");
        room=new EditText(this);room.setSingleLine(true);
        room.setText("glass_"+UUID.randomUUID().toString().replace("-","").substring(0,12));
        secret=new EditText(this);secret.setSingleLine(true);
        secret.setInputType(InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_VARIATION_PASSWORD);
        secret.setHint("GLASS_STREAM_WRITE_KEY (private)");
        fields.addView(label("HTTPS event ingestion URL",12,Color.BLACK));fields.addView(endpoint);
        fields.addView(label("Private room ID",12,Color.BLACK));fields.addView(room);
        fields.addView(label("Write capability (not stored)",12,Color.BLACK));fields.addView(secret);
        AlertDialog alert=new AlertDialog.Builder(this)
          .setTitle("Stream derived I/O? Never raw audio.")
          .setView(fields)
          .setPositiveButton("Enable HTTPS stream",(dialog,which)->{
            try{
                publisher.configure(endpoint.getText().toString().trim(),
                    secret.getText().toString(),room.getText().toString().trim());
                streamEnabled=true;setStatus("Protected numeric event stream ON. No voice uploaded.");
            }catch(Exception e){setNetwork("Stream refused: "+e.getMessage());}
            secret.setText("");
          })
          .setNegativeButton("Disable stream",(dialog,which)->{
            publisher.disable();streamEnabled=false;
          })
          .create();
        alert.show();
    }
    @Override protected void onPause(){
        super.onPause();
        stopAll(); // Mic and network stop on background, without ambiguity.
    }
    @Override protected void onDestroy(){
        stopAll();publisher.close();super.onDestroy();
    }
}
