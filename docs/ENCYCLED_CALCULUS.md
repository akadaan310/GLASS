# GLASS Ω — Encycled Calculus / Four-Tilde Computational Mechanics (0.1)

**Owner commissioning narrative:** 2026-10-26, GLASS and HOMELESS extension.  
**Formalization:** GLASS / 7u. **Science status:** proposed unifying formalism with explicit inherited mathematics, local executable mechanics and open measurement/novelty questions.  
**Research/terminology rule:** No Google/web research was used to test, certify, or originate this theory. The owner's GLASS, SURFACE, HOMELESS and QITṬ repositories were inspected directly.  
**Primary artifacts:** runtime/encycled.hpp, runtime/encycled_cli.cpp, tests/encycled_test.cpp, apps/clockworld/index.html, atlas/encycled-calculus-v0.1.json.

## 0. The thing the conventional bit snapshot omits

A captured bit value \(b=0\) or \(b=1\) is not a record of **how it became that value**. A richer observed computational state is

\[
X=(\mathrm{id},v,a,I,c,E,P),
\]

where id is stable identity, \(v\) is value, \(a\) is an address *in a declared address space*, \(I=[t_\mathrm{birth},t_\mathrm{end})\) is lifetime, \(c\) is the clock domain, \(E\) is a causal event sequence and \(P\) is provenance including uncertainty and observation mechanism.

The user proposes **Encycled Calculus** to study event-directed trajectories, repeated periods, optimization over lifetime, and replay. **Four-Tilde Mechanics**, written \(\widetilde{\mathcal M}^{(4)}\), is an author-defined four-projection contract:

\[
\widetilde{\mathcal M}^{(4)}(X)=
(\widetilde V,\widetilde L,\widetilde K,\widetilde O)
\]

- \(\widetilde V\): logical value/bitword and typed operation.
- \(\widetilde L\): identity, allocation, ownership and lifetime intervals.
- \(\widetilde K\): monotonic, logical, simulated and physical clock domains, with declared conversion.
- \(\widetilde O\): event origin, observation, provenance, measurement resolution, replay witness and unresolved uncertainty.

Tildes here denote an **instrumented representation**, not mathematical approximation by default. The superscript four counts named *independent description layers*, not four physical dimensions, a mathematical tensor rank, or four clock phases. This is a newly specified GLASS naming convention: neither originality in the global scientific literature nor physical completeness is asserted.

## 1. Established groundwork, integrated without relabeling it as discovery

**Established mathematical ingredients** include labeled transition systems, finite-state machines, temporal logic, logical/Lamport clocks, vector-clock causality, event sourcing, step functions and Stieltjes/distribution derivatives, hybrid dynamical systems, sampled-data control, harmonic analysis, optimization and game theory. In Encycled Calculus these are packaged under one typed computational interface.

**Proposed GLASS constructions** include four-tilde records, the cycle-carry operator over event trace/lifetime, per-object lifetime charge, normalized clock-domain maps, and the native/visual commission interfaces described below. The owner-defined name is not a proof that these have never been considered elsewhere. **Unverified physical claims** such as measuring intrinsic clocks of individual transistor states from app logs or observing every bit flip from software remain open and outside the current instrumentation capability.

## 2. A general-form mathematics of hybrid clocks

Choose a carrier \(Q\) of finite discrete states, a continuous vector space \(Z\subseteq\mathbb R^n\), event alphabet \(\Sigma\), clock domain set \(K\), and observable outputs \(Y\).

\[
\mathcal E=(Q,Z,\Sigma,K,F,G,R,H,\Lambda).
\]

Within a mode \(q\in Q\), the state flows continuously under \(\dot z(t)=F_q(z,u,t)\), when such a physical or simulated flow is actually declared. Discrete events \(e\in\Sigma\) occur when guard \(G_e(q,z,c)\) holds and reset \((q,z,c)\) through typed transformation \(R_e\). \(H\) projects what the observer is allowed to see; \(\Lambda\) preserves source and clock conversion witnesses.

A digital word is instead a right-continuous piecewise-constant function \(b:\mathbb R_{\ge0}\to\{0,1\}^n\). It can jump at programmed writes, DMA/device writes, fault injections, physical disturbances and other admitted causes. **The bit does not require a separate clock for every possible state flip.** A CPU clock, a memory subsystem, an oscillator and a logical event counter have different execution semantics.

