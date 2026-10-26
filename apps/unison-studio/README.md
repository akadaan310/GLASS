# GLASS UNISON 005 — Swift runtime, unified ASTs and synthetic Market I/O

Runnable artifact accompanying the GLASS [UNISON SCIENCE](docs/UNISON_SCIENCE.md) commission. **The backend really compiles under Swift on Linux**; the UI is HTML/CSS/JavaScript served by Swift. The SwiftUI/Android/iOS desktops are **adapter models** rather than mobile OS emulators.

## Run locally

```sh
# from apps/unison-studio/
python3 compiler/build_demo.py             # 6 genuine syntax-parser fixtures -> public/data/
swiftc -O -o server/unison-server server/main.swift
./server/unison-server 8765                # localhost GET-only Swift HTTP server
# Browse http://127.0.0.1:8765/
```

Other checks:

```sh
PYTHONPATH=. python3 -m unittest discover -s tests -v
(cd swift-core && swift test --jobs 2)
node --check public/app.js
python3 tools/watch_unison.py                # one regeneration if input changed
python3 tools/watch_unison.py --watch --max-polls 120 --interval 2
```

A Swift 6.2+ toolchain, JDK 17+, Python 3.10+, Node + installed TypeScript compiler are needed. The TypeScript parser uses `require('typescript')`; you may run `npm install --no-save typescript@5.8.3` if missing. The Swift parser uses local `swiftc -frontend -dump-parse`; Swift source is **parsed, never executed** by the Python converter.

On macOS/Linux, Swift backend port **8765** listens on `127.0.0.1` only. It has read-only GET endpoints `/api/status`, `/api/market?seed=...` and a fixed asset allowlist. It is a small experimental server, not a production TLS endpoint or Internet deployment. The UI can be opened as static files but then displays **offline illustrative fallback**, not the verified source ASTs.

## Implemented modes

| Mode | Current behavior | Nonclaim |
|---|---|---|
| AST Universe | Genuine Swift, SwiftUI syntax, Android Java/JavacTask, HTML parser, TypeScript and Python AST fixtures; token-prefix summary; node selection, IR export and pure recipe generation | No arbitrary code execution or iOS runtime translation |
| Market I/O | Swift 768-tick synthetic event stream, 8 fictitious assets, retrospective burst ranking and Canvas trace | Not stock quotes, exchange trade capture, price prediction or broker orders |
| Unibet | Hash-verified reversible AST-kind codebook mapped to Unicode PUA IDs, reports full size | Not source-code reconstruction, quantum compression or cryptographic hash inversion |
| Runtime Matrix | Swift/Linux host, official Android/WebAssembly SDK targets, Apple-framework blocker and visual desktop mockups | No released Swift/Android APK and no iOS OS emulator |

## Sources and legal boundaries

No proprietary SDK implementation is copied. Official Swift SDK, SwiftSyntax and Tree-sitter are *adapter references*. QuantConnect LEAN and TradingView Lightweight Charts are **not embedded** in this package; integrating them requires pinned versions, attribution, license compliance and conformance checks. This prototype emits no trades and needs no credentials.

`public/data/` contains small syntactic fixtures derived from the `examples/` files. The generator does not read private files, source code outside its allowlist or any GitHub credentials. The source watcher is **opt-in**, bounded and not installed as an always-on service. `systemd` units are examples with assumed service-user and filesystem paths; review before installing.

## Status

Consult `evidence/host.json` for executed checks. Only a verified build/package or host deployment receipt may be labeled live; a GitHub commit by itself proves source publication, not Swift Android runtime capability.
