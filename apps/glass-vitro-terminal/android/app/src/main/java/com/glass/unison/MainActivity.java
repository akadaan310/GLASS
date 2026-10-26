package com.glass.unison;

import android.app.Activity;
import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.View;
import android.view.inputmethod.EditorInfo;
import android.view.inputmethod.InputMethodManager;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.text.InputType;
import android.text.TextWatcher;
import android.text.Editable;
import java.nio.charset.StandardCharsets;
import java.nio.ByteBuffer;
import java.nio.CharBuffer;
import java.nio.charset.CharsetDecoder;
import java.nio.charset.CodingErrorAction;



/** The visible GLASS world is drawn by the native pixel engine; no web view. */
public final class MainActivity extends Activity {
    static { System.loadLibrary("unison_bridge"); }
    private native long nativeCreate(String journal);
    private native void nativeRelease(long pointer);
    private native String nativeDispatch(long pointer, String input);
    private native String nativeStatus(long pointer);
    private native void nativeRaster(long pointer, int[] pixels, int width, int height, long phase);
    private native long nativeShellOpen(String cwd);
    private native byte[] nativeShellRead(long handle);
    private native void nativeShellWrite(long handle, byte[] data);
    private native void nativeShellResize(long handle, int cols, int rows);
    private native void nativeShellStop(long handle);
    private native void nativeShellDispose(long handle);