For one bit changing at times \(t_i\), with signed jumps \(\Delta b_i=b(t_i^+)-b(t_i^-)\), its distributional derivative is

\[
Db=\sum_i\Delta b_i\delta_{t_i}.
\]

On an interval between events its ordinary derivative is zero. At a jump its classical derivative is not a finite slope. This formal distinction is one source of the new observatory's insight: a smooth display interpolated between frames does not preserve the actual event structure.

### Clocks, epochs and observation

A **clock record** carries (id, units, epoch, tick, resolution, observed_at, uncertainty, monotonicity, conversion_profile). Logical ticks count ordered events but need not measure elapsed milliseconds. Time from a JavaScript animation frame is not a CPU cycle counter. Converting one domain to another requires a calibrated map and error bound, not an asserted equality.

Device power states are special: a completely powered-off phone cannot continue measuring itself via an app. The terminal-world model therefore records **OFF/UNKNOWN** as an absence-of-observation interval and **BOOT_EPOCH** when the software becomes capable of witnessing the device again. A hardware external power monitor could provide a separate, physically observed signal. A Boolean flag written after boot is only evidence of that post-boot program action, not of an unobserved internal transition while the phone was off.

### Causality and replay

Let \(e_i\prec e_j\) mean happens-before, formed by program order, synchronization, and authenticated message edges. Two events sharing a wall timestamp are not necessarily causally ordered. A deterministic replay needs a declared initial state, executable transition rules, event order, external input capture and compatible version; it cannot generally reproduce nondeterministic hardware faults solely from the existence of an event log.

The native reference journal serializes an atomic control-word transaction into per-bit before/after witnesses with a **shared transaction ID**. A logical multi-bit RETURN is not rewritten as a single physical upset.

## 3. Encycled operators and the calculus of costs

Define the cycle comparison operator, for a value in a group such as \(\mathbb R^n\):

\[
\Delta_\circ^{T}x(t)=x(t+T)-x(t).
\]

The residual vanishes for a \(T\)-periodic trajectory on the chosen observable domain. For non-subtractable states use a declared metric \(d(x(t+T),x(t))\), equivalence predicate, or relation-valued return. **A zero sampled residual does not prove global periodicity:** it is limited to the inspected interval, observable and resolution.

The event-cycle aggregation operator is

\[
\mathscr I_\circ^T(f;t)=\int_{t}^{t+T}f(\tau)\,d\tau,
\]

with integration law stated by whether \(f\) is a continuous signal, discrete event intensity or mixed measure. For an instrumented object's lifetime \(I_o\), define the resource exposure:

\[
C_o=\int_{I_o}r_o(\tau)\mathbf 1_{\{\mathrm{alive}(o,\tau)\}}\,d\tau
+\sum_{e_i\in E_o}c(e_i).
\]

The \(r_o\) term is an *explicit charge model*, not direct electrical power measurement. This enables opportunity-cost accounting and optimizations across open intervals, not simply the final bit value.

For control states, a return map \(P:S\to S\) is defined only when its boundary, guard and effects exist. Repeated cycles generate iterates \(P^n\). A finite orbit is periodic when \(P^n(s)=s\) for some positive \(n\); the minimal such \(n\) is the exact state period. When state includes an increasing event generation or monotonically increasing real time, the **visible mask** may be periodic while the **entire augmented machine state** is not. This is essential for provenance-sensitive replay.

### Trigonometry, rounded geometry and light

For \(x(t)=\sin(\omega t+\phi)\), the period is \(T=2\pi/|\omega|\) for nonzero \(\omega\). \(\sin(t)\) has period \(2\pi\); \(\sin(2\pi t/T)\) has period \(T\). The user-requested dual plots distinguish *continuous phase* from its sampled and thresholded Boolean control. A sampled sequence at \(f_s\) can alias a component above \(f_s/2\) absent additional band-limiting assumptions.

A circular rounded corner with radius \(r\) satisfies \((x-x_c)^2+(y-y_c)^2=r^2\); an arc can be parameterized by \(x=x_c+r\cos\theta\), \(y=y_c+r\sin\theta\). CSS border-radius already supplies such geometry; hand-written trigonometry is optional for custom shaping or simulation.

