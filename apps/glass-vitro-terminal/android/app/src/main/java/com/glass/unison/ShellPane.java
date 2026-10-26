package com.glass.unison;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.view.View;
import java.util.ArrayDeque;

/** True PTY data, rendered with a deliberately bounded ANSI terminal subset. */
final class ShellPane extends View {
    interface ResizeHandler { void resize(int cols,int rows); }
    private final ArrayDeque<String> lines=new ArrayDeque<>();
    private final StringBuilder line=new StringBuilder(),csi=new StringBuilder();
    private final Paint ink=new Paint(3),shade=new Paint();
    private String typing="";
    private ResizeHandler sizeHandler;
    private int escape=0,cols=0,rows=0;
    ShellPane(Context ctx){
        super(ctx);ink.setTypeface(Typeface.MONOSPACE);
        ink.setTextSize(14*getResources().getDisplayMetrics().scaledDensity);
        ink.setColor(Color.rgb(169,245,229));
        shade.setColor(Color.argb(226,2,10,19));
        setContentDescription("GLASS PTY terminal output. Tap to type and keyboard Go to submit.");
    }
    void setResizeHandler(ResizeHandler h){sizeHandler=h;}
    void setPendingInput(String text){typing=text;invalidate();}
    void append(String text){
        for(int i=0;i<text.length();i++){
            char c=text.charAt(i);
            if(escape==1){if(c=='['){escape=2;csi.setLength(0);}else escape=0;continue;}
            if(escape==2){
                if(c>=0x40&&c<=0x7e){
                    if(c=='J'&&csi.toString().contains("2")){lines.clear();line.setLength(0);}
                    else if(c=='K')line.setLength(0);
                    escape=0;
                }else if(csi.length()<48)csi.append(c);else escape=0;
                continue;
            }
            if(c==27){escape=1;continue;}
            if(c=='\r'){line.setLength(0);continue;}
            if(c=='\n'){push();continue;}
            if(c=='\b'||c==127){if(line.length()>0)line.deleteCharAt(line.length()-1);continue;}
            if(c=='\t'){line.append("    ");continue;}
            if(c>=32)line.append(c);
            if(line.length()>8192)push();
        }
        invalidate();
    }
    private void push(){lines.addLast(line.toString());line.setLength(0);while(lines.size()>1500)lines.removeFirst();}
    @Override protected void onSizeChanged(int w,int h,int ow,int oh){
        super.onSizeChanged(w,h,ow,oh);
        int nc=Math.max(20,(int)((w-24)/ink.measureText("M")));
        int nr=Math.max(8,(int)((h-90)/(ink.getTextSize()*1.35f)));
        if(sizeHandler!=null&&(nc!=cols||nr!=rows)){cols=nc;rows=nr;sizeHandler.resize(cols,rows);}
    }
    private static String tail(String s,int n){return s.length()<=n?s:s.substring(s.length()-Math.max(0,n));}
    @Override protected void onDraw(Canvas canvas){
        canvas.drawRect(0,0,getWidth(),getHeight(),shade);
        float h=ink.getTextSize()*1.35f,y=ink.getTextSize()+20;
        int visible=Math.max(1,(int)((getHeight()-90)/h));
        int col=Math.max(20,(int)((getWidth()-24)/ink.measureText("M")));
        int skip=Math.max(0,lines.size()+1-visible),i=0;
        for(String row:lines){if(i++<skip)continue;canvas.drawText(tail(row,col),12,y,ink);y+=h;}
        canvas.drawText(tail(line.toString(),col),12,y,ink);
        ink.setColor(Color.rgb(79,218,196));
        canvas.drawText("⟐ "+tail(typing,Math.max(0,col-5))+"▏",12,getHeight()-30,ink);
        ink.setColor(Color.rgb(169,245,229));
    }
}
