package org.glass.nativebrowser;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Intent;
import android.content.Context;
import android.media.projection.MediaProjectionConfig;
import android.media.projection.MediaProjectionManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.graphics.Color;
import android.view.View;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.CookieManager;
import android.webkit.WebStorage;
import android.widget.LinearLayout;
import android.widget.EditText;
import android.widget.Button;
import android.widget.TextView;

/** Browser shell: app-origin logging; explicit user authorization for whole-screen capture. */
public class BrowserActivity extends Activity {
  private static final int CAPTURE_REQUEST=4901;
  private boolean privateProfile;
  private WebView page;
  private EditText address;
  private TextView status;
  private Button captureButton;
  private int dp(int x){return (int)(x*getResources().getDisplayMetrics().density+0.5f);}
  private Button button(String label){Button b=new Button(this);b.setText(label);b.setAllCaps(false);b.setTextColor(0xffc8fff3);b.setBackgroundTintList(android.content.res.ColorStateList.valueOf(0xff16443c));return b;}
  private static String origin(String value){
    try{Uri u=Uri.parse(value);String h=u.getHost();String s=u.getScheme();return s!=null&&h!=null?s+"://"+h:"local-or-unknown";}
    catch(Exception e){return "invalid-url";}
  }
  @Override public void onCreate(Bundle b){super.onCreate(b);
    privateProfile=getClass().getName().endsWith("PrivateActivity");
    if(privateProfile){CookieManager.getInstance().removeAllCookies(null);WebStorage.getInstance().deleteAllData();}
    LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(dp(8),dp(5),dp(8),dp(3));root.setBackgroundColor(0xff07111c);
    TextView brand=new TextView(this);brand.setText(privateProfile?"GLASS · ISOLATED PRIVATE":"GLASS · NATIVE BROWSER");brand.setTextColor(0xffa8fbe2);brand.setTextSize(17);root.addView(brand);
    status=new TextView(this);status.setText("Capture OFF · browser events local-only");status.setTextColor(0xff90adbd);status.setTextSize(12);root.addView(status);
    LinearLayout nav=new LinearLayout(this);nav.setOrientation(LinearLayout.HORIZONTAL);
    address=new EditText(this);address.setSingleLine(true);address.setHint("https://... or glass://terminal/v1/state");address.setTextColor(Color.WHITE);address.setHintTextColor(0xff7897a0);address.setTextSize(12);
    nav.addView(address,new LinearLayout.LayoutParams(0,dp(48),1));Button go=button("Go");nav.addView(go);root.addView(nav);
    LinearLayout commands=new LinearLayout(this);commands.setOrientation(LinearLayout.HORIZONTAL);
    captureButton=button("Start screen continuity");commands.addView(captureButton,new LinearLayout.LayoutParams(0,dp(49),2));
    Button stop=button("Stop");commands.addView(stop,new LinearLayout.LayoutParams(0,dp(49),1));
    Button isolate=button("Private");if(!privateProfile)commands.addView(isolate,new LinearLayout.LayoutParams(0,dp(49),1));root.addView(commands);
    page=new WebView(this);WebSettings ws=page.getSettings();ws.setJavaScriptEnabled(true);ws.setDomStorageEnabled(true);
    ws.setAllowFileAccess(false);ws.setAllowContentAccess(false);ws.setJavaScriptCanOpenWindowsAutomatically(false);ws.setSupportMultipleWindows(false);
    ws.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
    page.setWebViewClient(new WebViewClient(){
      @Override public boolean shouldOverrideUrlLoading(WebView view,WebResourceRequest request){Uri u=request.getUrl();String scheme=u.getScheme();
        if(!"https".equalsIgnoreCase(scheme)) {if(!privateProfile)Journal.event(BrowserActivity.this,"BLOCKED_LINK","browser",origin(u.toString()));return true;}return false;}
      @Override public void onPageStarted(WebView view,String url,android.graphics.Bitmap favicon){
        if(!privateProfile)Journal.event(BrowserActivity.this,"NAVIGATION","browser",origin(url));
        status.setText("Browser: "+origin(url)+" · "+(CaptureService.active?"capture ON":"capture OFF"));}
    });
    root.addView(page,new LinearLayout.LayoutParams(-1,0,1));setContentView(root);
    go.setOnClickListener(v->navigate(address.getText().toString()));
    captureButton.setOnClickListener(v->{if(privateProfile)status.setText("Capture consent is controlled by the main GLASS window");else requestCapture();});
    stop.setOnClickListener(v->{stopService(new Intent(this,CaptureService.class).setAction(CaptureService.ACTION_STOP));status.setText("Stopping capture; gaps retained");});
    isolate.setOnClickListener(v->startActivity(new Intent(this,PrivateActivity.class)));
    if(!privateProfile&&!getPreferences(MODE_PRIVATE).getBoolean("intro_seen",false)){
      getPreferences(MODE_PRIVATE).edit().putBoolean("intro_seen",true).apply();
      new AlertDialog.Builder(this).setTitle("GLASS · First screen continuity")
      .setMessage("GLASS can record browser-origin events locally. Whole-device frames require your Android permission for each capture session. A visible notification stays on; frames are sampled, stored privately, and rolled over. Secure screens and lock periods cannot be recorded. Nothing is uploaded. Start capture now?")
      .setPositiveButton("Request Android consent",(d,w)->requestCapture())
      .setNegativeButton("Not now",(d,w)->{Journal.event(this,"CAPTURE_GAP","user","first-launch-consent-declined");})
      .show();
    }
  }
  private void navigate(String raw){
    String url=raw.trim();if(url.isEmpty())return;
    if(url.startsWith("glass://")){
      // Only direct user actions can execute the internal terminal parser.
      String result=Bridge.nativeTerminal(url);status.setText(result);if(!privateProfile)Journal.event(this,"TERMINAL_QUERY","user","local read-only terminal");return;
    }
    if(!url.contains("://"))url="https://"+url;
    Uri uri=Uri.parse(url);if(!"https".equalsIgnoreCase(uri.getScheme())||uri.getHost()==null){status.setText("Refused: HTTPS URL required");return;}
    page.loadUrl(url);
  }
  private void requestCapture(){
    if(CaptureService.active){status.setText("Capture is already active");return;}
    String result=Bridge.transition(0,"new request");if(result.contains("error")){status.setText(result);return;}
    Journal.event(this,"CAPTURE_REQUEST","user","Android MediaProjection consent requested");
    MediaProjectionManager manager=(MediaProjectionManager)getSystemService(Context.MEDIA_PROJECTION_SERVICE);
    Intent ask=Build.VERSION.SDK_INT>=34?manager.createScreenCaptureIntent(MediaProjectionConfig.createConfigForDefaultDisplay()):manager.createScreenCaptureIntent();
    startActivityForResult(ask,CAPTURE_REQUEST);
  }
  @Override protected void onActivityResult(int requestCode,int resultCode,Intent data){super.onActivityResult(requestCode,resultCode,data);
    if(requestCode!=CAPTURE_REQUEST)return;
    if(resultCode==RESULT_OK&&data!=null){
      Intent start=new Intent(this,CaptureService.class).setAction(CaptureService.ACTION_START);
      start.putExtra("permission_result_code",resultCode);start.putExtra("permission_data",data);
      startForegroundService(start);status.setText("Authorized · starting visible capture service");
    }else{
      Bridge.transition(2,"denied");Journal.event(this,"CAPTURE_GAP","user","Android screen capture permission denied");
      status.setText("Screen capture denied · gap recorded");
    }
  }
  @Override protected void onResume(){super.onResume();if(status!=null&&CaptureService.active)status.setText("Capture active · Android indicator visible");}
  @Override public void onBackPressed(){if(page!=null&&page.canGoBack())page.goBack();else super.onBackPressed();}
  @Override protected void onDestroy(){if(privateProfile&&page!=null){page.clearHistory();page.clearCache(true);CookieManager.getInstance().removeAllCookies(null);WebStorage.getInstance().deleteAllData();}if(page!=null)page.destroy();super.onDestroy();}
}