Illustrative compositing uses \(C=\alpha F+(1-\alpha)B\) in a declared **linear-light** color space, with Gaussian-like blur \(K_\sigma *B\) approximating frosted glass. The production effect of real glass needs optical calibration/material models; screen opacity alone is not refractive physics. LUMEN/ILLUMINATION may be presented as lexical/visual labels, not used to infer an unverified Latin etymology or an X-ray research history.

## 4. The exact owner-specified control motif

The visible control word sequence is:

\[
0000\longrightarrow1000\longrightarrow1100\longrightarrow1110
\longrightarrow1000.
\]

Call the source initial stage **VOID**, then MARK1, MARK2, MARK3, RETURN. The final 1000 receives a new generation identity, even though it has the same **rendered bits** as the earlier 1000.

The 1110→1000 step changes **two bits**, not one. A serialized reference emits two per-bit records under **one causal transaction**. Treating that return as a *single-event upset* would be incorrect. The programmed symbolic control sequence itself can be replayed without any hardware disturbance.

The low-state/terminal transition can be linked to the previously formalized QITṬ register: typed ṢIFR and cycle/return positions are **analogous interface forms**, but base-two bit patterns and base-ten Arabic computational addresses are not interconvertible without a typed mapping and preservation law.

## 5. Lifetime semantics of pointers and objects

A declaration such as a local variable of type pointer creates **a binding with scope**, not necessarily a heap object's lifetime and not a CPU-level clock. For example:

~~~cpp
int* x = new int(7);
// x: pointer binding lifetime controlled by its enclosing scope
// *x: separately allocated int object, begins at successful allocation
delete x;
// pointee lifetime ends; x's binding may remain, now dangling
x = nullptr;
// x's binding continues with a new pointer value until scope exit
~~~

Under this model emit distinct events: BINDING_BORN, POINTEE_ALLOCATED, POINTER_ASSIGNED, POINTEE_DEALLOCATED, POINTER_ASSIGNED_NULL, BINDING_ENDED. Use stable generation-tagged allocation IDs to avoid pointer-reuse confusion. A *logical lifetime interval* is created by instrumentation; no claim is made that C++ pointer syntax activates an internal independent mechanical timer.

In a research profiler, clocks may attach to an allocation, object identity, lexical scope, thread, coroutine, network session, Android activity or world actor. The owner can ask when a lifetime opened, how much simulated resource exposure accumulated, which operations ran while it was open and whether a failure interval overlaps a race. **Observability has overhead**; the instrumentation budget and trace losses must be measured.

## 6. Mechanical computation and observability limits

**Mechanical computing** historically includes physical mechanisms such as switches, gears, cams, relays and clocks. This research constructs an **abstract, clocked computational machine** that can map events to symbolic mechanisms without claiming an app can directly manipulate transistor physics. A physical laboratory extension may implement relays, programmable microcontrollers, logic analyzer captures or measured CPU counters under explicit calibration and appropriate safety controls.

For optimization, distinguish:
1. **Simulation slowdown** changes the model's mapping from wall time to virtual time; exact logical transitions remain unchanged if integration is correct.
2. **Thread scheduling** affects when a program executes and can reveal race conditions but does not fully determine every microarchitectural bit write.
3. **Device hardware frequency and power** require platform-approved controls and measurement; a webpage cannot reliably throttle the whole CPU by decree.
4. **Sampling rate** limits what transitions are visible; increasing it does not recover events that were never instrumented.

An observation channel records its own resolution, known blind intervals, instrumentation cost, lost events and possible clock drift. No trace is labeled “complete” unless it covers its defined model with a witness.

## 7. The two-lane Commissioning Automaton

The former workflow needed repeated giant natural-language constitutions pasted to Codex. The proposed **Terminal World** separates a creative proposer from a deterministic effect gate:

~~~text
Human research directive ─┐
                           ├─ DRAFT → PARSE → TYPECHECK → ADMIT
Optional LLM proposal ─────┘                          │
                             bounded DSL, rights, event cursor
                                                      ↓
                           EXECUTE → OBSERVE → VERIFY → CHECKPOINT
                                           │              │
                                           └─ REFUSE/RETRY ┘
                                                        ↓
                                           PUBLISH main + receipt
~~~

**LLM lane:** optional agent generates *candidate* DSL operations, hypotheses, study plans and expressive descriptions. It has no ability to self-certify a scientific result or bypass authority. The local Clockworld contains **no model connection**.

