package com.glass.unison;
import java.nio.charset.StandardCharsets;
public class MainActivity {
    static {System.loadLibrary("glass_pty_test");}
    private native long nativeShellOpen(String cwd);
    private native byte[] nativeShellRead(long h);
    private native void nativeShellWrite(long h,byte[] b);
    private native void nativeShellResize(long h,int c,int r);
    private native void nativeShellStop(long h);
    private native void nativeShellDispose(long h);
    public static void main(String[] args){
        MainActivity t=new MainActivity();
        long h=t.nativeShellOpen(System.getProperty("user.dir"));
        if(h==0)throw new AssertionError("PTY failed");
        t.nativeShellResize(h,80,24);
        t.nativeShellWrite(h,"echo GLASS_PTY_OK\n".getBytes(StandardCharsets.UTF_8));
        StringBuilder transcript=new StringBuilder();
        long deadline=System.currentTimeMillis()+5000;
        while(System.currentTimeMillis()<deadline){
          byte[] b=t.nativeShellRead(h);
          if(b==null)break;
          transcript.append(new String(b,StandardCharsets.UTF_8));
          if(transcript.toString().contains("GLASS_PTY_OK"))break;
        }
        t.nativeShellStop(h);t.nativeShellDispose(h);
        if(!transcript.toString().contains("GLASS_PTY_OK"))throw new AssertionError(transcript);
        System.out.println("GLASS PTY JNI PASS");
    }
}
