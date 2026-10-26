# GLASS Browser — Gecko / Unison v0.1 source

This is an Android browser shell built around **Mozilla GeckoView**, which includes its own Gecko HTML/CSS/JavaScript/layout engine. It is **not** Android System WebView. This repository does not yet contain a locally rebuilt Gecko engine; build the upstream renderer from Mozilla source for internal instrumentation.

Source: https://github.com/mozilla-firefox/firefox
GeckoView docs: https://firefox-source-docs.mozilla.org/mobile/android/geckoview/consumer/geckoview-quick-start.html

## Build requirements

Android Studio; Android SDK 35; CMake/NDK; Java 17; compatible Gradle 8.9 environment and published GeckoView artifact. Set the GeckoView dependency explicitly: `gradle :app:assembleDebug -PgeckoviewVersion=<published-version>`. Gradle wrapper is not packaged. The APK has **not yet been compiled or device-tested** here.

## Working source modules

- `app/src/main/java/dev/glass/browser/BrowserActivity.java`: GeckoView session bootstrap, URL/search input, local GLASS terminal `glass://help`, `glass://trace` and `glass://home`.
- `app/src/main/cpp/trace.cpp`: C++20 native append-only event journal with monotonic timestamp, cursor, fsync.
- `tools/unison_ast.py`: addressable 100,000-entry typed grammar product with reproducible AST digest.
- `tools/test_unison_ast.py`: cardinality, uniqueness, digest and arithmetic fixture checks (run `cd tools && python -m unittest -v`).

**Research integrity**: 100,000 syntactic combinations are not 100,000 proven independent semantic transformations or optimized generators. Ten operator semantics have finite integer fixtures; contexts/strategies/phases are descriptors pending lowering and validation. No screen-wide monitoring, third-party session replication, background control, binary translation, device instrumentation or new transport layer is implemented yet.

## Next implementation milestones

Hook Gecko parser/layout/style engine tracing through a forked source build; expose versioned trace event schemas; implement AST adapters over parsed DOM/CSS/JS and lowered Gecko representation with provenance; add differential executable tests and bounded generator discovery; connect native isolation and an authenticated Unison protocol; compile and test on Android arm64.
