# SON/0.1 — Four-lane programmable Unison address

## Formal object

An open-ended alphabet is represented as a **directed family of finite, versioned registries**, `Σ∞ = ⋃Σₙ`. Only a finite registered subset has executable operator semantics at any checkpoint. New symbols receive typed, versioned addresses; a glyph alone is not enough to reconstruct a codebase or prove a physical event.

GLASS represents one symbolic source program as:
`(source_utf8, syntax_AST, lexical_tape, operator_ids, matrix_projection, trace, provenance)`.

The SON levels are **UNISON** (source and its operators), **BISON** (canonical address plus source recovery witness), **TRISON** (source/tape/matrix with explicit loss), and **NISON** (a finite, bounded composition of those projections). The term infinite describes the ability to extend the address namespace, not infinite memory or instantaneous execution.

## Syntax and URL contract

A SON portable URL has form `https://glass.com/?son=s1.<base64url(UTF-8 canonical JSON)>`. Its only JSON fields are `lanes` (one to four ordered source expressions) and `v` (1), sorted in canonical serialization. No credential, cookie, authority or hidden effect is conferred by a URL.

Allowed search atoms: bare terms, quoted phrases, `site:`, `filetype:`, `after:`, `before:`, unary negation, `AND` (or adjacency), `OR`, and parentheses. The compiler emits a Google query projection, **not** exact external Boolean-provider semantics. Google Search documents several search operators; the Programmable Search API uses a query parameter named `q`. Provider ranking and query interpretation remain outside GLASS's control.

The first operator glyph registry is `TERM ◉; PHRASE ≡; AND ∧; OR ∨; NOT ¬; SITE ⌁; FILETYPE ▤; AFTER ⊳; BEFORE ⊲; OPEN ⟦; CLOSE ⟧`. These have separate synthetic associations with **eleven** Arabic QITṬ registers. The original 28-symbol Arabic numeric alphabet is immutable and continues as a distinct profile; attributing logical-op semantics to letters is a computational construction, not an ancient linguistic assertion.

## Ordered projections

Each lexical source record preserves `role, glyph, raw, value, char_span, byte_span, sha256, index`. The glyph projection preserves **operator order** but cannot recover arbitrary original words without tape/source sidebands.

A 4×4 binary projection takes the first four token UTF-8 strings and computes the low nibble of the XOR of their bytes. Rows without tokens are zero. An explicit perturbation toggles one matrix bit at `r = seed mod 4, c = floor(seed/4) mod 4`; the same XOR toggle restores it. The matrix is deliberately lossy.

The local clock log distinguishes `IO_INPUT_READ`, `AST_PARSED`, `TAPE_PROJECTED`, `MATRIX_PROJECTED`, `MATRIX_PERTURBED`, `QUANTUM_SIMULATED`, `SEARCH_PROVIDER_PROJECTION`, and `SELF_REVISION`. Quantum records arise from a **classically simulated ideal one-qubit gate sequence**, never a physical device or measurement. Self-revisions require explicit approval, preserve the parent digest and emit a new immutable child version.

Four programs can live under one SON address and run through a deterministic round-robin *logical* schedule. They are **not four unapproved concurrent Google requests**.

## Four admitted examples

```text
"Unison alphabet" site:github.com (compiler OR grammar) filetype:md
"mechanical computation" (clock OR timing) -advertisement after:2024-01-01
"ألف لام ميم" (لسان OR نحو) site:edu
"Maxwell equations" (field OR electromagnetic) filetype:pdf before:2026-01-01
```

## Product location and execution status

The typing-only, no-buttons terminal is at [GLASS SON](../apps/glass-oracle/son.html). The root Oracle [index](../apps/glass-oracle/index.html) now recognizes `?son=s1.` and dispatches to the local SON view. **Deployment at glass.com is unverified**. The standalone source-and-test package includes a Python reference compiler, 31 passing standard-library tests, JavaScript cross-language projection checks and full protocol notes. The repository's published web view should not be mistaken for a source-backed distributed index over a full 50 GiB corpus.

References: [QITṬ](QITT_CYCLIC_ARABIC_REGISTER_CALCULUS.md), [Encycled Calculus](ENCYCLED_CALCULUS.md), [Google Search operators](https://support.google.com/websearch/answer/2466433), and [Google Programmable Search](https://developers.google.com/custom-search/docs/json_api_reference).

## Open evidence gates

Actual public site deployment, independent browser visual tests (local Chromium navigation was blocked by the environment), remote content-addressed source storage beyond the 2,048-character URL limit, and authorized live provider requests remain separate commissions. No protocol token can manipulate the behavior of a third-party LLM or evade provider policies.
