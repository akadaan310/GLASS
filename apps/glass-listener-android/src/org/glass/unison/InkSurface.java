package org.glass.unison;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.view.View;

/** GLASS reactive ink plane — draws only measured local I/O envelopes.
 * No audio playback, no generated art, no background session.
 * Wave traces are amplitude/flux summaries, NOT plots of raw PCM.
 */
public final class InkSurface extends View {
    private final Paint p=new Paint(Paint.ANTI_ALIAS_FLAG);
    private final float[] magnitude=new float[180],change=new float[180];
    private int cursor=0;
    private volatile boolean active=false;
    private volatile double currentRms=0,currentFlux=0,currentPitch=0,currentZcr=0,currentCentroid=0;
    private volatile long frames=0;
    private volatile String language="UNKNOWN",status="MIC OFF",signal="NOT CAPTURING";
    private final int BG=Color.rgb(7,12,19),GOLD=Color.rgb(237,188,106),
        CYAN=Color.rgb(80,204,231),MUTED=Color.rgb(141,163,174),
        GREEN=Color.rgb(91,225,169);
    public InkSurface(Context context){super(context);setLayerType(View.LAYER_TYPE_SOFTWARE,null);}
    private static float clamp(double x,double low,double high) {
        return (float)Math.max(low,Math.min(high,x));
    }
    public synchronized void ingest(TraceMath.Frame frame) {
        magnitude[cursor]=clamp(frame.rms*4,0,1);
        change[cursor]=clamp(frame.flux,0,1);
        cursor=(cursor+1)%magnitude.length;
        currentRms=frame.rms;currentFlux=frame.flux;currentPitch=frame.pitchHz;
        currentZcr=frame.zcr;currentCentroid=frame.centroidHz;
        signal=frame.voiced?"VOICE CANDIDATE":"QUIET / AMBIENCE";
        frames=frame.seq;
        postInvalidate();
    }
    /** OS recognizer mode shares no raw PCM with our own AudioRecord.
     * Its reported RMS callback can still drive a clearly labelled visual
     * envelope. This is an OS measurement hint, not 16k sample math.
     */
    public synchronized void ingestOsRms(double hint){
        double v=clamp(hint,0,1);
        double before=currentRms;
        magnitude[cursor]=(float)v;
        change[cursor]=clamp(Math.abs(v-before),0,1);
        cursor=(cursor+1)%magnitude.length;
        currentRms=v;currentFlux=Math.abs(v-before);
        currentPitch=0;currentCentroid=0;currentZcr=0;
        signal="OS RMS HINT / NOT RAW PCM";frames++;
        postInvalidate();
    }
    public synchronized void setMode(boolean on){active=on;status=on?"LOCAL MICROPHONE LIVE":"MIC OFF";postInvalidate();}
    public synchronized void setStatus(String label){status=label;postInvalidate();}
    public synchronized void setLanguage(String label){language=label;postInvalidate();}
    private void text(Canvas c,String value,float x,float y,float size,int color,boolean bold){
        p.setColor(color);p.setStyle(Paint.Style.FILL);p.setTextSize(size);
        p.setTypeface(bold?android.graphics.Typeface.create("monospace",android.graphics.Typeface.BOLD):
                         android.graphics.Typeface.create("monospace",android.graphics.Typeface.NORMAL));
        c.drawText(value,x,y,p);
    }
    private void line(Canvas c,float x1,float y1,float x2,float y2,int color,float alpha,float width){
        p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(width);p.setColor(color);p.setAlpha((int)(255*alpha));
        c.drawLine(x1,y1,x2,y2,p);p.setAlpha(255);p.setStyle(Paint.Style.FILL);
    }
    @Override protected synchronized void onDraw(Canvas c){
        super.onDraw(c);
        int w=getWidth(),h=getHeight();
        if(w<=0||h<=0)return;
        c.drawColor(BG);
        float sx=w/390f,sy=h/580f,unit=Math.min(sx,sy);
        float margin=22*unit;
        text(c,"GLASS / UNISON",margin,42*sy,13*unit,GOLD,true);
        text(c,"SUBSTRATE I/O    .01",margin,66*sy,9*unit,MUTED,false);
        String light=active?"●  LIVE":"○  IDLE";
        text(c,light,w-120*unit,43*sy,12*unit,active?GREEN:MUTED,true);
        line(c,margin,82*sy,w-margin,82*sy,MUTED,.20f,1);
        // Stable concentric sample rings. Growth is driven by real RMS, not time.
        float cx=w*.5f,cy=h*.46f;
        float limit=Math.min(w,h)*.30f;
        double sound=clamp(currentRms*4,0,1),flux=clamp(currentFlux,0,1);
        for(int ring=0;ring<8;ring++){
            float t=(ring+1)/8f;
            float radius=limit*(.18f+t*.76f)+(float)sound*(20+ring*3)*unit;
            p.setStyle(Paint.Style.STROKE);
            p.setStrokeWidth(ring==3?1.7f:1.0f);
            p.setColor(ring<4?CYAN:GOLD);
            p.setAlpha(28+ring*7+(active?(int)(flux*26):0));
            c.drawCircle(cx,cy,radius,p);
        }
        p.setStyle(Paint.Style.FILL);p.setAlpha(255);
        text(c,"⟐",cx-15*unit,cy+10*unit,34*unit,active?GOLD:MUTED,true);
        // Actual measured amplitude and flux envelope over the last 180 frames.
        float graphY=h*.78f,graphH=57*unit,x0=margin,gw=w-2*margin;
        line(c,x0,graphY,x0+gw,graphY,MUTED,.28f,1);
        Path envelope=new Path(),fluctuation=new Path();
        for(int i=0;i<magnitude.length;i++){
            int idx=(cursor+i)%magnitude.length;
            float x=x0+gw*i/(magnitude.length-1f);
            float y=graphY-magnitude[idx]*graphH;
            float fy=graphY+graphH*.38f-change[idx]*graphH*.40f;
            if(i==0){envelope.moveTo(x,y);fluctuation.moveTo(x,fy);}
            else {envelope.lineTo(x,y);fluctuation.lineTo(x,fy);}
        }
        p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2.1f*unit);p.setColor(CYAN);p.setAlpha(245);
        c.drawPath(envelope,p);
        p.setStrokeWidth(1.3f*unit);p.setColor(GOLD);p.setAlpha(185);c.drawPath(fluctuation,p);
        p.setAlpha(255);p.setStyle(Paint.Style.FILL);
        text(c,"MIC PCM16  /  RMS",margin,graphY-graphH-9*unit,10*unit,CYAN,true);
        text(c,"SPECTRAL FLUX",margin,graphY+graphH*.40f+17*unit,10*unit,GOLD,false);
        // Honest diagnostic labels.
        float base=h-91*unit;
        text(c,status,margin,base,11*unit,active?GREEN:MUTED,true);
        text(c,"SIGNAL: "+signal,margin,base+18*unit,10*unit,MUTED,false);
        text(c,"LANG: "+language,margin,base+36*unit,10*unit,MUTED,false);
        text(c,"RMS "+fmt(currentRms)+"  ZCR "+fmt(currentZcr),margin,base+54*unit,9*unit,MUTED,false);
        text(c,"CENTROID "+(int)currentCentroid+" Hz  PITCH PROXY "+(int)currentPitch+" Hz",margin,base+72*unit,9*unit,MUTED,false);
        if(active)postInvalidateDelayed(50);
    }
    private static String fmt(double x){return String.format(java.util.Locale.ROOT,"%.3f",x);}
}