    private long engine;
    private FrameLayout root;
    private NativeWorld world;
    private EditText keyboard;
    private ShellPane terminalView;
    private volatile long shellHandle=0;
    private long paintCounter = 0;
    private boolean showingShell = false;

    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.rgb(0,7,17));
        getWindow().setNavigationBarColor(Color.rgb(0,7,17));
        getWindow().getDecorView().setSystemUiVisibility(5894 | 1024 | 512);
        engine = nativeCreate(getFilesDir().getAbsolutePath()+"/vitromaton.jsonl");
        root = new FrameLayout(this);
        world = new NativeWorld(this);
        root.addView(world, new FrameLayout.LayoutParams(-1, -1));
        keyboard = new EditText(this);
        keyboard.setSingleLine(true);
        keyboard.setContentDescription("GLASS Unison programmable command input");
        keyboard.setInputType(InputType.TYPE_CLASS_TEXT|InputType.TYPE_TEXT_FLAG_NO_SUGGESTIONS|InputType.TYPE_TEXT_VARIATION_VISIBLE_PASSWORD);
        keyboard.setImeOptions(EditorInfo.IME_ACTION_GO|EditorInfo.IME_FLAG_NO_EXTRACT_UI);
        keyboard.setAlpha(0.01f);
        FrameLayout.LayoutParams p = new FrameLayout.LayoutParams(1,1);
        root.addView(keyboard,p);
        keyboard.addTextChangedListener(new TextWatcher(){
            @Override public void beforeTextChanged(CharSequence s,int a,int c,int d){}
            @Override public void onTextChanged(CharSequence s,int a,int b,int c){world.typing=s.toString();world.invalidate();if(terminalView!=null)terminalView.setPendingInput(s.toString());}
            @Override public void afterTextChanged(Editable e){}
        });
        keyboard.setOnEditorActionListener((TextView v,int action,KeyEvent event)->{
            if(action==EditorInfo.IME_ACTION_GO || (event!=null&&event.getKeyCode()==KeyEvent.KEYCODE_ENTER)){
                String command=keyboard.getText().toString().trim();keyboard.setText("");
                if(showingShell){
                    if(command.equals(":exit")){returnWorld();return true;}
                    if(command.equals(":ctrl-c"))nativeShellWrite(shellHandle,new byte[]{3});
                    else nativeShellWrite(shellHandle,(command+"\n").getBytes(StandardCharsets.UTF_8));
                    return true;
                }
                if(command.equals(":shell")){openShell();return true;}
                if(!command.isEmpty())world.lastResult=nativeDispatch(engine,command);
                world.invalidate();return true;
            }return false;
        });
        setContentView(root);
    }
    private void showKeyboard() {
        keyboard.requestFocus();
        InputMethodManager manager=(InputMethodManager)getSystemService(INPUT_METHOD_SERVICE);
        manager.showSoftInput(keyboard,InputMethodManager.SHOW_IMPLICIT);
    }
    private void openShell() {
        if(showingShell)return;
        final long handle=nativeShellOpen(getFilesDir().getAbsolutePath());
        if(handle==0){world.lastResult="⊣ PTY UNAVAILABLE";world.invalidate();return;}
        shellHandle=handle;showingShell=true;
        terminalView=new ShellPane(this);
        terminalView.setResizeHandler((columns,rows)->nativeShellResize(handle,columns,rows));
        terminalView.setOnClickListener(v->showKeyboard());
        root.addView(terminalView,new FrameLayout.LayoutParams(-1,-1));
        terminalView.append("⟦ GLASS · LOCAL PTY SHELL ⟧\nType commands; keyboard Go sends Enter. :exit returns to UNISON.\n");
        Thread reader=new Thread(()->{
            CharsetDecoder decoder=StandardCharsets.UTF_8.newDecoder()
                .onMalformedInput(CodingErrorAction.REPLACE).onUnmappableCharacter(CodingErrorAction.REPLACE);
            ByteBuffer incoming=ByteBuffer.allocate(16384);
            CharBuffer decoded=CharBuffer.allocate(16384);
            try{
                while(true){
                    byte[] bytes=nativeShellRead(handle);
                    if(bytes==null)break;
                    if(bytes.length==0)continue;
                    incoming.put(bytes);
                    incoming.flip();
                    decoder.decode(incoming,decoded,false);
                    incoming.compact();
                    decoded.flip();
                    String segment=decoded.toString();decoded.clear();
                    runOnUiThread(()->{if(terminalView!=null&&shellHandle==handle)terminalView.append(segment);});
                }
            }finally{
                nativeShellStop(handle);
                runOnUiThread(()->{
                    if(shellHandle==handle){shellHandle=0;returnWorld();}
                    nativeShellDispose(handle);
                });
            }
        },"GLASS-PTY");
        reader.setDaemon(true);reader.start();showKeyboard();
    }
    private void returnWorld(){
        showingShell=false;
        long handle=shellHandle;shellHandle=0;
        if(handle!=0)nativeShellStop(handle);
        if(terminalView!=null){root.removeView(terminalView);terminalView=null;}
        if(world!=null){world.lastResult="۞ SHELL RETURNED · UNISON CONTINUITY";world.invalidate();}
    }
    @Override public void onBackPressed(){if(showingShell){returnWorld();return;}super.onBackPressed();}
    @Override protected void onDestroy(){returnWorld();nativeRelease(engine);engine=0;super.onDestroy();}

    private final class NativeWorld extends View {
        private Bitmap bitmap;
        private int[] pixels;
        private int pixelWidth, pixelHeight;
        private final Paint fg=new Paint(3);
        private final Paint image=new Paint(3);
        private String typing="";
        private String lastResult="◉ ⟦ Λ ⊗ Ω ⊗ Γ ⊗ τ ⊗ Π ⟧ → ۞";
        private final String[] letters={"0","1","Λ","Ω","Γ","τ","Π","⊕","۞","ج","α","λ","◉","⟐"};
        NativeWorld(Context context){super(context);fg.setTypeface(Typeface.create("monospace",Typeface.NORMAL));setFocusable(true);setContentDescription("GLASS immersive terminal. Tap to type. Type colon shell to open terminal.");}
        @Override protected void onDraw(Canvas canvas){
            if(engine==0)return;
            int w=getWidth(),h=getHeight();if(w==0||h==0)return;
            int pw=Math.min(480,Math.max(1,w/2)),ph=Math.min(960,Math.max(1,h/2));
            if(bitmap==null || pixelWidth!=pw||pixelHeight!=ph){
                pixelWidth=pw;pixelHeight=ph;bitmap=Bitmap.createBitmap(pw,ph,Bitmap.Config.ARGB_8888);pixels=new int[pw*ph];
            }
            nativeRaster(engine,pixels,pw,ph,paintCounter++);
            bitmap.setPixels(pixels,0,pw,0,0,pw,ph);
            canvas.drawBitmap(bitmap,null,new android.graphics.Rect(0,0,w,h),image);
            float unit=Math.min(w/38f,h/70f);
            fg.setTextSize(Math.max(13f,unit*1.30f));fg.setColor(Color.rgb(184,250,244));
            canvas.drawText("G L A S S",w*.11f,h*.095f,fg);
            fg.setTextSize(Math.max(10f,unit*.83f));fg.setColor(Color.rgb(118,202,200));
            canvas.drawText("UNISON / VITROMATON / RESEARCH TERMINAL",w*.11f,h*.125f,fg);
            canvas.drawText("⟦جَ⟧  ◉  ⟐ K↔Q  ۞",w*.11f,h*.165f,fg);
            fg.setTextSize(Math.max(12f,unit));
            for(int i=0;i<48;i++){
                float yy=h*(.20f+i*.015f);int ix=(int)((i+paintCounter/4)%letters.length);
                fg.setColor((i%4==0)?Color.rgb(117,246,209):Color.rgb(41,112,117));
                canvas.drawText(letters[ix],Math.max(4,w*.03f),yy,fg);
                canvas.drawText(letters[(ix+7)%letters.length],w*.945f,yy,fg);
            }
            fg.setColor(Color.rgb(159,234,223));fg.setTextSize(Math.max(12f,unit));
            canvas.drawText("Λ   Ω   Γ   τ   Π",w*.23f,h*.31f,fg);
            fg.setTextSize(Math.max(11f,unit*.85f));
            canvas.drawText("AST → IR → RUNTIME → ORACLE",w*.13f,h*.72f,fg);
            drawWrapped(canvas,lastResult,w*.10f,h*.76f,w*.80f,Math.max(13f,unit),4);
            fg.setColor(Color.rgb(214,254,247));fg.setTextSize(Math.max(14f,unit*1.20f));
            drawWrapped(canvas,"⟐ "+typing+(paintCounter%12<6?"▏":" "),w*.10f,h*.92f,w*.80f,Math.max(16f,unit*1.24f),2);
            if(isShown())postInvalidateDelayed(110);
        }
        private void drawWrapped(Canvas canvas,String text,float x,float y,float width,float size,int rows){
            fg.setTextSize(size);int row=0;for(String para:text.split("\\n")){
                String line="";for(String word:para.split(" ")){
                    if(fg.measureText(line+" "+word)>width&&!line.isEmpty()){
                        canvas.drawText(line,x,y+row*size*1.35f,fg);row++;line=word;
                        if(row>=rows)return;
                    }else line+=(line.isEmpty()?"":" ")+word;
                }
                canvas.drawText(line,x,y+row*size*1.35f,fg);row++;if(row>=rows)return;
            }
        }
        @Override public boolean onTouchEvent(MotionEvent e){if(e.getAction()==MotionEvent.ACTION_UP){showKeyboard();performClick();return true;}return true;}
        @Override public boolean performClick(){super.performClick();return true;}
    }
}
