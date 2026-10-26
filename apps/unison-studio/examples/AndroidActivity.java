package org.glass;
import android.app.Activity;
import android.os.Bundle;
public final class GlassActivity extends Activity {
    private int logicalTick = 0;
    @Override public void onCreate(Bundle bundle) {
        super.onCreate(bundle);
        logicalTick += 1;
    }
}
