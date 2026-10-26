package org.glass.unison;

import android.content.ContentResolver;
import android.net.Uri;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.util.function.Consumer;

/** Manual, read-only 16 kHz mono PCM16 RIFF/WAV analysis.
 * No sound output, no implicit media playback, no network.
 * Broader codecs need an explicit Android MediaCodec adapter with tests.
 */
public final class WavImport {
    private WavImport(){}
    private static int u16(ByteBuffer b,int off){return b.getShort(off)&0xffff;}
    private static long u32(ByteBuffer b,int off){return Integer.toUnsignedLong(b.getInt(off));}
    private static String fourcc(byte[] data,int off){
        return new String(data,off,4,StandardCharsets.US_ASCII);
    }
    public static int analyze(ContentResolver resolver, Uri uri, TraceMath math,
                              Consumer<TraceMath.Frame> sink) throws Exception {
        if(resolver==null||uri==null||math==null||sink==null)
            throw new IllegalArgumentException("Invalid WAV read arguments");
        ByteArrayOutputStream data=new ByteArrayOutputStream();
        try(InputStream stream=resolver.openInputStream(uri)){
            if(stream==null)throw new IOException("Document not accessible");
            byte[] chunk=new byte[16384];int n;
            while((n=stream.read(chunk))!=-1){
                if(data.size()+n>5_000_000)throw new IOException("WAV file exceeds 5MB read budget");
                data.write(chunk,0,n);
            }
        }
        byte[] raw=data.toByteArray();
        if(raw.length<44||!"RIFF".equals(fourcc(raw,0))||!"WAVE".equals(fourcc(raw,8)))
            throw new IOException("Only uncompressed RIFF/WAV is supported");
        ByteBuffer b=ByteBuffer.wrap(raw).order(ByteOrder.LITTLE_ENDIAN);
        if(u32(b,4)+8L>raw.length)throw new IOException("WAV container truncated");
        int channels=0,bits=0,rate=0,format=0,offset=-1,length=0;
        for(int pos=12;pos+8<=raw.length;){
            String type=fourcc(raw,pos);
            long lengthLong=u32(b,pos+4);
            if(lengthLong>5_000_000L||pos+8L+lengthLong>raw.length)
                throw new IOException("Invalid WAV chunk length");
            int n=(int)lengthLong;
            int start=pos+8;
            if("fmt ".equals(type)){
                if(n<16)throw new IOException("Invalid WAV format chunk");
                format=u16(b,start);channels=u16(b,start+2);
                rate=b.getInt(start+4);bits=u16(b,start+14);
            }else if("data".equals(type)){
                offset=start;length=n;
            }
            pos=start+n+(n&1);
        }
        if(format!=1||channels!=1||rate!=TraceMath.SAMPLE_RATE||bits!=16)
            throw new IOException("Require PCM16 mono at 16 kHz; use explicit conversion for other codecs");
        if(offset<0||length<256||length%2!=0)throw new IOException("Missing or invalid PCM data");
        int frames=0;short[] samples=new short[1024];
        for(int pos=offset;pos<offset+length;){
            int take=Math.min(samples.length,(offset+length-pos)/2);
            for(int i=0;i<take;i++)samples[i]=b.getShort(pos+2*i);
            pos+=2*take;
            if(take<128)break;
            sink.accept(math.process(samples,take));
            frames++;
        }
        return frames;
    }
}
