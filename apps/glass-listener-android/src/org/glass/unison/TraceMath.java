package org.glass.unison;

/** Pure Java, deterministic on-device microphone measurements.
 * These are inexpensive DSP OBSERVATIONS, not trained MUQRI CTC or Tajwid
 * verdicts. The full engine requires a phoneme model and acoustic references.
 * PCM16 mono; fixed 16 kHz. Never saves or transmits samples.
 */
public final class TraceMath {
    public static final int SAMPLE_RATE=16000;
    private double noiseFloor=0.012;
    private final double[] lastBands=new double[5];
    private long frameIndex=0;
    private boolean lastVoice=false;

    public static final class Frame {
        public final long seq;
        public final double rms,peak,zcr,centroidHz,flux,lowEnergy,midEnergy,highEnergy,pitchHz,noiseFloor;
        public final boolean voiced,onset;
        public final int frameMs;
        public Frame(long seq,double rms,double peak,double zcr,double centroidHz,double flux,
                     double lowEnergy,double midEnergy,double highEnergy,double pitchHz,
                     double noiseFloor,boolean voiced,boolean onset,int frameMs) {
            this.seq=seq;this.rms=rms;this.peak=peak;this.zcr=zcr;this.centroidHz=centroidHz;this.flux=flux;
            this.lowEnergy=lowEnergy;this.midEnergy=midEnergy;this.highEnergy=highEnergy;
            this.pitchHz=pitchHz;this.noiseFloor=noiseFloor;this.voiced=voiced;this.onset=onset;this.frameMs=frameMs;
        }
    }
    private static double powerAt(double[] x,int n,int hz) {
        // Goertzel at a declared frequency; returns window-normalized energy.
        double omega=2*Math.PI*hz/SAMPLE_RATE;
        double c=2*Math.cos(omega),a=0,b=0;
        for(int i=0;i<n;i++){
            double next=x[i]+c*a-b;
            b=a;a=next;
        }
        return Math.max(0,(a*a+b*b-c*a*b)/(n*n));
    }
    private static double pitchProxy(double[] x,int n) {
        // ACF peak is a proxy; it is NOT a fundamental-frequency claim on noise.
        int minLag=Math.max(1,SAMPLE_RATE/450),maxLag=Math.min(n/2,SAMPLE_RATE/75);
        double best=0;int lag=0;
        double total=0;
        for(int i=0;i<n;i++)total+=x[i]*x[i];
        if(total<0.0005)return 0;
        for(int j=minLag;j<=maxLag;j++){
            double numerator=0,left=0,right=0;
            for(int i=j;i<n;i++){
                numerator+=x[i]*x[i-j];left+=x[i]*x[i];right+=x[i-j]*x[i-j];
            }
            double corr=left>1e-12 && right>1e-12 ? numerator/Math.sqrt(left*right):0;
            if(corr>best){best=corr;lag=j;}
        }
        return best>=0.6 && lag>0?((double)SAMPLE_RATE/lag):0;
    }

    public synchronized Frame process(short[] pcm,int length) {
        if(pcm==null||length<128||length>pcm.length||length>4096)
            throw new IllegalArgumentException("Bounded valid PCM16 frame required");
        double[] x=new double[length];
        double sum=0,peak=0,cross=0;
        for(int i=0;i<length;i++){
            double v=pcm[i]/32768.0;
            x[i]=v;sum+=v*v;peak=Math.max(peak,Math.abs(v));
            if(i>0 && ((pcm[i-1]>=0)!=(pcm[i]>=0)))cross++;
        }
        double rms=Math.sqrt(sum/length), zcr=cross/(length-1.0);
        int[] hz={180,400,850,1750,3350};
        double weighted=0,weightSum=0,difference=0;
        double[] bands=new double[hz.length];
        for(int j=0;j<hz.length;j++){
            bands[j]=powerAt(x,length,hz[j]);
            weighted+=bands[j]*hz[j];weightSum+=bands[j];
            double pos=Math.max(0,bands[j]-lastBands[j]);
            difference+=pos;
            lastBands[j]=bands[j];
        }
        double centroid=weightSum>1e-12?weighted/weightSum:0;
        double flux=weightSum>1e-12?Math.min(1,difference/(weightSum+1e-12)):0;
        // Adaptive floor changes only under quiet observations to resist loud adaptation.
        boolean voice=rms>Math.max(.018,noiseFloor*2.8);
        if(!voice)noiseFloor=0.985*noiseFloor+0.015*rms;
        else noiseFloor=Math.min(noiseFloor*1.001,.10);
        double low=bands[0]+bands[1],mid=bands[2]+bands[3],high=bands[4];
        double total=low+mid+high+1e-12;
        double pitch=voice?pitchProxy(x,length):0;
        Frame frame=new Frame(++frameIndex,rms,peak,zcr,centroid,flux,
          low/total,mid/total,high/total,pitch,noiseFloor,voice,voice&&!lastVoice,
          (int)Math.round(length*1000.0/SAMPLE_RATE));
        lastVoice=voice;
        return frame;
    }
}
