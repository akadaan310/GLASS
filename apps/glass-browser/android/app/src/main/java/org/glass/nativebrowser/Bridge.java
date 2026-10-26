package org.glass.nativebrowser;
import android.os.SystemClock;
final class Bridge {
  static {System.loadLibrary("glass_native");}
  static native String nativeEvent(String kind,String origin,String detail,long monotonicNs);
  static native String nativeTransition(int action,String reason,long monotonicNs);
  static native String nativeStatus();
  static native String nativeTerminal(String address);
  static String event(String kind,String origin,String detail){return nativeEvent(kind,origin,detail,SystemClock.elapsedRealtimeNanos());}
  static String transition(int action,String reason){return nativeTransition(action,reason,SystemClock.elapsedRealtimeNanos());}
  private Bridge(){}
}
