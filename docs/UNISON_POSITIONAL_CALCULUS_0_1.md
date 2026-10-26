# GLASS / UNISON Positional Calculus 0.1 — صِفْر, ∅ and rotating tapes

## Origin
Research derived from the owner's formulation of PURL, seURL, ACPS/ACSP, Vitromaton, zero/null positional tapes, Arabic numeral registers, and optimization contour grammars. Hypotheses are not physical discoveries. Source links:
- https://github.com/akadaan310/purl (stateful resources, capabilities, event replay)
- https://github.com/akadaan310/seurl (URL-as-transition state machine)

## Typed alphabet
State vocabulary: ∅(no admitted datum), NULL(missing typed observation), 0(additive identity), 1(multiplicative identity), 00(two-position zero tape), ⊙(observation), τ(clock), ↻(position rotation), ⊕(xor), ⤳(candidate inverse), Π(provenance).

The mathematical null space ker(A)={x|Ax=0} is a linear subspace, not the same as empty set or a null pointer. The all-zero binary state may be a selected initial register state but is not compulsory. Quantum superposition is a property of quantum states in Hilbert space, not evidence that every astrophysical star is itself a binary quantum bit.

## Tape and positional semantics
A base-b tape d0...dn has value Σ_i d_i b^(n-i), with digits 0<=d_i<b. Successor is right-to-left carry. Example decimal 09 -> 10; binary 01 -> 10. Rotation rho(d0,...,dn)=(d1,...,dn,d0); rho^m = identity for a tape of length m, with smaller periods for repeated patterns. Rotation and numerical successor are distinct.

For a fixed-width tape length m, define C_b,m(s) as modular successor on Z/(b^m Z). This yields exact cycles of b^m distinct states. If width is allowed to grow, successor generates an unbounded tape sequence. Adding null and unknown requires a tagged sum type rather than coercion to numeral 0.

## Language / geometric operator bridge
Use field semantics, not mystical equivalence: predecessor/successor = discrete order; prefix/suffix = formal language position; anterior/posterior = orientation relative to declared frame; adjacency = graph edge; juxtaposition = concatenation/tensor or product as typed; superposition = linear combination of vectors; projection = map into an observed space; perturbation = controlled parameter delta; contours = level sets {x | f(x)=c}; gradient = vector of partial derivatives; stationary points = ∇f=0; Hessian = second derivative matrix; orbit = repeated operation of a group/semigroup action.

Arabic letter / abjad sequences may define independent register profiles or mappings. They are not presumed physically equivalent to solar/lunar cycles or every language. Store mappings as explicit rules with counterexamples.

## Vitromaton protocol bridge
PURL: durable resource state/capability/provenance; seURL: finite URL transition verbs; ACPS: handoff/checkpoints; Vitromaton: machine state and generators; GLASS: observational rendering.
Proposed typed expression:
⟦Λ:bin ⊗ Γ:successor ⊗ τ:42 ⊙ tape:01 Π:source⟧
This is a language string, not yet a registered URL scheme. Encode as percent-encoded data within HTTPS and publish manifest operations via PURL. GET is observation only; mutations use authenticated explicit verbs and expected version.

## Convergence experiments
Known functions: Sphere, Rastrigin, Ackley. The first has a convex basin; Rastrigin has many local minima and a global minimum at zero; Ackley has a central global minimum and nonlinear periodic outer terrain. Sample finite grids, quantize level sets to contour bands, estimate finite-difference gradients and sample-local minima, and compare rotated cell neighborhoods/transition tapes. Quantization, grid size and coordinate frame must be recorded to distinguish discrete artefacts from mathematical properties. See tools/unison_positional.py.

## Tests / obligations
- NULL != ZERO; unknown is not coerced to 0.
- value(digits(n,b),b)==n for n>=0, b>=2.
- rotate(tape,len(tape))==tape.
- successor((0,1),2)==(1,0); successor((9,),10)==(1,0).
- Sphere, Rastrigin, Ackley evaluated at (0,0) are approximately 0.
- For a known centered odd grid, sampled minimum approximately (0,0).
- Replay must store function choice, grid extent, step size, contour quantization, and code revision.
- These tests are obligations until executed with retained receipts; a GitHub commit is not a proof.

## Next
Join Vitromaton oracle event IDs to PURL resource manifests and ACPS continuity receipts; implement normalized URL language parser; expose landscape contour and register rotations inside GLASS; provide independently reproducible perturbation comparisons on same grid with fixed parameter changes.
