package dev.glass.browser;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.view.KeyEvent;
import android.view.inputmethod.EditorInfo;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import java.io.File;
import org.mozilla.geckoview.GeckoRuntime;
import org.mozilla.geckoview.GeckoSession;
import org.mozilla.geckoview.GeckoView;

/** GLASS shell over Mozilla's independent Gecko HTML/CSS renderer. */
public final class BrowserActivity extends Activity {
 static { System.loadLibrary("glass_native"); }
 private native long record(String path, String type, String value);
 private GeckoRuntime runtime;
 private GeckoSession session;
 private EditText address;
 private String journal;
 private void emit(String event,String value){record(journal,event,value);}
 @Override public void onCreate(Bundle state){
  super.onCreate(state);
  journal=new File(getFilesDir(),"browser-events.jsonl").getAbsolutePath();
  LinearLayout column=new LinearLayout(this);
  column.setOrientation(LinearLayout.VERTICAL);
  column.setBackgroundColor(Color.rgb(8,14,25));
  LinearLayout bar=new LinearLayout(this);
  address=new EditText(this);address.setSingleLine(true);
  address.setTextColor(Color.WHITE);address.setHintTextColor(Color.LTGRAY);
  address.setHint("URL or glass://help");
  bar.addView(address,new LinearLayout.LayoutParams(0,120,1));
  TextView go=new TextView(this);go.setText(" GO ");
  go.setTextColor(Color.WHITE);go.setPadding(12,40,12,20);
  go.setOnClickListener(v->navigate(address.getText().toString()));
  bar.addView(go);column.addView(bar);
  GeckoView view=new GeckoView(this);
  column.addView(view,new LinearLayout.LayoutParams(-1,0,1));
  setContentView(column);
  runtime=GeckoRuntime.create(this);
  session=new GeckoSession();
  session.setContentDelegate(new GeckoSession.ContentDelegate(){});
  session.open(runtime);
  view.setSession(session);
  address.setOnEditorActionListener((v,id,event)->{
   if(id==EditorInfo.IME_ACTION_GO||id==EditorInfo.IME_ACTION_DONE||
      (event!=null&&event.getKeyCode()==KeyEvent.KEYCODE_ENTER)){
     navigate(address.getText().toString());return true;
   }return false;
  });
  emit("browser_launch","gecko");
  session.loadUri("about:blank");
 }
 private void navigate(String input){
  String u=input.trim();
  if(u.isEmpty())return;
  if(u.startsWith("glass://")){
   emit("terminal",u);
   String answer=u.equals("glass://help")?"GLASS Terminal: glass://help glass://trace glass://home":
     u.equals("glass://trace")?"Local event journal: "+journal:
     u.equals("glass://home")?"GLASS / UNISON":"Unknown terminal operator";
   String html="<!doctype html><meta charset='utf-8'><body style='background:#08131f;color:#eee;font:18px monospace;padding:24px'><h1>GLASS / UNISON</h1><pre>"+
     answer.replace("&","&amp;").replace("<","&lt;")+"</pre></body>";
   session.loadData(html,"text/html");
   return;
  }
  if(!u.contains("://"))u=u.contains(".")?"https://"+u:"https://www.google.com/search?q="+android.net.Uri.encode(u);
  if(!(u.startsWith("https://")||u.startsWith("http://")||u.startsWith("about:"))){
    emit("navigation_denied",u);return;
  }
  emit("navigation_request",u);session.loadUri(u);
 }
 @Override protected void onDestroy(){
  emit("browser_close","gecko");
  if(session!=null)session.close();
  super.onDestroy();
 }
}