**Automaton lane:** finite parser, operator registry, guard/type checker, resource admission, bounded executor and source-linked journal. Typed operations have finite input domains or explicit budget bounds; unlimited natural-language generality is never claimed.

**Minimum terminal grammar, local reference:**

~~~ebnf
command = "HELP" | "TRACE" | "RESET" | "PAUSE" | "PLAY"
        | "FLIP", bitindex
        | "FREQ", decimal_in_0_25_to_4
        | "STEP", integer_1_to_64
        | "WORLD", ("HOUSING"|"SHELTER"|"HOLD")
        | "PROPOSE", command
        | "ADMIT" ;
~~~

PROPOSE stores a candidate without applying it; ADMIT passes it to the finite grammar/effect handler. Plain local commands execute directly after equivalent parser/guard checks. The terminal does not eval arbitrary code, spawn shell processes or contact an LLM. The browser demonstration records volatile bounded events; permanent publishing/identity and durable ACSP/PURL transport remain future adapters.

**Parent harness contract:** exact source pin + user statement → typed requirement map → permitted operational grammar → pre-appended intent → version-fenced worker → event receipt → independently checked replay/proof obligation → safe main publication. A model and a grammar-based interpreter are complementary engines, not the same entity.

## 8. HOMELESS: living population, housing and opportunity cost

The existing HOMELESS repository's authoritative product is a Unity-native game with a reusable Dark engine and a unique founder player identity. The GLASS Clockworld experiment is an **independent synthetic modeling instrument, not native gameplay or a replacement of that commission**.

A simulated person carries age, unique synthetic ID, kinship/household edges, guardian relationships where appropriate, daily availability, mobility constraints, housing security and event history. A child can be linked to a family/guardian rather than simulated as an unconstrained independent economic adult. Orphanhood, loss of a parent/guardian, institutional placement and homelessness are **different predicates**. Biological twins share a birth cohort; “twins at different ages” would need an explicit fantasy/time-shift mechanic or different observation clocks rather than fabricated demographic facts.

Housing state is not a binary moral label. A modest reference carrier is:

\[
H=\{\mathrm{unsheltered},\mathrm{sheltered},
\mathrm{temporary},\mathrm{stably\ housed}\}.
\]

Events such as loss of housing, entry to a shelter, move to temporary accommodation and permanent tenancy are guarded by household continuity, supply and chosen policy. State is allowed to change; identity persists. “Houseful” and “Full House” can be authored narrative metaphors, without claiming they are historical linguistic derivations or a full theory of shelter.

The browser demonstration generates **deterministic fictional households** and currently uses a simpler three-state projection (unsheltered, sheltered, housed) with illustrative transition probabilities. It is not populated from hospitals, census data or phone contacts. Hospital encounters are not a complete demographic census. Any future geographically representative population requires independently sourced, dated data, privacy constraints, eligibility/coverage definitions, uncertainty and conservation accounting (births, deaths, migration, households), none of which is claimed in the prototype.


### Encounter memory and “Have I met this person?”

A simulated actor may ask another actor whether an encounter happened. A binary acquaintance flag is not enough to answer honestly when event history is incomplete. Define a source-aware relation

\[
\operatorname{Met}(i,j,[t_a,t_b],P)\in
\{\mathrm{WITNESSED},\mathrm{NOT\ OBSERVED},\mathrm{UNKNOWN}\},
\]

with encounter event \((\mathrm{id}_i,\mathrm{id}_j,t,\mathrm{location},\mathrm{observer},\mathrm{source},\mathrm{confidence})\). A **witnessed** event proves that the finite model recorded an encounter; absence from an incomplete log does **not** establish non-encounter. NOT_OBSERVED is explicitly scoped to the instrument's observation interval, and any claim about time before its epoch is UNKNOWN.

The Clockworld console adds **MEET a b** to record a synthetic encounter between two distinct cohort IDs and **MET a b** to ask whether that exact pair was witnessed in the current epoch. Reset clears this synthetic record, making prior history unknown rather than inventing a negative history. No device location, camera, contacts or real person identification is used.

Under game theory, an encounter is a state transition with attention/time cost and possible information gain, not necessarily a beneficial or harmful outcome. The alternative action foregone is part of opportunity cost only after the relevant utilities and constraints are declared.


### Action value and foregone alternatives

