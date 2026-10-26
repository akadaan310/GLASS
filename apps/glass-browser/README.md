# GLASS Native Browser · Terminal Protocol · Screen Continuity / 0.1

Native Android browser shell and scientific experiment, **not** a browser that has automatic access to someone else's screen or a new Internet transport. Its own UI is Java using Android's Chromium-derived system WebView; its finite event machine, Arabic terminal grammar and binary header inspection are C++20/NDK; a pure sample shared-object gate is C11. A single visible Android MediaProjection foreground service samples the device's screen **only while the user has approved that session**.

## What works in the reference source

- First launch displays the capture disclosure. **No capture starts until the user confirms Android's system consent dialog.** The browser functions without capture.
- Browser navigation history is a **local-origin event** (not a whole-device Accessibility log). Directly typed `glass://terminal/v1/state` returns local state; `glass://terminal/v1/spell?word=%D9%82%D8%B7` returns a source-preserving QITṬ/14+14 signature of قط.
- Device projection samples a **maximum of one JPEG per second**, retains up to 120 private images and appends a SHA-256 linked receipt. This is *sampled continuity*, **not every display frame or every tap across the OS**.
- Stop button/notification action ends projection; MediaProjection callbacks mark `CAPTURE_GAP` when Android stops it. Restarting capture requires a new consent token on Android 14+.
- Private browser Activity runs in a separate Android process and calls `WebView.setDataDirectorySuffix()` before WebView creation to segregate WebView storage. Its cookies/storage are cleared on entry/normal activity teardown. No remote cookies are duplicated, and a process crash may bypass normal teardown—secure ephemeral profile lifecycle remains a separate production gate.
- GLASS native C++ ledger records typed events, logical epochs, monotonic timestamps and bounded event retention. Java app-private JSONL holds a SHA-256 hash chain and JPEG receipts. A local/offline `verify_ledger.py` validates the hash links after the owner exports them. This chain is **not signed, not encrypted by GLASS itself, and not a proof of completeness**.
- A packaged C11 `libglass_gate_bit.so` exposes a versioned gate descriptor. A focused host harness loads it with `dlopen` and rejects incorrect buffers. **No arbitrary downloaded SO, PE/DLL or EXE is executed.** Small binary header inspection reports likely formats without loading them.

## Development and APK

From the project root:

```sh
bash tools/test_host.sh
cd android
# Require Android SDK platform 36, Android build tools, NDK 27.2.12479018,
# CMake 3.22.1, Gradle 8.11.1, JDK 17 and network dependencies available.
gradle :app:assembleDebug --no-daemon
# APK: android/app/build/outputs/apk/debug/app-debug.apk
```

Debug APKs are automatically debug-signed **by the building developer environment**; they are not release-signed. Never distribute a release without reviewing provenance, licenses, screen-capture privacy and a production signing policy. Release signing keys are private and must not be committed.

This container does **not** have the Android SDK/NDK/Gradle toolchain, and its network cannot resolve the official Android download server. No GLASS APK was compiled or signed in the local container. The checked native files are host-compiled, not Android-run. The GitHub workflow may provide an Android build attempt on a suitable runner; status must be checked from actual logs before claiming APK availability.

## Namespaced terminal operator

`glass://terminal/v1/` is an internal address grammar that resolves typed objects in GLASS. It is not publicly routable DNS/TLS and does not replace HTTPS. The *only* read-only commands in this source increment are:

```
glass://terminal/v1/state
glass://terminal/v1/spell?word=<percent-encoded UTF-8 single Arabic word>
```

These are admitted only when typed into the GLASS address bar; web pages cannot invoke privileged native operators. All conventional website navigation is HTTPS with safe browsing enforced by the device WebView provider. There is no embedded remote server, bearer token or AI-access endpoint.

## Research boundaries and open source reuse

- **Choose GeckoView / Firefox for a browser-grade self-contained engine.** Its source is in Mozilla Central, and it supports session context IDs and private mode; GLASS/0.1 uses the already provisioned Chromium WebView to keep the native first-launch shell small. Upgrading to GeckoView requires a pinned audited dependency, a tested engine adapter and a separately packaged APK. No GeckoView library is bundled here.
- **Choose Fennec F-Droid** as an independently installable open-source Android browser while GLASS has no built APK. It is not a GLASS control endpoint; signing in to a website in Fennec does not authorize GLASS or ChatGPT to clone its session.
- **Static binary inspection:** LIEF can parse ELF/PE/Mach-O, Android DEX/ART and debugging info. It is a proposed independent parser adapter, not bundled or compiled here. Windows executables and DLLs require CPU ABI and OS compatibility layers; headers alone do not make them runnable. Native Android packaged `.so` files are separate from Windows DLLs.
- **All-device continuity:** Android 16 requires explicit consent every projection session, a visible notification, and honors screen-lock/secure-window restrictions. Android apps cannot silently reestablish projection at boot. Screen frames do not reveal physical transistor state, every touch in other apps, or unobserved intervals.
- **Security:** no source code may capture passwords/keystrokes via hidden accessibility, forward images off-device, secretly bypass `FLAG_SECURE`, or reuse one-shot MediaProjection tokens. Remote AI operation is reserved for a later paired-capability protocol with explicit grants, revocation and on-device indicators.

References: [Android MediaProjection](https://developer.android.com/media/grow/media-projection) · [Foreground service requirements](https://developer.android.com/develop/background-work/services/fgs/service-types) · [Chromium Android WebView architecture](https://chromium.googlesource.com/chromium/src/+/main/android_webview/docs/architecture.md) · [GeckoView](https://mozilla.github.io/geckoview/) · [Fennec F-Droid](https://f-droid.org/packages/org.mozilla.fennec_fdroid/) · [LIEF](https://github.com/lief-project/LIEF).
