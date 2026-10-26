package org.glass.nativebrowser;
import android.content.Context;
import java.io.*;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Arrays;

/** Local, SHA-256-linked event ledger; not digitally signed or remote-anchored. */
final class Journal {
  private static final Object LOCK=new Object();
  private static byte[] previous=new byte[32];
  private static boolean initialized=false;
  private static final String FILE="glass-events-v1.jsonl";
  private Journal(){}
  private static String hex(byte[] bytes){StringBuilder b=new StringBuilder();for(byte x:bytes)b.append(String.format(java.util.Locale.ROOT,"%02x",x&255));return b.toString();}
  static void write(Context context,String event) {
    if(event==null||event.length()>4096)throw new IllegalArgumentException("invalid event receipt");
    synchronized(LOCK){
      try{
        File path=new File(context.getNoBackupFilesDir(),FILE);
        if(!initialized){
          if(path.exists()&&path.length()>0){
            // On process restart keep the last hash link; a later offline verifier
            // must still validate the full chain and mark missing time as a gap.
            try(BufferedReader in=new BufferedReader(new FileReader(path))){String last,line;last=null;while((line=in.readLine())!=null)last=line;
              if(last!=null){org.json.JSONObject row=new org.json.JSONObject(last);String digest=row.getString("hash");if(digest.matches("[0-9a-f]{64}"))
                for(int i=0;i<32;i++)previous[i]=(byte)Integer.parseInt(digest.substring(i*2,i*2+2),16);
              }
            }
          }
          initialized=true;
        }
        byte[] body=event.getBytes(StandardCharsets.UTF_8);
        MessageDigest digest=MessageDigest.getInstance("SHA-256");
        digest.update(previous);digest.update(ByteBuffer.allocate(4).putInt(body.length).array());digest.update(body);
        previous=digest.digest();
        String row="{\"hash\":\""+hex(previous)+"\",\"event\":"+event+"}\n";
        try(FileOutputStream out=new FileOutputStream(path,true)){out.write(row.getBytes(StandardCharsets.UTF_8));out.getFD().sync();}
      }catch(Exception e){android.util.Log.e("GLASS-Journal","Cannot append local event",e);}
    }
  }
  static void event(Context context,String kind,String origin,String detail){write(context,Bridge.event(kind,origin,detail));}
}
