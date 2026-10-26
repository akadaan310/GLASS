# ⟦ GLASS / UNISON / VITROMATON TERMINAL 0.1 ⟧

**Native first.** C++20 deterministic symbolic runtime + finite-state clock + real PTY shell, native pixel renderer, ANSI celestial terminal scene, and Android ARM64 NDK application. Built on the open-source Termux `terminal-view` and `terminal-emulator` libraries (Apache 2.0 exemptions of a GPLv3 app).

## Native CLI, on Linux or Termux

```sh
cmake -S . -B build -G Ninja
cmake --build build
ctest --test-dir build --output-on-failure
./build/glass-terminal
```

Termux installation: `pkg install clang cmake ninja` and compile inside your Termux home. No Android root required. Use an actual PTY (`termux`) for the immersive view; test with `./build/glass-terminal --eval 'xor 3 1'` when piping or scripting.

## English and Unison instructions

- `xor 0xff 0x34`, `and 3 1`, `rot 1 4`, `energy 0 15`
- `matrix` or `multiply matrices` — exact 10×10 row/column product, 1000 MAC trace steps
- `tape row`, `tape column`, `tape diagonal`, `tape anti-diagonal`, `tape perimeter`, `tape snake`
- `space 6`, `move 0 2`, `spin 0 1 1.57` — typed ℝⁿ coordinates and rotation
- `clock`, `stop clock`, `resume clock`, `trace`, `protocol`, `arabic alphabet`
- `⟦Λ:binary ⊗ Γ:xor(1,0) ⊗ τ:1⟧`
- `:shell` — enter an **actual interactive OS shell** through your existing PTY, `exit` returns to GLASS
- `:run 'command'` — explicitly invoke the user's local shell once; don't hand untrusted suggestions directly to a shell
- `:help` — introspect available grammar; `exit` — close GLASS

### Android APK

The `android/` project provides a native C++/JNI full-screen scene, keyboard input, and Termux's real PTY terminal component. Type `:shell` to switch into an embedded Android `/system/bin/sh` session; press Back to return. No access to arbitrary private app sessions, rooted features, or system-wide telemetry. The native field is rasterized in `core/pixels.cpp`; Android canvas overlays typed text/glyphs and Termux handles terminal semantics. This architecture doesn't require browser HTML or WebView.

A GitHub Actions workflow builds an ARM64 debug APK on pushes to `main`. **Only download the APK after the Actions build completes successfully.** Android APK signing in CI uses an automatically generated *debug key*, not a Play Store release key. Packaging is not equivalent to device-level execution testing.

## Exact current contract

- Every controlled **32-bit** Boolean gate is O(1); computing N arbitrary pixels requires at least Ω(N) outputs.
- `τ` is a discrete logical event clock with independently running visual frames. `halt` freezes the generator progression, not the physical device or wall clock.
- Switching `energy` is a **proxy for bit flips**, not device heat, a quantum measurement or a thermodynamic model.
- SHA-256 event chaining allows replay-integrity checks but is not an authenticated signature unless its root is signed externally.
- N-dimensional rotation in specified coordinate planes preserves Euclidean norm, without suggesting exact physical n-dimensional quantum simulation.
- Multilingual fallback categorizes Unicode code points without inventing semantics; CLDR/ICU full grapheme normalization is a follow-up.
- Autonomous letter events are emitted every 24 display frames while the local scene is running, bounded at 10k in-memory event objects; append-only journal file may grow without rotation in v0.1.
- The universe is a **synthetic** celestial scene; actual Gaia positions and genuine astronomical telemetry require sourced catalog adapters.
- The SDK is not an embedded ChatGPT model or autonomous coding agent. Further agent connection requires an authorized API and declared transport/permissions.

## Research succession

1. Lift the original PHANTOM / PolyIA generators through verified adapters rather than copy their results.
2. Add external PURL resource manifests, seURL transitions, ACSP checkpoint handoff over authenticated transport.
3. Establish AST generator property tests and complete normalized Unicode registry.
4. NDK device profiler: actual frame timings, pixel diff counts, battery/temperature readings only with permission and supported OS APIs.
5. Production artifact signing, UI accessibility verification, performance/backpressure, cross-client state replay, and secure authorized agent transport.

Source provenance: https://github.com/termux/termux-app (Terminal emulator and TerminalView libraries Apache-2.0; entire Termux app GPLv3-only). Respect redistribution/attribution and actual library versions.
