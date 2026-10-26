# GLASS UNISON/0.1 — Typed AST Continuity, Portable Swift, and Market I/O

**Commission:** glass.unison-005 · 26 October 2026 · User-directed product name: **GLASS**.  
**Status:** implemented first deterministic source-to-syntax-IR pipeline, portable Swift pure-operation library, Swift/Linux read-only web server, responsive web console, synthetic market-event ranking, reversible Unibet codebook. **Not** an operating system, universal transpiler, general iOS/Android emulator, broker connection, or deployed always-on agent.

## 1. Unison equation

A *GLASS Unison instance* consists of a source-attested graph and a collection of typed projections:

\[
\mathfrak U = (S, A, P, T, I, K, R, W),\qquad
\Phi_{\mathfrak U}: S \to (A,P,T,I,K,R,W),
\]

- `S`: original immutable source bytes, language profile, version, source SHA-256.
- `A`: *real* native syntax AST from a parser and its parentage, including source spans when available.
- `P`: prefix trie over selected source identifiers; not a replacement for the AST.
- `T`: typed transformations with inputs, effects, guards and refusal conditions.
- `I`: lower-level intermediate forms (typed IR / CFG / LLVM IR / bytecode / metadata) with **independent fidelity status**.
- `K`: clock-bearing events and causality: `(epoch, sequence, logical_tick, origin, inputs, outputs)`.
- `R`: executable runtime capability, ABI, target, trust and compatibility evidence.
- `W`: observations, fixtures, proof obligations, negative results and provenance.

Only `A`, `P`, elementary pure `T`, a finite `K`, and demo `R` are implemented in this version; the general `I` and a whole-device `W` are open. A graph can encode candidates for semantic correspondences, but *identical node names do not imply observationally equivalent SDK behavior*. An AST is syntax. A CFG is control flow. SSA is data-flow form. A token trie indexes spellings. They become connected through **explicitly typed correspondence edges**, not by asserting they are one tree.

To preserve the principles from Encycled Calculus, a node may have a location and a time-bearing annotation, but syntax parse alone carries **no runtime clock observations**. Repeated analysis should not claim it has watched unexecuted functions.

## 2. Native parser operators and real boundaries

| Source grammar | Implementation in v0.1 | Witness and limit |
|---|---|---|
| Swift 6 | Local `swiftc -frontend -dump-parse` | Swift compiler's parser text; no typechecking or execution |
| SwiftUI | Same parser | `import SwiftUI` recognized as platform dependency; no UIKit/SwiftUI runtime translated |
| TypeScript / JavaScript | Actual TypeScript compiler syntax tree | `ts.createSourceFile`; preserves AST parentage; no `eval()` or user JS execution |
| Android Java | JDK `JavacTask.parse` compiler tree; source-only | No Android SDK typing or ART runtime invocation |
| HTML | Python `html.parser` | HTML parse **events**, not a browser's error-corrected DOM/CSS layout tree |
| Python strategies | CPython standard `ast.parse` | No execution/import of source code |
| Kotlin | Explicitly unsupported until Tree-sitter / Kotlin compiler grammar imported | No fake AST or inferred Android API behavior |
| C/C++/LLVM IR | Planned Clang/LLVM source and MLIR adapters | No claim of recovered binary source code |
| Android DEX/ART, iOS Mach-O, PE/DLL | Prior GLASS binary header classification is reusable by source-linked adapter | Headers and method symbols are not full behavioral ASTs |

Each source is bounded to 32 KiB and 640 nodes (this is a research fixture, not a full production parser). Parser subprocesses have timeouts. Source/AST versions and exact SHA-256 identities stay separate. A local Swift compiler parse does not execute Swift source. The actual parse-dump contains source path metadata from a temporary file; this is a parsing witness and not a standardized SwiftSyntax tree. For production, **SwiftSyntax** is the preferred source-accurate Swift grammar layer, and **Tree-sitter** provides a multi-language incremental parser family. Both should be pinned, licensed and conformance-tested independently before substitution.

## 3. Cross-target runtime and pixel control

