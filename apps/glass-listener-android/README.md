# GLASS UNISON Live — standalone Android listening APK source

**First native phone implementation of the UNISON local I/O calculus**, additive to GLASS. It is a new, separate Android application with package name **org.glass.unison** and its own development signing certificate. It is NOT a replacement for or an update to a previously installed SURFACE recovery APK.

Read [the formal calculus](../../docs/UNISON_LIVE_CALCULUS.md) and [the source-linked 33-trace manifest](../../atlas/unison-live-traces-v0.1.json).

## On first launch

- **Microphone OFF**. No capture starts until the user taps Listen PCM or Offline ASR.
- **Network streaming OFF**. No event goes to the internet until the user separately configures a protected HTTPS endpoint, room and private write capability.
- **No playback** at launch or on microphone activation. Analyze WAV is an explicit *no-sound* file probe.
- An onscreen indicator reports microphone/stream state; both are turned off in Activity.onPause().
- No service runs in the background. No persistent voice buffer, transcript upload, voiceprint or microphone remote access.
- On-device Android SpeechRecognizer is optional, only if the OS reports an installed offline recognition service. No cloud recognizer fallback and no guarantee its downloaded models include Arabic and English.

## Live controls

**Listen PCM**: 16 kHz mono PCM16 AudioRecord, 1024-sample frames. Updates the in-app Canvas ink rings, RMS envelope, Goertzel spectral flux/energy, pitch proxy and speech/pause candidate trace. These numeric features are not MUQRI's trained 40ms CTC phoneme or Tajwid classifier.

**Offline ASR**: a separate capture mode. Uses installed Android on-device SpeechRecognizer; on Android API 34+ it requests Arabic/English language detection and switching if the recognizer supports these models. The OS's reported RMS hint drives the ink display; do not present that as the PCM signal.

**Arabic ✓ / English ✓ / Other ✓**: first 30 phrase confirmations calibrate a language clock, count *confirmed switches*, and retain disagreements. A weak hint is not proof of language. State can be UNKNOWN and ask again.

**Analyze WAV**: user selects a read-only 16 kHz mono PCM16 RIFF/WAV document, maximum 5 MB, which is analyzed but NEVER played. Other codecs deliberately refuse rather than pretending to decode.

**Event stream**: user enters a HTTPS URL such as their own Vercel /api/glass/publish, a protected room ID and a 24+-character write token. The stream contains at most 1 aggregated numeric audio trace/sec plus confirmed language/session events. It never emits PCM, text or voiceprints. A bounded queue drops data under sustained transport failure.

## Build APK with official Android SDK

If an installed Android SDK is available (Python 3.11+, Java21, SDK platform35 and build-tools35):

    python3 apps/glass-listener-android/tools/build_apk.py --sdk-root "$ANDROID_HOME"

Expected output **after a successful build only**:

    apps/glass-listener-android/build/Glass-UNISON-Live.apk
    apps/glass-listener-android/build/GLASS_APK_RECEIPT.json

The temporary debug signing key stays under the ignored build directory. Its identity is NOT the old SURFACE APK signing identity, and a new fresh key cannot update a prior APK. Rebuilds for continuous use need a privately secured durable production signing key outside Git.

The same build is configured in [.github/workflows/glass-live-apk.yml](../../.github/workflows/glass-live-apk.yml), and will upload a GitHub Actions artifact when runner/build success is actually observed. **Status for this commission:** GitHub Actions failed before runner assignment, and the ChatGPT container lacks the Android SDK. Do not claim this is a presently downloadable or verified APK until a successful run and hash exist.

The source includes a pure-JVM synthetic numerical test at tests/TraceMathSmoke.java; neither that test nor the Android app launch is substituted for real voice/phone measurements. A Java-only app does not embed an extra Python webserver, because low-latency local DSP needs none.

## Related runtime

- Local source: src/org/glass/unison/*.java.
- Protocol: [NetGovComEduGovOrgEduGovComNet](https://github.com/akadaan310/NetGovComEduGovOrgEduGovComNet), private event ingestion + room SSE, publicly visible synthetic terminal.
- Model-based recitation engine: [MUQRI](https://github.com/akadaan310/muqri) remains canonical for Hafs text, phoneme alignment and Tajwid.
- Physics/ink source: [SURFACE](https://github.com/akadaan310/SURFACE) remains canonical for native C++ physics, field measurements and quantum-reference boundaries. This GLASS standalone APK uses Android Canvas to display admitted trace features before an Android/device-tested bridge to SURFACE's CPU raster.

## Acceptance stages

1. Pure Java DSP numerical smoke → result and compiler version logged.
2. Android SDK compile/D8/aapt2/zipalign/apksigner → artifact hash and signature.
3. Real Android microphone permission/session test → PCM frame and stop proof.
4. Installed on-device recognizer Arabic/English test (or explicit unsupported report).
5. 30 real human-confirmation switching experiment, false prompts and abstention rate.
6. HTTPS post/replay/ACL/event-no-PCM test against configured Postgres/Vercel.
7. Crash/no-autoplay/background stop/OS rotation and battery profile.
8. Native SURFACE renderer admission separately, without overwriting historical evidence.

**No proof of perfect language detection, Qur'anic meaning from numbers, or always-on cosmic/quantum sensing is claimed.**
