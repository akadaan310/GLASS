package org.glass.unison;

import android.app.Activity;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import java.util.ArrayList;

/** ONLY the installed on-device speech service may be used.
 * Never fall back to the network speech recognizer. No spoken text is sent
 * to the GLASS event publisher. This is a separate mode from PCM AudioRecord:
 * the two capture clients must not compete for the microphone.
 */
public final class OfflineRecognizer implements RecognitionListener {
    public interface Listener {
        void status(String label);
        void energy(double proxy);
        void language(String language,double hint);
        void localResult(String transcript,String detected,double hint);
    }
    private final Activity activity;
    private final Listener listener;
    private final Handler handler=new Handler(Looper.getMainLooper());
    private SpeechRecognizer recognizer;
    private boolean running=false;
    private String latestLanguage="unknown";
    private double latestHint=0;

    public OfflineRecognizer(Activity activity,Listener listener){
        this.activity=activity;this.listener=listener;
    }
    public boolean supported(){
        return Build.VERSION.SDK_INT>=31 && SpeechRecognizer.isOnDeviceRecognitionAvailable(activity);
    }
    public void start(){
        if(!supported())throw new UnsupportedOperationException(
            "No installed on-device speech service; returning to local PCM mode");
        stop();
        running=true;
        latestLanguage="unknown";latestHint=0;
        recognizer=SpeechRecognizer.createOnDeviceSpeechRecognizer(activity);
        recognizer.setRecognitionListener(this);
        begin();
    }
    private void begin(){
        if(!running||recognizer==null)return;
        Intent intent=new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS,true);
        intent.putExtra(RecognizerIntent.EXTRA_PREFER_OFFLINE,true); // advisory only; factory enforces on-device
        intent.putExtra(RecognizerIntent.EXTRA_MAX_RESULTS,1);
        if(Build.VERSION.SDK_INT>=34){
            intent.putExtra(RecognizerIntent.EXTRA_ENABLE_LANGUAGE_DETECTION,true);
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_DETECTION_ALLOWED_LANGUAGES,
                new ArrayList<>(java.util.Arrays.asList("ar-SA","en-US")));
            intent.putExtra(RecognizerIntent.EXTRA_ENABLE_LANGUAGE_SWITCH,
                RecognizerIntent.LANGUAGE_SWITCH_BALANCED);
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_SWITCH_ALLOWED_LANGUAGES,
                new ArrayList<>(java.util.Arrays.asList("ar-SA","en-US")));
        }
        try{
            recognizer.startListening(intent);
            listener.status("OFFLINE LANGUAGE SERVICE / listening");
        }catch(RuntimeException e){
            stop();listener.status("On-device recognition not supported for selected languages");
        }
    }
    public void stop(){
        running=false;handler.removeCallbacksAndMessages(null);
        if(recognizer!=null){
            try{recognizer.cancel();}catch(Exception ignored){}
            recognizer.destroy();recognizer=null;
        }
    }
    public boolean isRunning(){return running;}
    @Override public void onReadyForSpeech(Bundle params) {listener.status("ON-DEVICE ASR READY");}
    @Override public void onBeginningOfSpeech() {listener.status("ON-DEVICE SPEECH");}
    @Override public void onRmsChanged(float rmsdB) {
        // OS dB scalar is a visualization hint, not raw PCM RMS.
        listener.energy(Math.max(0,Math.min(1,(rmsdB+2)/15.0)));
    }
    @Override public void onBufferReceived(byte[] buffer) {/* no buffer is stored */}
    @Override public void onEndOfSpeech() {listener.status("PHRASE ENDED / local decoding");}
    @Override public void onError(int error){
        if(!running)return;
        listener.status("Offline recognizer status "+error+" / no text sent");
        // No endless retry on missing languages/microphone/model: user can select PCM.
        if(error==SpeechRecognizer.ERROR_LANGUAGE_NOT_SUPPORTED ||
           error==SpeechRecognizer.ERROR_LANGUAGE_UNAVAILABLE ||
           error==SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS ||
           error==SpeechRecognizer.ERROR_CLIENT ||
           error==SpeechRecognizer.ERROR_SERVER){
            stop();
        }else handler.postDelayed(this::begin,450);
    }
    private void emit(Bundle bundle,boolean finalResult) {
        ArrayList<String> alternatives=bundle==null?null:bundle.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
        if(finalResult){
            String text=alternatives!=null&&!alternatives.isEmpty()?alternatives.get(0):"";
            listener.localResult(text,latestLanguage,latestHint);
        }
    }
    @Override public void onResults(Bundle results){
        if(!running)return;
        emit(results,true);
        handler.postDelayed(this::begin,500);
    }
    @Override public void onPartialResults(Bundle partialResults){
        // Deliberately keep partial hypotheses local, off the network.
    }
    @Override public void onEvent(int eventType,Bundle params){}
    @Override public void onLanguageDetection(Bundle results){
        if(Build.VERSION.SDK_INT<34||results==null)return;
        String locale=results.getString(SpeechRecognizer.DETECTED_LANGUAGE,"");
        int level=results.getInt(SpeechRecognizer.LANGUAGE_DETECTION_CONFIDENCE_LEVEL,0);
        String code=locale.startsWith("ar")?"ar":locale.startsWith("en")?"en":"unknown";
        latestLanguage=code;
        // Android defines categorical confidence. Mapping to 0..0.9 is ONLY a UI hint.
        latestHint=code.equals("unknown")?0:Math.max(0.35,Math.min(.90,.35+.15*level));
        listener.language(latestLanguage,latestHint);
    }
};
