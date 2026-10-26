package org.glass.nativebrowser;
import android.app.Application;
import android.webkit.WebView;
/** A separate browser process receives a distinct WebView directory. */
public final class GlassApplication extends Application {
  @Override public void onCreate(){super.onCreate();
    // Must be called before constructing any WebView in this process.
    if(Application.getProcessName().endsWith(":private"))WebView.setDataDirectorySuffix("glass-private");
  }
}
