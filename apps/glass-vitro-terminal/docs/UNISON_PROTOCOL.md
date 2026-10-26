# UNISON/0.1 — N-dimensional terminal operator language

**Host:** GLASS (an observable terminal scene). **Engine:** Vitromaton (guarded automaton). **Language:** UNISON. **Projection:** the SURFACE stage inside GLASS. These labels name software contracts, not new fundamental laws of physics.

## 1. Alphabets and typed semantics

| Operator | Sort | Effect |
|:--|:--|:--|
| `⟦...⟧` | `Scope` | delimit one typed program expression |
| `Λ` | `Alphabet` | script / register identity |
| `Ω` | `Oracle` | observed state and measurements |
| `Γ` | `Generator` | executable transformation with declared input/output types |
| `τ` | `Clock` | logical time and guarded time events |
| `Π` | `Witness` | hash-chained provenance and evidence |
| `⊗` | `Compose` | ordered association; not assumed commutative |
| `⊕` | `U32×U32→U32` | bitwise XOR |
| `∧` | `U32×U32→U32` | bitwise AND |
| `∨` | `U32×U32→U32` | bitwise OR |
| `↻` | `U32×U32→U32` or `Rⁿ→Rⁿ` | typed rotation, requires operator selection |
| `∅` | `No admitted value` | not equivalent to `0`, false, or an empty vector |
| `۞` | `Projection` | observable terminal / rendered frame |
| `⊣` | `Refusal/Counterexample` | failed guard or contradicting witness |

A compact token example is `⟦Λ:binary ⊗ Γ:xor(1,0) ⊗ τ:1⟧`. In the initial executable, this and `⟦Γ:rotate⟧`, `⟦Γ:halt⟧` are recognized families. The full grammar below is a **specification frontier**, not a claim the partial parser implements every case.

```ebnf
Program       = Scope | EnglishCommand ;
Scope         = "⟦", Term, { "⊗", Term }, "⟧" ;
Term          = "Λ:", Ident | "Ω:", Ident | "Γ:", Application |
                "τ:", Integer | "Π:", Ident ;
Application   = Ident, "(", [ Operand, { ",", Operand } ], ")" ;
Operand       = Integer | Ident | Scope ;
Ident         = UnicodeIdentifier ;
Integer       = Decimal | Hex ;
```

## 2. N-dimensional state machine

Let `x∈ℝⁿ`, `1≤n≤16` in the tested runtime. A `space n` command replaces the state with the origin. The operator `move i δ` applies `x' = x+δeᵢ`. The plane operator `spin i j θ` applies a Euclidean Givens rotation in the axes `(i,j)`. If `i≠j`, `0≤i,j<n`, and `θ` is finite, `‖Rᵢⱼ(θ)x‖₂=‖x‖₂` and its inverse is `Rᵢⱼ(−θ)`. These are *software mathematical transforms*, not full quantum gates on arbitrary Hilbert spaces.

A timeline state is `s=(x,Q,G,τ,Π)`. Each admitted command advances `τ`, records a source-linked result and a SHA-256 chain. `halt` guards mutation; `resume` allows transitions again. Screens may still render observational frames while a logical transition clock is stopped. A display refresh is not automatically a witnessed physical state transition.

## 3. Fixed word and matrix operations

`xor 0xff 0x34` is evaluated in fixed-width 32-bit arithmetic (O(1) per machine word). Matrix `10×10` multiplication evaluates 100 entries and 1,000 multiply-accumulate terms, with per-term `(row,col,k,before,after)` records and a canonical trace digest. Tapes `row`, `column`, `diagonal`, `anti-diagonal`, `perimeter`, `snake` address the stored linear memory in different orders; the traversal path is not a new matrix product.

An independent raster `P` with `N` pixels requires Ω(N) output values even if its fixed-width per-pixel gates are O(1). Native renderer computes every pixel in C++ and the Android platform composites separate typography and keyboard input. No claims of actual measured phone heat from XOR counts are made. The operator `energy before after` reports only the number of switching bits and a declared proportional energy model.

## 4. Quantum state operator

A 1-qubit classical simulation stores `(α,β)∈ℂ²` with norm `|α|²+|β|²=1`, and gates `H`, `X`, `Z`. `qubit h` from `|0⟩` produces two 0.5 measurement probabilities. Repeated `H` returns to `|0⟩`. `qubit measure` samples from a reproducible **pseudorandom** digest and collapses the simulated state. It does not execute on physical quantum hardware or imply quantum computational speedup.

## 5. The terminal and the web

Native CLI `:shell` opens the already-local shell attached to a PTY. Android mode embeds the Apache-licensed Termux terminal library to execute `/system/bin/sh` under normal app process permissions; it does not inherit the installed Termux user's packages or HOME. An optional future authenticated gateway can translate accepted `unisol://` typed addresses to ordinary HTTPS PURL resource manifests and ACSP/seURL checkpoint mechanisms. No automatic account access or remote shell access exists in v0.1.

## 6. Finite evidence and next stages

A language-bearing oracle is accepted when input types, transition guards, outputs, provenance and replay have finite witnesses. Advanced layers require Unicode grapheme-cluster parsing (ICU), additional alphabet profiles, a declared rule inducer over AST witnesses, instrumentation of actual instruction/thermal traces via authorized APIs, NDK on-device profiling, and server-side work partitioning. Future research is not treated as current execution evidence.
