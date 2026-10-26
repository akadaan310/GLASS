package org.glass.unison;

/** Phrase clock and 30-confirmation feedback calculus, no covert language claims.
 * Acoustic centroids provide weak hypotheses only; on-device OS language
 * detection may provide stronger evidence if explicitly enabled and supported.
 * A confirmation improves user-specific hints but cannot guarantee recognition.
 */
public final class LanguageClock {
    public static final int BOOTSTRAP_CONFIRMATIONS=30;
    public static final class Candidate {
        public final String language,reason;
        public final double confidence;
        public final long phrase;
        public final boolean requiresConfirmation,possibleSwitch;
        Candidate(String language,double confidence,long phrase,String reason,
                  boolean confirm,boolean change){
            this.language=language;this.confidence=confidence;this.phrase=phrase;
            this.reason=reason;this.requiresConfirmation=confirm;this.possibleSwitch=change;
        }
    }
    private static final String[] LABELS={"ar","en","other"};
    private static final int DIM=5;
    private final int[] counts=new int[3];
    private final double[][] centroids=new double[3][DIM];
    private final double[] accum=new double[DIM];
    private int confirmed=0,correct=0,wrong=0,switches=0;
    private long phrase=0,voicedFrames=0,quietFrames=0;
    private boolean withinPhrase=false;
    private Candidate awaiting;
    private String previousConfirmed="unknown";
    private String osLanguage="unknown";
    private double osConfidence=0;
    private final double[] latestFeatures=new double[DIM];

    private static int id(String s){
        for(int i=0;i<LABELS.length;i++)if(LABELS[i].equals(s))return i;
        return -1;
    }
    private static double clip(double x,double low,double high){
        return Math.max(low,Math.min(high,x));
    }
    private static double[] vector(TraceMath.Frame f){
        return new double[]{
            f.zcr,clip(f.centroidHz/4000.0,0,1),
            f.lowEnergy, f.highEnergy,clip(f.pitchHz/500.0,0,1)
        };
    }
    public synchronized void externalOnDeviceHint(String language,double evidence){
        if(id(language)<0){osLanguage="unknown";osConfidence=0;}
        else{osLanguage=language;osConfidence=clip(evidence,0,0.98);}
    }
    public synchronized Candidate onFrame(TraceMath.Frame frame){
        if(awaiting!=null)return null;
        if(frame.voiced) {
            if(!withinPhrase){withinPhrase=true;voicedFrames=0;quietFrames=0;
                for(int i=0;i<DIM;i++)accum[i]=0;}
            double[] v=vector(frame);
            for(int i=0;i<DIM;i++)accum[i]+=v[i];
            voicedFrames++;quietFrames=0;return null;
        }
        if(!withinPhrase)return null;
        quietFrames++;
        if(quietFrames<5)return null;
        withinPhrase=false;
        if(voicedFrames<5)return null; // Ignore a very brief artifact.
        for(int j=0;j<DIM;j++)latestFeatures[j]=accum[j]/voicedFrames;
        phrase++;
        return awaiting=propose();
    }
    private Candidate propose(){
        String language="unknown"; double confidence=0;
        String reason="ABSTAIN: spectral measurements alone are not a reliable linguistic identity";
        if(!osLanguage.equals("unknown")&&osConfidence>0){
            language=osLanguage;confidence=osConfidence;reason="on-device speech recognizer hint";
        } else {
            double best=Double.POSITIVE_INFINITY,runner=Double.POSITIVE_INFINITY;
            int winning=-1;
            for(int i=0;i<3;i++){
                if(counts[i]<3)continue;
                double dist=0;
                for(int j=0;j<DIM;j++){
                    double weight=j==0?9:j==1?2:1;
                    double delta=latestFeatures[j]-centroids[i][j];
                    dist+=weight*delta*delta;
                }
                if(dist<best){runner=best;best=dist;winning=i;}
                else if(dist<runner)runner=dist;
            }
            if(winning>=0 && Double.isFinite(runner)){
                language=LABELS[winning];
                // A FEATURE-ONLY hint is intentionally capped at 0.6.
                confidence=Math.min(.6,.25+.35*clip((runner-best)/(runner+1e-12),0,1));
                reason="unvalidated user-calibrated DSP acoustic similarity";
            }
        }
        boolean changed=!previousConfirmed.equals("unknown")
            &&!language.equals("unknown")&&!language.equals(previousConfirmed);
        double threshold=threshold();
        boolean require=confirmed<BOOTSTRAP_CONFIRMATIONS ||
            confidence<threshold || changed || language.equals("unknown");
        return new Candidate(language,confidence,phrase,reason,require,changed);
    }
    public synchronized double threshold(){
        // Laplace-smoothed observed confirmation agreement, not a probability
        // that the next phrase is correct.
        double agreement=(correct+1.0)/(correct+wrong+2.0);
        return clip(0.70+0.18*(1-agreement),0.70,0.88);
    }
    public synchronized Candidate pending(){return awaiting;}
    public synchronized void confirm(String language){
        int i=id(language);
        if(i<0)throw new IllegalArgumentException("Confirm only ar/en/other");
        if(awaiting==null)throw new IllegalStateException("No speech phrase awaiting confirmation");
        if(!awaiting.language.equals("unknown")){
            if(awaiting.language.equals(language))correct++;
            else wrong++;
        }
        if(!previousConfirmed.equals("unknown")&&!previousConfirmed.equals(language))switches++;
        int old=counts[i];
        for(int j=0;j<DIM;j++)centroids[i][j]=(centroids[i][j]*old+latestFeatures[j])/(old+1.0);
        counts[i]++;confirmed++;
        previousConfirmed=language;
        awaiting=null;osLanguage="unknown";osConfidence=0;
    }
    public synchronized void dismissAsUncertain(){
        // Rejects current prediction without pretending to know truth.
        awaiting=null;osLanguage="unknown";osConfidence=0;
    }
    public synchronized int confirmations(){return confirmed;}
    public synchronized int switches(){return switches;}
    public synchronized int disagreements(){return wrong;}
    public synchronized String lastConfirmed(){return previousConfirmed;}
    public synchronized boolean trainedEnough(){return confirmed>=BOOTSTRAP_CONFIRMATIONS;}
}
