package org.glass.unison;

import org.json.JSONObject;
import java.io.OutputStream;
import java.net.URL;
import javax.net.ssl.HttpsURLConnection;
import java.nio.charset.StandardCharsets;
import java.util.ArrayDeque;
import java.util.UUID;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

/** Opt-in GLASS-LIVE/0.1 private numeric event publisher.
 * Audio, recognized words, raw text, names and persistent device identity
 * never enter the queue. HTTPS only. No upload runs without user enable.
 */
public final class EventPublisher {
    public interface Status { void changed(String state); }
    private final ArrayDeque<JSONObject> queue=new ArrayDeque<>();
    private final ScheduledExecutorService worker=Executors.newSingleThreadScheduledExecutor();
    private final Status status;
    private volatile boolean enabled=false;
    private volatile String endpoint="",token="",room="";
    private long eventCount=0,discarded=0;
    private long lastFrameNs=0;

    public EventPublisher(Status status){
        this.status=status;
        worker.scheduleWithFixedDelay(this::flushSafely,600,600,TimeUnit.MILLISECONDS);
    }
    public synchronized void configure(String endpoint,String token,String room){
        if(endpoint==null||!endpoint.startsWith("https://"))
            throw new IllegalArgumentException("HTTPS event endpoint required");
        if(endpoint.contains("@")||endpoint.contains("?")||endpoint.contains("#"))
            throw new IllegalArgumentException("Credentials/query URLs are refused");
        try{
            URL check=new URL(endpoint);
            if(!"https".equals(check.getProtocol())||check.getHost().isEmpty())
                throw new IllegalArgumentException("Invalid HTTPS host");
        }catch(Exception e){throw new IllegalArgumentException("Invalid stream URL",e);}
        if(token==null||token.length()<24||token.length()>1024)
            throw new IllegalArgumentException("Private write capability must be provided");
        if(room==null||!room.matches("[A-Za-z0-9_-]{8,64}"))
            throw new IllegalArgumentException("Invalid room code");
        this.endpoint=endpoint;this.token=token;this.room=room;
        queue.clear();enabled=true;
        status.changed("STREAM ENABLED / derived numbers only");
    }
    public synchronized void disable(){
        enabled=false;token="";endpoint="";room="";queue.clear();
        status.changed("STREAM DISABLED / no network publishing");
    }
    public void close(){
        disable();worker.shutdownNow();
    }
    public synchronized int backlog(){return queue.size();}
    public synchronized long discarded(){return discarded;}

    private void push(String kind,JSONObject features){
        if(!enabled)return;
        try{
            JSONObject body=new JSONObject();
            body.put("room",room);
            body.put("eventId","g"+UUID.randomUUID().toString().replace("-",""));
            body.put("kind",kind);
            body.put("features",features);
            if(queue.size()>=64){queue.removeFirst();discarded++;}
            queue.addLast(body);
            eventCount++;
        }catch(Exception e){discarded++;}
    }
    public synchronized void trace(TraceMath.Frame frame){
        long now=System.nanoTime();
        if(now-lastFrameNs<1_000_000_000L)return; // publish at most 1 trace/s
        lastFrameNs=now;
        JSONObject x=new JSONObject();
        try{
            x.put("traceId","dsp.rms");x.put("rms",frame.rms);
            x.put("peak",frame.peak);x.put("zcr",frame.zcr);
            x.put("centroidHz",frame.centroidHz);x.put("flux",frame.flux);
            x.put("lowEnergy",frame.lowEnergy);x.put("midEnergy",frame.midEnergy);
            x.put("highEnergy",frame.highEnergy);x.put("pitchHz",frame.pitchHz);
            x.put("noiseFloor",frame.noiseFloor);x.put("frameMs",frame.frameMs);
            x.put("voice",frame.voiced);x.put("onset",frame.onset);
            x.put("generation",frame.seq);
            push("audio.trace",x);
        }catch(Exception ignored){}
    }
    public synchronized void proposed(LanguageClock.Candidate c,double threshold,int confirmations){
        JSONObject x=new JSONObject();
        try{
            x.put("traceId","language.clock");
            x.put("language",c.language);
            x.put("confidence",c.confidence);
            x.put("threshold",threshold);
            x.put("confirmations",confirmations);
            x.put("generation",c.phrase);
            push("language.candidate",x);
        }catch(Exception ignored){}
    }
    public synchronized void confirmed(String language,int confirmations,int switches,int disagreements){
        JSONObject x=new JSONObject();
        try{
            x.put("traceId","language.clock");x.put("language",language);
            x.put("verdict","confirmed");x.put("confirmations",confirmations);
            x.put("switches",switches);x.put("disagreement",disagreements);
            push("language.confirmed",x);
        }catch(Exception ignored){}
    }
    public synchronized void state(String state) {
        JSONObject x=new JSONObject();
        try{x.put("state",state);x.put("traceId","language.clock");push("session.state",x);}
        catch(Exception ignored){}
    }
    private void flushSafely(){
        JSONObject data;String e,t;
        synchronized(this) {
            if(!enabled||queue.isEmpty())return;
            data=queue.peekFirst();e=endpoint;t=token;
        }
        if(data==null||e.isEmpty()||t.isEmpty())return;
        HttpsURLConnection conn=null;
        try{
            conn=(HttpsURLConnection)new URL(e).openConnection();
            conn.setRequestMethod("POST");conn.setConnectTimeout(3000);conn.setReadTimeout(3000);
            conn.setDoOutput(true);conn.setUseCaches(false);
            conn.setRequestProperty("Content-Type","application/json; charset=utf-8");
            conn.setRequestProperty("Authorization","Bearer "+t);
            byte[] bytes=data.toString().getBytes(StandardCharsets.UTF_8);
            if(bytes.length>2048)throw new IllegalStateException("EVENT_TOO_LARGE");
            try(OutputStream out=conn.getOutputStream()){out.write(bytes);}
            int statusCode=conn.getResponseCode();
            if(statusCode==200||statusCode==201){
                synchronized(this){if(queue.peekFirst()==data)queue.removeFirst();}
                status.changed("EVENT STREAM / ACK");
            }else if(statusCode==401||statusCode==403){
                disable();status.changed("STREAM REJECTED: private capability");
            }else if(statusCode==400||statusCode==413){
                synchronized(this){if(queue.peekFirst()==data){queue.removeFirst();discarded++;}}
                status.changed("EVENT REJECTED / schema or size");
            }else status.changed("STREAM WAIT / "+statusCode);
        }catch(Exception e1){status.changed("STREAM OFFLINE / retrying bounded queue");}
        finally{if(conn!=null)conn.disconnect();}
    }
}