At world state \(s\), actor \(i\) has feasible actions \(A_i(s)\). With model reward \(r_i\), future policy \(\pi\) and discount factor \(0<\gamma\le1\), define horizon-\(T\) action value:

\[
U_i^\pi(s,a)=\mathbb E_\pi\left[\sum_{t=0}^{T}
\gamma^t r_i(s_t,a_t)\mid s_0=s,a_0=a\right].
\]

The **opportunity cost** of choosing \(a\) under that model is

\[
OC_i(s,a)=\max_{a'\in A_i(s)}U_i^\pi(s,a')-U_i^\pi(s,a).
\]

The browser uses an explicitly illustrative immediate-score approximation to this expression: add stable housing, add a temporary shelter, or maintain resources. It shows a *foregone modeled utility score*, not dollars, measured life outcomes, or moral valuations of persons. Resource tradeoffs and service access could be expanded through a source-backed economics model later.

The condition for a household-level transition must preserve all household members' source identities and verify guardian/child relationships. The model should expose alternative future actions for agency, rather than reduce homeless people to scripted obstacles.

## 9. Realtime screen and mathematical graphics

The first deliverable is **apps/clockworld/index.html**. It is a standalone offline HTML/CSS/Canvas2D instrument that renders full viewport and offers an optional Fullscreen control; no Three.js service/CDN is needed. Four screens:

| Screen | Computation and UI behavior |
|---|---|
| MECHANICS | Lissajous phase trace, live sine signal, sampled observations, exact 4-bit word, manual step/pause/fault injection, source event stream, frequency/speed/sample controls |
| HOMELESS | Deterministic synthetic household cohort, three housing security states, policy turns, state counts, and immediate modeled opportunity cost |
| TERMINAL | Local finite parser with typed commands and optional PROPOSE → ADMIT. No shell or LLM transport |
| ATLAS | Six accessible science cards: event derivative, period residual, resource exposure, aliasing, clock causality and game-theoretic payoff |

Rendering uses Canvas2D analytical curves with glow, perspective grid, and responsive panel layout; user input updates runtime computation. It is a **scientific visualization of an explicitly modeled system**, not a physical observation of bit hardware or a Unity-native game scene.

The native C++20 header independently implements a fixed bounded bit-event ledger, logical clocks, event origin, per-object logical lifetime, replay and a step-function integral. The native CLI produces a JSON trace with the displayed 0000→1000→1100→1110→1000 control motif. It is not directly linked into the browser; the browser and native core share the *specified conceptual contract* pending adapter/parity certification.

## 10. Mathematics and topology review

The full domain rake follows SURFACE's domain IDs. Each is applicable only as described; none is proof of general scientific universality:

| Domain | Construct / obligation |
|---|---|
| logic | Explicit guards, temporal predicates and proof-vs-claim separation |
| set theory | State carriers, event and interval domains, finite and infinite bounds |
| type theory | Distinct logical bit, address, clock, event, object and observation types |
| arithmetic | Bitword transitions, popcount, carry and exact integer event ticks |
| algebra | State-transition monoids, partial maps, period iterates and quotient laws |
| order/lattices | Causal partial order and clock information ordering |
| combinatorics | Finite words, traces, scheduling orders and state explosion budgets |
| graph theory | Event DAG, household graph, phase cycle and transition automata |
| automata/languages | Command DSL, deterministic finite admission and statechart |
| information/coding | Loss when snapshots discard intermediate writes or clocks |
| geometry | Phase projections, drawn curves and coordinate transform |
| topology | Loops, event graph, phase circle and quotient/fiber distinctions |
| analysis/calculus | Distribution derivatives, step-function integration, periodic residual |
| differential equations | Optional hybrid continuous flow between guarded events |
| spectral/harmonic | Oscillator phase, sampling, Fourier interpretation and alias controls |
| probability/statistics | Optional transition kernels, confidence and finite random seed |
| optimization/control | Resource exposure, constraints and policy opportunity costs |
| numerical analysis | Integration step, discretization error and stability contracts |
| category/composition | Typed domain translations, admitted functors and source preservation |
| physics/units | Explicit frequency Hz vs ticks, electrical measurement as separate evidence |
| quantum information | Not applicable to demonstration without a quantum state/channel |
| computational complexity | Per-event O(width), bounded ledger, history cap and state explosion |
| metrology/uncertainty | Observer resolution, missed transitions, calibration and model-vs-measurement |