**Swift language portability is real:** Swift runs on Linux and offers official SDKs for Android and WebAssembly. The portable `swift-core/` library uses Foundation and no Apple UI imports. It compiles and runs on Linux with Swift 6.2.1 and is a source target for the Android Swift SDK plus NDK toolchain. This unit does not possess an installed Android Swift SDK or device test.

An arbitrary iOS app cannot be repackaged by renaming `.ipa` into `.apk`: it may depend on UIKit, SwiftUI, Objective-C runtime, private Apple frameworks, entitlements, Mach-O APIs, signing, Metal, WebKit and particular device behavior. A **source-level compatibility build** can lower approved portable business logic from Swift to Android, and adapt supported UI semantics. It cannot promise pixel-identical or behaviorally identical iOS apps in general. A faithful iOS emulator is a separate large, platform- and licensing-constrained project.

The current Swift web server serves an actual website over localhost HTTP on Linux. The browser UI is HTML/CSS/JavaScript (not Swift rendered magically as HTML), and WebAssembly Swift compilation is an unimplemented but documented target. The `Runtime Matrix` contains static side-by-side *Android-style and iOS-style design projections*, **not OS desktops**. Pixel-level control of GLASS's own Canvas output is feasible; physical device screen capture requires explicit OS permission as documented by GLASS Browser. 

## 4. Unibet, glyphs and semantic compression

A glyph is a **registry reference**, not an arbitrary amount of data. `compiler/unibet.py` picks repeated AST node kinds, assigns each a private-use code point (U+E000 onward), and records the exact ordered glyph sequence, codebook, SHA-256 digests and byte-size accounting. The generated `public/data/unibet.json` round-trips precisely to its AST-kind sequence when its codebook travels with it. It does **not** reconstruct original source code, which remains in separate custody. This is a typed structural codebook, not lossless compression of an arbitrarily large codebase into one character.

Any apparent compression is reported together with **full codebook and metadata size**, and compared to reference DEFLATE over the same canonical token sequence. Unicode private-use characters do not supply new standard glyphs: display requires a font, so the web UI renders portable hex IDs and descriptive labels. SHA-256 is a cryptographic digest, not an invertible codec and not evidence of unique meaning.

**QITṬ** letter registers, Latin transliterations, Greek, scripts with diacritics, and owner-named letter operators can be declared as additional typed codebooks. Display glyph normalization and semantic equivalence must not be conflated with numeric registry weights. The existing GLASS/QITṬ sources are retained unchanged.

## 5. Market I/O — observed source or simulated events

The user requests event universes across stocks and crypto, event-trigger signals, a language like Pine Script, and selection of the most rapidly changing instruments. `server/main.swift` contains an actual native Swift deterministic synthetic event stream with 768 logical ticks and eight fictional symbols, chosen by XorShift32. The `ORCA` symbol receives an explicit artificial event burst. The client plots generated sample prices and ranks **retrospective event concentration**, not future price performance.

For a symbol `s` and successive fixed windows of equal size, define the proposed bounded activity-surprise score:

\[
B_s = \frac{N_{\mathrm{recent}}(s) - N_{\mathrm{prior}}(s)}{\sqrt{\max(1,N_{\mathrm{prior}}(s))}}.
\]

The numerator counts sourced events; denominators are not statistical claims without a calibrated stochastic null model. A change in message ingestion, venue coverage, batching or feed dropouts can produce apparent bursts. Prices, volumes, and transaction/source metadata are different signals. A count of *observed trade or quote messages* cannot reveal the private clicks of all traders, and GLASS has no such account telemetry.

The strategy DSL is intentionally bounded and **signal-only**: `WHEN SMA(3) CROSS_ABOVE SMA(9) THEN SIGNAL BUY`. It parses to typed IR, computes pure indicators on supplied price sequences and cannot place orders. TradingView's Pine language is not bundled or assumed open source. Choose **QuantConnect LEAN** as the primary open-source complex multi-market trading engine (Apache-2.0; Python/C# strategy models); **Freqtrade** is another open-source crypto-bot research candidate, with its own license. An adapter must pin its code version, data rights, broker/auth boundary, event and strategy schemas, then run independent compatibility tests. No trades are routed by this project.

