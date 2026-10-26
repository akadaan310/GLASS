package org.glass.nativebrowser;
import android.app.Service;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ServiceInfo;
import android.hardware.display.DisplayManager;
import android.hardware.display.VirtualDisplay;
import android.media.Image;
import android.media.ImageReader;
import android.media.projection.MediaProjection;
import android.media.projection.MediaProjectionManager;
import android.os.Handler;
import android.os.HandlerThread;
import android.os.IBinder;
import android.os.Build;
import android.os.SystemClock;
import android.graphics.Bitmap;
import android.graphics.PixelFormat;
import android.util.DisplayMetrics;
import android.view.WindowManager;
import java.io.File;
import java.io.FileOutputStream;
import java.nio.ByteBuffer;
import java.security.MessageDigest;
import java.util.Arrays;
import java.util.Comparator;

/** Android-owned recording boundary; never hidden, never restarted without new user consent. */
public final class CaptureService extends Service {
  static final String ACTION_START="org.glass.nativebrowser.START_CAPTURE";
  static final String ACTION_STOP="org.glass.nativebrowser.STOP_CAPTURE";
  private static final String CHANNEL="glass-visible-recording";
  static volatile boolean active=false;
  private MediaProjection projection;
  private VirtualDisplay display;
  private ImageReader reader;
  private HandlerThread thread;
  private Handler background;
  private long nextFrameMs=0,frameIndex=0;
  private volatile boolean closed=false;
  @Override public IBinder onBind(Intent i){return null;}
  @Override public int onStartCommand(Intent intent,int flags,int startId){
    if(intent==null){stopSelf();return START_NOT_STICKY;}
    if(ACTION_STOP.equals(intent.getAction())){shutdown("user_stop");return START_NOT_STICKY;}
    if(!ACTION_START.equals(intent.getAction())||active){stopSelf();return START_NOT_STICKY;}
    try{
      NotificationManager nm=(NotificationManager)getSystemService(NOTIFICATION_SERVICE);
      nm.createNotificationChannel(new NotificationChannel(CHANNEL,"GLASS recording",NotificationManager.IMPORTANCE_LOW));
      Intent stop=new Intent(this,CaptureService.class).setAction(ACTION_STOP);
      PendingIntent pi=PendingIntent.getService(this,1,stop,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_IMMUTABLE);
      Notification n=new Notification.Builder(this,CHANNEL).setSmallIcon(android.R.drawable.ic_menu_view)
        .setContentTitle("GLASS screen continuity active").setContentText("Locally sampling screen · Tap Stop to end")
        .setOngoing(true).addAction(new Notification.Action.Builder(android.R.drawable.ic_menu_close_clear_cancel,"Stop",pi).build()).build();
      startForeground(41,n,ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PROJECTION);
      int result=intent.getIntExtra("permission_result_code",0);
      Intent data=Build.VERSION.SDK_INT>=33?intent.getParcelableExtra("permission_data",Intent.class):intent.getParcelableExtra("permission_data");
      if(data==null||result!=-1)throw new SecurityException("Android permission result absent");
      MediaProjectionManager manager=(MediaProjectionManager)getSystemService(Context.MEDIA_PROJECTION_SERVICE);
      projection=manager.getMediaProjection(result,data);
      thread=new HandlerThread("GLASS-frame-sampler");thread.start();background=new Handler(thread.getLooper());
      projection.registerCallback(new MediaProjection.Callback(){@Override public void onStop(){shutdown("projection_stopped_or_screen_locked");}},background);
      DisplayMetrics metrics=new DisplayMetrics();((WindowManager)getSystemService(WINDOW_SERVICE)).getDefaultDisplay().getRealMetrics(metrics);
      reader=ImageReader.newInstance(metrics.widthPixels,metrics.heightPixels,PixelFormat.RGBA_8888,2);
      reader.setOnImageAvailableListener(r->sample(r),background);
      display=projection.createVirtualDisplay("GLASS-consented-screen",metrics.widthPixels,metrics.heightPixels,metrics.densityDpi,
         DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,reader.getSurface(),null,background);
      active=true;String state=Bridge.transition(1,"approved");Journal.write(this,state.contains("error")?Bridge.event("CAPTURE_GAP","system",state):Bridge.event("CAPTURE_STARTED","system","authorized foreground session"));
    }catch(Exception e){Journal.event(this,"CAPTURE_GAP","system","permission or device capture initialization failed");
      shutdown("capture_init_failed");}
    return START_NOT_STICKY;
  }
  private static String hex(byte[] v){StringBuilder b=new StringBuilder();for(byte x:v)b.append(String.format(java.util.Locale.ROOT,"%02x",x&255));return b.toString();}
  private void sample(ImageReader r){
    Image image=null;
    try{
      if(closed||!active)return;
      image=r.acquireLatestImage();if(image==null)return;
      long ms=SystemClock.elapsedRealtime();if(ms<nextFrameMs)return;nextFrameMs=ms+1000; // <=1 fps by contract
      final int w=image.getWidth(),h=image.getHeight();
      Image.Plane plane=image.getPlanes()[0];int stride=plane.getRowStride(),pixel=plane.getPixelStride();
      if(pixel!=4||w<=0||h<=0||w>8192||h>8192)return;
      Bitmap bufferBitmap=Bitmap.createBitmap(stride/pixel,h,Bitmap.Config.ARGB_8888);
      ByteBuffer data=plane.getBuffer();bufferBitmap.copyPixelsFromBuffer(data);
      Bitmap cut=Bitmap.createBitmap(bufferBitmap,0,0,w,h);
      final int scale=Math.max(1,(Math.max(w,h)+959)/960);
      Bitmap scaled=Bitmap.createScaledBitmap(cut,Math.max(1,w/scale),Math.max(1,h/scale),true);
      File dir=new File(getNoBackupFilesDir(),"consented-frames");if(!dir.exists()&&!dir.mkdirs())throw new IllegalStateException("cannot create private frames directory");
      File file=new File(dir,String.format(java.util.Locale.ROOT,"frame-%016d.jpg",++frameIndex));
      try(FileOutputStream out=new FileOutputStream(file)){if(!scaled.compress(Bitmap.CompressFormat.JPEG,70,out))throw new IllegalStateException("JPEG encoder failed");out.getFD().sync();}
      byte[] bytes=java.nio.file.Files.readAllBytes(file.toPath());String digest=hex(MessageDigest.getInstance("SHA-256").digest(bytes));
      Journal.event(this,"SCREEN_FRAME","media_projection","sample_1fps sha256="+digest+" bytes="+bytes.length+" file="+file.getName());
      File[] files=dir.listFiles((d,name)->name.startsWith("frame-")&&name.endsWith(".jpg"));if(files!=null&&files.length>120){
        Arrays.sort(files,Comparator.comparing(File::getName));for(int i=0;i<files.length-120;i++){
          if(files[i].delete())Journal.event(this,"FRAME_EVICTED","retention",files[i].getName());
        }
      }
      if(scaled!=cut)scaled.recycle();cut.recycle();bufferBitmap.recycle();
    }catch(Exception e){Journal.event(this,"FRAME_GAP","media_projection","sample unavailable; no complete-frame claim");}
    finally{if(image!=null)image.close();}
  }
  private synchronized void shutdown(String reason){
    if(closed)return;closed=true;boolean wasActive=active;active=false;
    Journal.event(this,"CAPTURE_GAP","system",reason);
    try{Bridge.transition(3,reason);}catch(Exception ignored){}
    if(display!=null){display.release();display=null;}
    if(reader!=null){reader.close();reader=null;}
    if(projection!=null){MediaProjection p=projection;projection=null;p.stop();}
    if(thread!=null){thread.quitSafely();thread=null;}
    stopForeground(STOP_FOREGROUND_REMOVE);stopSelf();
  }
  @Override public void onDestroy(){shutdown("service_destroyed");super.onDestroy();}
}
