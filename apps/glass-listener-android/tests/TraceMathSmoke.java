package org.glass.unison;

/** No Android dependencies: local DSP and clock smoke tests on the JVM.
 * This proves numerical/tape logic only, not actual microphone accuracy,
 * Quranic phoneme recognition, Android device launch or ASR service support.
 */
public final class TraceMathSmoke {
    private static void demand(boolean value,String why) {
        if(!value)throw new AssertionError(why);
    }
    private static short[] wave(double amplitude,double frequency){
        short[] p=new short[1024];
        for(int i=0;i<p.length;i++)p[i]=(short)Math.round(
            amplitude*32767*Math.sin(2*Math.PI*frequency*i/16000.0));
        return p;
    }
    public static void main(String[] unused) {
        TraceMath math=new TraceMath();
        TraceMath.Frame quiet=math.process(new short[1024],1024);
        demand(!quiet.voiced,"Silence marked as voice");
        demand(quiet.rms==0,"Zero vector should have zero RMS");
        TraceMath.Frame tone=math.process(wave(.25,220),1024);
        demand(tone.voiced,"Strong periodic tone must exceed noise threshold");
        demand(tone.rms>.15 && tone.rms<.20,"RMS outside expected sinusoidal band");
        demand(tone.centroidHz>0,"Centroid missing for nonzero periodic signal");
        demand(tone.peak>.20 && tone.peak<.26,"Peak wrong");
        LanguageClock lang=new LanguageClock();
        for(int j=0;j<9;j++)lang.onFrame(math.process(wave(.25,220),1024));
        LanguageClock.Candidate candidate=null;
        for(int j=0;j<5;j++)candidate=lang.onFrame(math.process(new short[1024],1024));
        demand(candidate!=null,"No phrase was generated");
        demand(candidate.requiresConfirmation,"First 30 candidates require confirmation");
        lang.confirm("ar");
        demand(lang.confirmations()==1,"Confirmation counter not persisted");
        demand("ar".equals(lang.lastConfirmed()),"Confirmed language incorrect");
        LanguageClock.Candidate next=lang.proposeFromOnDevice("en",.80);
        demand(next.possibleSwitch,"English vs Arabic change was not observed");
        lang.confirm("en");
        demand(lang.switches()==1,"Confirmed switch was not counted");
        demand(lang.confirmations()==2,"Confirmation count should be 2");
        demand(lang.threshold()>=.70 && lang.threshold()<=.88,"Bad adaptive threshold");
        System.out.println("GLASS DSP and language-clock smoke: PASSED (synthetic only)");
    }
}
