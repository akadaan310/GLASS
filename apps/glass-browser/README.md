# GLASS Browser 0.1 — first executable Android browser source

Android Java WebView browser shell + C++20 NDK append-only trace library. This is a real embeddable browser using the installed Android System WebView; it is not yet a separately forked Chromium/Gecko engine.

## Build
Open this folder in Android Studio with Android SDK 35 and NDK/CMake installed, then assembleDebug, or use `gradle :app:assembleDebug` with a compatible Gradle 8.9 installation. A Gradle wrapper is not committed yet.

## v0.1 controls
URL/search omnibox; Go; back; forward; reload; home; add/close tabs; GLASS terminal commands (`glass://help`, `glass://trace`, `glass://tabs`, `glass://home`), local native C++ journal of browser events (JSONL). New sessions default to a blank page; no sound starts automatically.

## Limits
No system-wide screen acquisition; browser-scoped navigation events only. No remote takeover, Chrome session extraction, EXE runner, agent transport, cross-process profile isolation or native binary lifter yet. Never claim broader telemetry or executable support without end-to-end evidence. Do not expose traces via JavaScript. Never browse to untrusted URLs under file-access enabled settings. The local journal may contain sensitive visited URLs; it remains private to the APK.

## Follow-on
Browser engine abstraction (GeckoView); isolated profile processes; explicit capture consent; terminal to native executor with strong process isolation; packaged provenance and test receipts; opt-in Unison transport.