**Topological profile:** finite phase cycle \(C_n\) has one connected component and one independent loop when its edges explicitly close. Its geometric realization is a circle graph. The cumulative event trace is usually a **directed path with unique sequence positions**, not a periodic topological loop merely because a repeated bit mask appears. Quotienting by displayed mask can produce a cycle, but loses event generation, so full replay cannot descend to that quotient. Multi-clock products have a chosen topology only after component topology and synchronization relations are specified.

## 11. Invariants, counterexamples and admission gates

- **I1:** replaying typed per-bit effects from the zero initial word yields the final stored word, or a categorized refusal.
- **I2:** a multi-bit logical event uses one transaction identifier but records each actually changed bit.
- **I3:** every event has a nondecreasing logical tick and strictly increasing journal sequence number.
- **I4:** object lifetime closure occurs at or after opening; a second closure is rejected.
- **I5:** a denied operation leaves the prior bitword and event count unchanged.
- **I6:** all given integration samples have finite times/values and a monotonic time axis.
- **I7:** visualization samples never substitute for an independently complete event trace.
- **I8:** synthetic NPC identity persists through household-level housing changes.
- **I9:** proposals without admission have no worker side effects; admitted commands remain restricted to the grammar.
- **I10:** source records distinguish owner-proposed interpretation, defined mathematical semantics, locally reproduced simulation and externally measured physical observation.

**Counterexample E1:** 0000→1000→1100→1110→1000 is not binary successor arithmetic; the numeric values are 0,8,12,14,8.  
**E2:** two writes 0→1→0 between observations appear unchanged at the endpoints; endpoints cannot reconstruct a missed event.  
**E3:** at equal wall timestamps two racing writes can have no reliable inferred causal order.  
**E4:** aliasing may show a near-stationary sampled sinusoid despite fast continuous oscillation.  
**E5:** a pointer variable can outlive its deallocated pointee.  
**E6:** a power-off epoch is not observationally complete from the phone's own app.  
**E7:** a "house" label does not identify a person's family, safety or access history.

**Research gate status:** typed formal model and first native implementation exist; local native bounded tests pass on the creating Linux host, covering deterministic trace replay, transaction grouping, lifetime refusal, out-of-bounds refusal, event-budget atomic refusal and exact sampled integration fixture. Browser JavaScript passed Node syntax checking; an attempted container headless Chromium screenshot timed out even for a trivial page, so **visual browser acceptance remains unverified**. No Android/Unity device build, real hardware bit measurement, formal theorem prover or external scientific originality review is claimed.

## 12. Source-to-runtime adoption

- **GLASS:** parent commission event journal, source custody, results, evidence and main publication.
- **SURFACE:** independent native rendering/physics, typed physical computation, stable PHANTOM provenance and future C++ adapter. No rewrite of the existing renderer.
- **QITṬ:** related loop/return/ṢIFR transition language under a deliberately separate numeric encoding.
- **PolyIA:** typed finite alphabets, generators and guarded compilation are candidate reference adapters with source pins, not assumed runtime deployment.
- **PURL / SEURL:** identity, permissioned resource operations and URL-addressed state are future transport interfaces. Do not silently change safe-GET semantics.
- **HOMELESS:** Dark/Unity remains authoritative for the actual game. The synthetic GLASS cohort is a replayable exploratory model only and imports no private real-world persons.
- **Mechanical laboratory:** an external hardware capture/oscilloscope/logic analyzer interface may be commissioned to close physical observation gaps, with clock conversion and calibration.

**Next bounded commission:** formalize persistent clock-domain IDs and causal event API; implement typed dual-mode LLM proposal/finite-worker RPC with provenance; establish browser/native output parity; adapt the synthetic household state machine into HOMELESS's Unity project only after the product's existing commission and native gates have been reconciled.

**Native local reproduction:**
~~~sh
g++ -std=c++20 -O2 -Wall -Wextra -pedantic tests/encycled_test.cpp -o /tmp/encycled-test
/tmp/encycled-test
g++ -std=c++20 -O2 -Wall -Wextra -pedantic runtime/encycled_cli.cpp -o /tmp/encycled
/tmp/encycled trace
# Open apps/clockworld/index.html in a modern browser for the standalone visual instrument
~~~
