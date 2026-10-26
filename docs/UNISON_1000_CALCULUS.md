# GLASS / UNISON-1000 — Computational Genesis Calculus v0.1

## Objective
Select 1000 provenance-preserved open source repositories; acquire each at a declared rate; derive a GLASS AST and reversible generator; learn compiler transitions using separately isolated compilation experiments; retain witnesses. Extend the same mechanism to successive corpora.

## Exact contract
R := (repository, commit, tree, license, dependency resolution, toolchain, environment).
Four paired observations:
1. GENESIS G: source object bytes -> content addresses
2. GRAMMAR A: source -> typed AST (syntax + symbol semantics + references)
3. CONJUGATE D: generator recipe + retained parameters -> source candidate; explicit inverse proof required
4. EXECUTION X: source -> compiler IR -> objects -> ELF/PE/Mach-O -> process and I/O traces
The fifth form Q is a queryable identity joining G, A, D, X with all evidence.

Conjugates are relations, not assumed equalities:
C1=(parse, emit), C2=(compile, lift), C3=(execute, replay), C4=(compress, regenerate).
For each relation record forward domain, reverse domain, fidelity, lost information and counterexamples.

Let B = exact source bytes, P = generator program+version+grammar dictionary, Z = parameters+metadata+external dependencies. Define validated compression as
  rho = |B| / (|P| + |Z|).
A 3-5 symbol label only addresses a stored model and **is not itself lossless compression**. Payload sizes must include shared generator/dictionary amortization. Any roundtrip claim requires SHA256 equality per file, mode/symlink handling, stable paths, pinned dependencies and reproducible filesystem representation. v0.1 prototype does not preserve symlink and permissions; this is a known fidelity gap.

## 1000 cohort selection
20 language strata, 50 repositories each. Public non-fork, non-archived, licensed, star>=20, <50 MB GitHub-reported size. Repository uniqueness is global. Deterministic ranking is stars descending with fixed pagination, but GitHub search is mutable; freeze the JSON manifest and resolved commit immediately. Use license compatibility checks **before** deriving redistributed corpus artifacts. Do not execute untrusted repositories during retrieval.

## Budget and rate
GitHub search REST request spacing 4 seconds, serial, retry-after/reset adherence, no retry storms. Clone sequentially by default every 30 seconds, max 10 per explicit invocation, plus a per-repository execution timeout. First run 10, then 50, then 1000 after receipts and storage budgets are observed. Do not schedule autonomous indefinite cloning. Optional GitHub token via GITHUB_TOKEN. Clone uses partial fetch; pin commit on acquisition. A full repository with history is different from a current-tree acquisition and is not claimed.

## Implementation
`python tools/unison_corpus.py select --manifest corpus/selection.json`
`python tools/unison_corpus.py clone --manifest corpus/selection.json --destination corpus/acquired --limit 10`
`python tools/unison_regenerate.py pack corpus/acquired/repos/OWNER/REPO /path/to/objects`
`python tools/unison_regenerate.py unpack /path/to/objects /path/to/reconstructed`
`python tools/unison_regenerate.py verify /path/to/objects /path/to/reconstructed`

Local scripts are a first executable harness, not proof of a populated 1000-source corpus. No clones or compiler executions have been run in this commission. Next tasks: implement tree-sitter multi-language parsing, symbol/linker metadata, AST generator induction, hermetic deterministic toolchains, PE/ELF object instrumentation, source maps, concurrency and clock event traces, typed QITṬ alphabet bridges and minimum-description-length candidate search.

## Four conjugate alphabets
Alpha_genesis encodes content-addressed source objects; Alpha_grammar encodes syntax/category morphisms; Alpha_clock encodes causal transition order; Alpha_binary encodes bytes, instructions, and emissions. Arabic 28-register and additional terminal alphabets are typed profiles whose mappings require explicit mathematical witnesses. Lunar and solar register structures are models to explore, not proven natural identities.

## Governance
Keep original authors, licenses, attribution and versions. Generated candidates are hypotheses; compile success is not semantic equivalence. Record counterexamples and reject false reverse claims. Changes to the native engine remain linked to the original GLASS event journal, and incremental commits publish to main.