**Charting:** TradingView **Lightweight Charts** is Apache-2.0 and can be added as an optional rendering adapter with its attribution requirements. The richer Advanced Charts and Trading Platform libraries are not open source. Current GLASS ships a self-authored Canvas2D fallback with no third-party charts bundled.

## 6. Finite generator-of-generators, replay and always-on execution

`swift-core` contains a finite `GeneratorRecipe`, `GeneratorFactory`, `PureMachine` and exact event replay. The initial operators are `IDENTITY`, `INCREMENT`, `SIGN` over bounded signed integers. A generated recipe is a **typed admitted function**, not untrusted code compiled from text. Unsupported operations and overflowing arithmetic are refused without partial mutation. The GLASS AST generator compiles **projections** from pinned source fixture files.

`tools/watch_unison.py` offers an **opt-in source-change loop** with a bounded polling contract. Successful recompilation writes an append-only logical revision entry with parent-hash, source hash and result hash. It does not claim global trust anchoring or that the process survives power loss. Sample systemd path/service files are included but not installed. Continuous background work requires an explicitly running host, platform account, audit and deployment; neither ChatGPT nor an idle web tab is implicitly a permanent job worker.

`SCOPE → SOURCE_PIN → PARSE → ADMIT → LOWER → GENERATE → TEST → TRACE → REVIEW → PUBLISH`. A generator can propose a recipe; only admitted effect boundaries operate the OS or broker. Library import is license/profile checked. An optional LLM may propose IR but cannot grant itself authority or scientific proof.

## 7. Acceptance gates and next commissioning frontier

**Implemented and tested on this host:** Swift/Linux server, Swift 6.2.1 portable library, Python/HTML/TypeScript/Swift/Android Java source parsers, Unibet AST-kind codebook, finite strategy DSL, deterministic synthetic event rankings, browser frontend preview with responsive screenshots, journal generator logic. Actual test outcomes and tool versions are recorded in `evidence/host.json`.

**Not implemented or certified:** arbitrary SwiftUI/UIKit execution on Android, native iOS desktop, complete source-to-binary universal AST reconstruction, Swift WebAssembly frontend binary, actual market feed, Pine language interpreter, full LEAN integration, Android IPA or APK repackaging, a self-running permanent agent, global O(N) asymptotic breakthrough, algorithmic theorem discovery, or a P = NP proof.

Future bounded work: Tree-sitter Kotlin and C++ adapter with pin; SwiftSyntax rather than compiler dump for rich source spans; Clang/LLVM intermediate representation edges; a source-level Swift Android `UnisonCore` build and JNI bridge; SwiftWasm from official SDK; append-only data-feed adapters for licensed market sources; measured scalability (throughput, dropped events, memory) and rigorous holdout benchmarking; full device integration with GLASS Browser.

## 8. Confirmed technology source references (capability lookup, not theory validation)

- Official [Swift SDK for Android](https://www.swift.org/documentation/articles/swift-sdk-for-android-getting-started.html), [Swift WebAssembly guide](https://docs.swift.org/latest/documentation/wasmguide/), and [Swift on Server](https://www.swift.org/documentation/server/).
- [SwiftSyntax](https://github.com/swiftlang/swift-syntax) for Swift source-accurate syntax; [Tree-sitter](https://github.com/tree-sitter/tree-sitter) grammars for multiple languages.
- [QuantConnect LEAN](https://github.com/QuantConnect/Lean), Apache-2.0 event-driven engine with Python and C# strategies.
- [TradingView Lightweight Charts](https://github.com/tradingview/lightweight-charts), Apache-2.0 with attribution notice; other TradingView chart products remain proprietary.
- [Freqtrade documentation](https://www.freqtrade.io/en/stable/), Python trading strategies with dry-run/backtest support.

**Commercialization:** GLASS Unison code is an owner-directed project. Upstream licenses and source attribution survive every adapter, and an exported product must address parser/trading library licenses, legal market-data rights, API credentials, exchange rules, and security reviews before live operation.
