# QITṬ/0.1 — ṢIFR–LIFF Cyclic Arabic Register Calculus
## A GLASS general-form science of letter registers, positional address, operator-holders and return topology

**Owner's originating proposal:** Abed Kadan, 2026-10-25. **Formalization:** GLASS / 7u collaboration.  
**Status:** An internally specified mathematical and computational research system. Owner-proposed axioms are distinguished from mathematical consequences of those axioms and from claims requiring historical/linguistic evidence. No external Google/web theory-check was conducted.  
**Canonical artifacts:** [Complete 28-entry registry](../atlas/qitt-register-v0.1.json), [QITṬ/0.1 grammar](QITT-0.1.ebnf), [predeclared commission](../commissions/qitt-001/INTENT.json).

---

## 0. The science, its object and its epistemic perimeter

**Discipline:** *Cyclic Arabic Letter-Register Calculus* (**CALRC**).  
**Research language:** **QITṬ/0.1** (قِطّ), a named example of a boundary-formed word/address.  
**Core control pair:** **ṢIFR–LIFF**, referring here to a typed holding/void register and a controlled carry/turn/return transition.  
**Computational object:** an explicitly interpreted, addressable finite tape of decimal slots whose nonempty cells project to the 28 Arabic registry symbols under a periodic lift.  
**GLASS home:** general-form language/number/transition research, **not** a replacement for Arabic as a natural language.

The owner proposes that the familiar 28-letter numeric ordering is useful as a register table, not merely as an enumeration of the writing system. We name it here a **letter-register table** and preserve the historical term "abjad" only as a quoted source-language label, never as the name of the proposed science. This text does not establish that ancient Arabic authors, Qur'anic composition or the historical development of Arabic employed the QITṬ execution rules. Such claims are outside the present owner-directed internal formalization.

The object is given by a tuple

\[
\mathfrak Q=(\Sigma_{28},R,\mathbb N_0,P,D,Z,L,V,G,T,\mathcal I,\mathcal O,\mathcal P),
\]

where:
- \(\Sigma_{28}\): 28 distinguished Arabic base-letter glyph identities.
- \(R:\Sigma_{28}\to\{1,\ldots,9,10,\ldots,90,100,\ldots,900,1000\}\): native registry weights; each listed native weight is unique.
- \(P=\mathbb N_0\): base-ten place indexes, with place 0 the units.
- \(D=\{0,\ldots,9\}\): decimal coefficients.
- \(Z\): typed ṢIFR states (gap, numeric zero, vacant operand, operator holder, reserved argument).
- \(L:P\times (D\setminus\{0\})\to\Sigma_{28}\): position-sensitive letter projection.
- \(V(p,d)=d10^p\): mathematical place valuation, distinct from \(R(L(p,d))\).
- \(G\): formal syntax/grammar for word and address programs.
- \(T\): registered transition relation including carry, borrow, bind, release, flip and return.
- \(\mathcal I\): explicitly declared word/operator interpretations.
- \(\mathcal O\): provenance-bearing observations/outputs.
- \(\mathcal P\): versioned source, profile, cycle and position evidence.

**Novelty boundary:** CALRC is a newly specified research language within GLASS. Novelty versus all other mathematical work is not claimed without external literature comparison, which is intentionally excluded here.

## 1. A full 28-place computational registry

The complete primary registry is \(9+9+9+1=28\). **These are register IDs with native numeric weights; they are not decimal digit glyphs and do not contain ṢIFR as a twenty-ninth letter.**

| # | Glyph | Name | Native \(R\) | Primary band | Primary role |
|---:|:---:|---|---:|---|---|
| 1 | ا | Alif | 1 | units | low-unit one; LIFF-associated turning marker only by explicit operator annotation |
| 2 | ب | Bāʾ | 2 | units | unit coefficient 2 |
| 3 | ج | Jīm | 3 | units | unit coefficient 3 |
| 4 | د | Dāl | 4 | units | unit coefficient 4 |
| 5 | ه | Hāʾ | 5 | units | unit coefficient 5 |
| 6 | و | Wāw | 6 | units | unit coefficient 6 |
| 7 | ز | Zāy | 7 | units | unit coefficient 7 |
| 8 | ح | Ḥāʾ | 8 | units | unit coefficient 8 |
| 9 | ط | Ṭāʾ (heavy Ṭ) | 9 | units | unit terminal \(9\) |
| 10 | ي | Yāʾ | 10 | tens | ten coefficient 1 |
| 11 | ك | Kāf | 20 | tens | ten coefficient 2 |
| 12 | ل | Lām | 30 | tens | ten coefficient 3 |
| 13 | م | Mīm | 40 | tens | ten coefficient 4 |
| 14 | ن | Nūn | 50 | tens | ten coefficient 5 |
| 15 | س | Sīn | 60 | tens | ten coefficient 6 |
| 16 | ع | ʿAyn | 70 | tens | ten coefficient 7 |
| 17 | ف | Fāʾ | 80 | tens | ten coefficient 8 |
| 18 | ص | Ṣād | 90 | tens | tens terminal \(90\) |
| 19 | ق | Qāf | 100 | hundreds | hundred coefficient 1 |
| 20 | ر | Rāʾ | 200 | hundreds | hundred coefficient 2 |
| 21 | ش | Shīn | 300 | hundreds | hundred coefficient 3 |
| 22 | ت | Tāʾ (light T) | 400 | hundreds | hundred coefficient 4; distinct from Ṭāʾ |
| 23 | ث | Thāʾ | 500 | hundreds | hundred coefficient 5 |
| 24 | خ | Khāʾ | 600 | hundreds | hundred coefficient 6 |
| 25 | ذ | Dhāl | 700 | hundreds | hundred coefficient 7 |
| 26 | ض | Ḍād | 800 | hundreds | hundred coefficient 8 |
| 27 | ظ | Ẓāʾ | 900 | hundreds | hundreds terminal \(900\) |
| 28 | غ | Ghayn | 1,000 | thousands | Ghayn return anchor |

The letter identities and native weights are exactly the 28 declarations of the registry source artifact. **Ṭāʾ ط=9 and Tāʾ ت=400 are separate registers.** The glottal **hamza** is a separate spelling/annotation dimension in this 28-entry profile; hamza-bearing alif forms are not silently identified with bare ا, and no additional numerical value is invented for ء.

A natural letter, a form written on the page, its native weight, its pronunciation, its etymology, and a computational operator are distinct typed fields. A letter is not automatically a machine instruction.

## 2. The periodic address law: the table folds without losing the address

Let \(U_d\) be the unit glyph for coefficient \(d\in\{1,\dots,9\}\), \(T_d\) the tens glyph, and \(H_d\) the hundreds glyph. Define:

\[
L(p,d)=
\begin{cases}
U_d,&p=0,\\
T_d,&p=1,\\
H_d,&p=2,\\
\mathrm{GHAYN},&p\ge3,\ p\bmod3=0,\ d=1,\\
U_d,&p\ge3,\ p\bmod3=0,\ 2\le d\le9,\\
T_d,&p\ge3,\ p\bmod3=1,\\
H_d,&p\ge3,\ p\bmod3=2.
\end{cases}
\]

**Critical identity:** \(R(L(p,d))\) is a *native letter weight*, while \(V(p,d)=d10^p\) is the *actual value held at place \(p\)*. For example, Bāʾ has native weight 2 but at place 3 with coefficient 2 its contextual value is 2,000. This is an intended multi-typed registry, not a contradiction.

| Decimal region | Place index | Registered coefficient range | 1st coefficient | 9th coefficient |
|---|---:|---|---|---|
| units | 0 | 1–9 | 1 → ا | 9 → ط |
| tens | 1 | 10–90 | 10 → ي | 90 → ص |
| hundreds | 2 | 100–900 | 100 → ق | 900 → ظ |
| thousands | 3 | 1,000–9,000 | 1,000 → غ | 9,000 → ط |
| ten-thousands | 4 | 10,000–90,000 | 10,000 → ي | 90,000 → ص |
| hundred-thousands | 5 | 100,000–900,000 | 100,000 → ق | 900,000 → ظ |
| millions | 6 | 1,000,000–9,000,000 | 1,000,000 → غ | 9,000,000 → ط |
| ten-millions | 7 | 10,000,000–90,000,000 | 10,000,000 → ي | 90,000,000 → ص |
| hundred-millions | 8 | 100,000,000–900,000,000 | 100,000,000 → ق | 900,000,000 → ظ |
| billions | 9 | 1,000,000,000–9,000,000,000 | 1,000,000,000 → غ | 9,000,000,000 → ط |

Thus the **repeat unit** has period three *positions* after the original lower register sequence. Absolute place \(p\), not just \(p\bmod3\), is necessary to recover numerical magnitude. The special Ghayn return at \(p=3,6,9,\dots\) implements the owner's **ALIF-skip rule**: the first coefficient at a high unit-like band uses Ghayn, reserving Alif for 1 at the original low unit place.

The strict positional tape for a nonnegative integer \(n\) is its unique base-ten coefficient sequence \((d_m,\dots,d_0)\), each \(0\le d_p\le9\), with \(d_m\ne0\) for \(n>0\). Each nonzero \(d_p\) emits the tagged token \(\langle p,d_p,L(p,d_p)\rangle\); each zero emits a typed ṢIFR cell. The number 0 itself is represented by a single **numeric ṢIFR zero** at \(p=0\). All positions through \(p=0\) are represented explicitly in a canonical serialized tape.

### Concrete addresses

- **9:** \([0:9:\text{ط}]\).
- **10:** \([1:1:\text{ي},\,0:\text{ṢIFR}]\).
- **109:** \([2:1:\text{ق},\,1:\text{ṢIFR},\,0:9:\text{ط}]\).
- **190:** \([2:1:\text{ق},\,1:9:\text{ص},\,0:\text{ṢIFR}]\).
- **999:** \([2:9:\text{ظ},\,1:9:\text{ص},\,0:9:\text{ط}]\).
- **1,000:** \([3:1:\text{غ},\,2:0,\,1:0,\,0:0]\).
- **2,000:** \([3:2:\text{ب},\,2:0,\,1:0,\,0:0]\).
- **9,000:** \([3:9:\text{ط},\,2:0,\,1:0,\,0:0]\).
- **10,000:** \([4:1:\text{ي},\,3:0,\,2:0,\,1:0,\,0:0]\).
- **100,000:** \([5:1:\text{ق},\,4:0,\dots,0:0]\).
- **1,000,000:** \([6:1:\text{غ},\,5:0,\dots,0:0]\).

In these examples an unlabelled **0** in a tape list is shorthand for a zero-coefficient cell with a declared ṢIFR gap role, never an additional letter. The electronic binary number 1000₂ equals eight; the decimal address 1000₁₀ equals one thousand. They are never silently conflated.

### The four foundational tape forms and their infinite lift

The owner's **1,000 as confirmation of four tape forms** is modeled by a finite register *type* system, not by claiming that 1,000 equals an ordinary 4-digit Boolean word.

| Form ID | Place | Native register family | Entrance or exit |
|---|---:|---|---|
| \(\mathcal T_1\) | \(p=0\) | Alif through Ṭāʾ | 1 initiates; 9 terminal |
| \(\mathcal T_2\) | \(p=1\) | Yāʾ through Ṣād | 10 initiates; 90 terminal |
| \(\mathcal T_3\) | \(p=2\) | Qāf through Ẓāʾ | 100 initiates; 900 terminal |
| \(\mathcal T_4\) | \(p=3\) | Ghayn anchor with Bāʾ–Ṭāʾ coefficient continuation | 1,000 initiates the 3-place return cycle |

For all higher places, repeat the *band types* \(\mathcal T_1,\mathcal T_2,\mathcal T_3\), while Ghayn specifically replaces high-order coefficient-1 ALIF at \(p\equiv0\pmod3\). Thus the fourth tape is a **return/confirmation gate** and the higher-index register families are reusable. That convention is a proposed new operation profile; it is not a claim about historically standard Arabic notation.

### A deterministic reference encoder

~~~text
encode_nonnegative_integer(n, profile="QITT/0.1"):
  reject non-integer and n < 0
  if n == 0: return [Cell(place=0, coefficient=0, role=SIFR_ZERO)]
  cells = []
  p = 0
  while n > 0:
    digit = n mod 10
    if digit == 0:
      cells.append(Cell(p, 0, SIFR_GAP, glyph=none))
    else:
      cells.append(Cell(p, digit, LETTER, glyph=L(p,digit)))
    n = floor(n/10)
    p = p+1
    if p > maximum_places: RESOURCE_LIMIT
  return reverse(cells) with exact place tags and registry version

decode_typed_address(cells):
  check consecutive place tags, high-to-low, final place 0
  check SIFR role and every nonzero glyph L(place,coefficient)
  return sum(coefficient * 10^place for each cell)
~~~

The encoder and decoder are **algorithms specified in this paper**, not evidence that an interpreter binary is installed. The number of output cells is linear in decimal digit length. The 28 native registry symbols are reused; no additional Unicode glyph is minted when the tape expands.


## 3. ṢIFR: an operator-capable absence and holding type

**Axiom CALRC-Z1.** ṢIFR is a family of *typed cell conditions*, not a single scalar value:

\[
Z=\{\operatorname{GAP},\operatorname{ZERO},\operatorname{HOLD}_{operand},
\operatorname{HOLD}_{operator},\operatorname{RESERVED}\}.
\]

- **GAP:** position exists and contributes coefficient 0 in an otherwise populated address.
- **ZERO:** canonical representation of the number zero itself.
- **HOLD_operand:** a declared operand destination awaiting a typed value; not equal to numerical zero.
- **HOLD_operator:** a temporary site for an operation token with guard and lifetime; not equal to numerical zero.
- **RESERVED:** a continuation/return position held open for a later lawful transition.

State must carry at least \((p,\mathrm{role},\mathrm{occupancy},\mathrm{payload},\mathrm{generation})\). The *logical occupancy bit* may be zero while the software representation contains metadata; logical zero does not imply zero bytes in RAM.

**Binding grammar.**

\[
\mathrm{HOLD}_{operand}\xrightarrow{\operatorname{bind}(x)}
\mathrm{BOUND}(x)\xrightarrow{\operatorname{release}}\mathrm{HOLD}_{operand}.
\]

\[
\mathrm{HOLD}_{operator}\xrightarrow{\operatorname{bind}(\omega)}
\mathrm{ARMED}(\omega)\xrightarrow{\operatorname{execute}(args)}
\mathrm{RESULT}(\omega,args)\xrightarrow{\operatorname{release}}\mathrm{HOLD}_{operator}.
\]

A reserved place may acquire coefficient 1 via an explicitly guarded **0→1 logical flip**, but the coefficient 1 has no implicit glyph until **\(p\)** is known. At \(p=0\) the glyph is Alif; at \(p=3\) and \(p=6\) it is Ghayn. This precisely separates the owner's Alif-in-Sifr/bit-flip image from an invalid assumption that every logical 1 must print Alif.

**Undefined, missing, empty, false, numeric zero, uninitialized storage, and ṢIFR operand-holder are separate semantic types.** No coercion between them exists unless an explicit transition is registered.

## 4. LIFF, GHAYN and the arithmetic/bit transition laws

**LIFF** is adopted as the owner's named *turn, wrap, and carry* operator. Etymological and historical claims about the name ALIF or LIFF are not necessary to define its mathematical behavior.

For decimal successor \(S(n)=n+1\), begin with an increment of the units coefficient, then perform the following local decimal carry rewrite while the active coefficient equals 10:

\[
(\dots,d_{p+1},10,d_{p-1},\dots)
\xrightarrow{\mathrm{LIFF}_p}
(\dots,d_{p+1}+1,0,d_{p-1},\dots).
\]

A fresh most-significant cell is allocated when carry leaves the existing tape. At each step the numeric invariant \(\sum_p d_p10^p\) is preserved across the carry rewrite because \(10\cdot10^p=1\cdot10^{p+1}\). The original increment increases the total by 1. After canonicalization, glyph projection is recalculated under \(L\).

Examples:
- **9→10:** Ṭāʾ at \(p=0\) becomes ṢIFR at \(p=0\), while Yāʾ activates at \(p=1\).
- **99→100:** terminal units and tens return to ṢIFR, Qāf activates at \(p=2\).
- **999→1,000:** Ṭāʾ, Ṣād and Ẓāʾ all release into ṢIFR; Ghayn activates at \(p=3\).
- **1,999→2,000:** Ghayn's high-place coefficient 1 advances to coefficient 2, emitted Bāʾ at \(p=3\); lower slots become ṢIFR.
- **999,999→1,000,000:** a new place \(p=6\) activates Ghayn again.

**GHAYN_RETURN** recognizes \(p\in\{3,6,9,\dots\}\) with coefficient 1, preserving the absolute place and cycle count. It is a *return projection*, not an arithmetical decrement or deletion of thousands.

**FLIP** changes a declared Boolean occupancy bit by XOR with one. FLIP is not decimal ADD, and LIFF is not XOR: injection, carry propagation and assignment must retain separate traces. These distinctions follow the PHANTOM/SURFACE source-encoding boundary.

### The requested 4-bit temporal motif

The owner's explicit formation trace is:

\[
0000\rightarrow1000\rightarrow1100\rightarrow1110\rightarrow1000.
\]

Define named states \(\mathrm{VOID}\), \(\mathrm{MARK_1}\), \(\mathrm{MARK_2}\), \(\mathrm{MARK_3}\), and \(\mathrm{RETURN_1}\). Here both MARK_1 and RETURN_1 *render* 1000 but are distinguished by history/generation. The transitions are:
1. VOID → MARK_1 on ACTIVATE.
2. MARK_1 → MARK_2 on GROW.
3. MARK_2 → MARK_3 on GROW.
4. MARK_3 → RETURN_1 on RETURN.
5. RETURN_1 → MARK_2 on GROW in the next cycle.

This is a **finite control path over bit masks**, not the binary count sequence 0,8,12,14,8 interpreted as numerical successor. No unshown 1111 step is inserted. If hidden history is quotiented out, the visible graph has an incoming edge to a 3-cycle. This distinguishes a return operation from a conventional bitwise increment.

### Ten as a terminal transition and the owner's "00" formation

The owner also describes the move after the nine unit forms as **"00"** rather than treating "ten" as a mere static verbal number. CALRC retains this as a **temporal two-ṢIFR formation annotation**, not as the decimal numeral 00. The canonical numeric value ten remains \(1\cdot10^1+0\cdot10^0=10\), while the *transition history* includes **CLEAR(terminal-unit)**, **HOLD(lower-address)** and **ACTIVATE(tens-register-1 = ي)**. A two-slot state rendering "00" may represent two temporarily unbound holdings at the turning boundary, under a separately declared DUAL_SIFR control profile. It is neither 0₂ nor 0₁₀ and cannot replace the completed address of 10.

The subsequent move **10→11** activates Alif in the low unit place while Yāʾ remains at the tens place. This preserves the owner's empty-then-one bit-activation account without reinterpreting the mathematical value of ten. The precise time order of those intermediate two holdings is **proposed/open** until a compiler transition specification is independently implemented.

### Algebraic formation of a word

A word \(w\) determines an occurrence vector \(c(w)\in\mathbb N_0^{28}\) counting each registered glyph. With weight vector \(r=(1,2,\ldots,9,10,\ldots,90,100,\ldots,900,1000)\), the additive value is the linear functional \(A(w)=r^\top c(w)\). This exposes exactly what numerical projection forgets: **the order of the letters**. For instance قط and طق each project to 109, though they are different ordered words. Their ordered programs may have different semantics even when the occurrence vectors agree. A morphology or operation compiler must therefore carry both **sequence/order** and **numeric address**.

This resembles the role of a typed composition grammar in chemical nomenclature: a compositional name and a formula may each encode structure, but no formula or sum automatically specifies the full ordered molecular graph. The comparison is one of **representation layers and reverse-lookup loss**, not a claim that Arabic morphology and chemistry use identical scientific operators.


## 5. Words as profiled programs: two through nine letters

Let \(W_n=\Sigma_{28}^n\) for \(2\le n\le9\). The owner's *program-form laboratory* has domain

\[
W_{2:9}=\bigcup_{n=2}^9W_n.
\]

These are **formal candidate programs**, not a claim that natural Arabic roots have every one of these lengths. Natural-language morphology is separately modeled through roots, templates, affixes, vowels, orthography, source period and variety.

Each word \(w=\ell_1\cdots\ell_n\) can carry:
1. **Raw form:** original UTF-8 source string and source span.
2. **Grapheme form:** letter tokens and diacritics under a named normalization policy.
3. **Root/template form:** optional morphology analysis with evidence and language profile.
4. **Native additive value:** \(A(w)=\sum_{i=1}^{n}R(\ell_i)\) under the bare-grapheme profile.
5. **Positional address:** \(\operatorname{encode}(A(w))\), an address of the value, not a lossless reconstruction of the spelling.
6. **Operator program:** only if an explicit interpretation \(\mathcal I(w)\) is declared with typed inputs, outputs, transition constraints and provenance.

Thus \(A(uv)=A(u)+A(v)\) makes \(A\) a monoid homomorphism from word concatenation to nonnegative integer addition, but **not an injective code** and not by itself an interpreter.

### QITṬ and QAṢ examples

**QITṬ** as bare graphemes **قط** is \(R(\text{ق})+R(\text{ط})=100+9=109\). Its positional address is Qāf at place 2, ṢIFR at place 1 and Ṭāʾ at place 0. A dedicated QITṬ boundary annotation may designate this pattern as **hundreds-entry + absent tens + units-terminal**. That is a newly specified operator role. Its numeric value remains 109.

The vowelled/shadda spelling **قِطّ** must be source-preserved. If a separately opted-in **shadda-expanded** profile counts the doubled Ṭāʾ, the resulting additive value is \(100+9+9=118\); the owner's 109 exemplar belongs to the **bare grapheme** profile. Neither profile silently overwrites the other.

**QAṢ** as **قص** is \(100+90=190\). A specifically constructed **QAṢ | QAṢ** program, with graphemic sequence **قصقص**, has value \(190+190=380\). By contrast, **قصص** has the distinct three-letter sequence Qāf–Ṣād–Ṣād, \(100+90+90=280\). Including the definite article, **القصص** is \(1+30+100+90+90=311\) under the same additive profile. These values are different precisely because an operator-concatenation hypothesis is not identical to spelling. The owner's reference to Qur'an surah 28 is retained as an interpretive research locus, not evidence that this grammar historically encoded that chapter.

A **program** also need not be its own canonical numeral. The word **قصقص** has additive value 380, while the standard positional tape for 380 projects to **ش** at hundreds and **ف** at tens. The source word is retained through a provenance-bearing mapping:

\[
w\xrightarrow{\mathrm{native\ value}}A(w)
\xrightarrow{\mathrm{positional\ encode}}\operatorname{Addr}(A(w)).
\]

The reversed arrow from value to *original source word* is not a function without additional information.

## 6. Formal syntax, typing and operational semantics

The machine-readable syntax is [QITT-0.1.ebnf](QITT-0.1.ebnf). Its design recognizes four categories: **WORD**, **ADDR**, **TAPE**, **APPLY**, with **BOUNDARY** and **CONTROL** extensions. The parser produces typed AST nodes; it never treats untrusted Arabic source text as an executable shell/program statement.

Representative language:

~~~text
QITT/0.1 PROFILE bare_graphemes
WORD "قط"
ADDR 109
TAPE [2:1:LETTER:ق;1:0:SIFR_GAP:_;0:9:LETTER:ط]
APPLY LIFF TO ADDR 999
BOUNDARY QITT ON "قط"
CONTROL 0000 ACTIVATE
CONTROL 1000 GROW
CONTROL 1100 GROW
CONTROL 1110 RETURN
~~~

These lines are **specification fixtures**; a complete QITT language parser/interpreter is not claimed as installed.

**Typing and judgment forms:**

\[
\Gamma\vdash w:\mathrm{Word}(\mathrm{profile},n),\quad2\le n\le9,
\]

\[
\Gamma\vdash (p,d,L(p,d)):\mathrm{NonzeroCell},
\qquad
\Gamma\vdash(p,0,z):\mathrm{SifrCell}(z),
\]

\[
\Gamma\vdash T:\mathrm{CanonicalAddress}(n)
\iff \operatorname{decode}(T)=n
\text{ and the cell invariants hold.}
\]

\[
\Gamma\vdash\omega:\mathrm{Operation}(A\to B,effects,guards),
\qquad
\Gamma\vdash\langle s,\omega\rangle\to s'
\text{ only when guard}(s,\omega).
\]

Declared arithmetic, glyph normalization, morphological analysis, and permission-bearing mutable state are never implicitly unified. Proof obligations accompany all grammar rewrites: type preservation, valuation preservation where stipulated, admitted source profile and resource budget.

**Admissibility is separate from syntax.** The structurally admissible language of a word program is \(G\); its interpretation is the labelled transition relation \(\llbracket\cdot\rrbracket\) over a carrier state. This follows the separation of structure, move signature, admissibility, semantics, encoding and cost already used in Computational Grammar Theory. Grammar in Numbers supplies a compatible warning that numerals, numbers, machine states and representations are not interchangeable.

## 7. The mathematical formation engine and its proofs

**Definition 1 — Canonical encoder.** \(\operatorname{encode}(n)\) computes the finite decimal expansion of \(n\in\mathbb N_0\), stores every coefficient with absolute position and corresponding ṢIFR or \(L(p,d)\) symbol, and retains registry/profile/version IDs.

**Definition 2 — Decoder.** \(\operatorname{decode}(T)=\sum_{p=0}^{m}d_p10^p\) for a well-typed canonical tape.

**Proposition P1 — Completeness of primary registry.** The 28 declared native values occupy exactly nine units, nine tens, nine hundreds and one thousands anchor; every native value appears once. Proof: enumeration by the pair (band,coefficient), with Ghayn in its own band.

**Proposition P2 — Contextual glyph determinism.** At fixed place \(p\), the mapping \(d\mapsto L(p,d)\) for \(1\le d\le9\) is injective; the nonzero coefficient at a fixed place can be recovered from its glyph when \(p\) is retained. Proof: the selected nine-symbol band at each place contains no duplicate glyphs.

**Proposition P3 — Exact round trip of typed addresses.**

\[
\forall n\in\mathbb N_0:
\quad\operatorname{decode}(\operatorname{encode}(n))=n.
\]

Proof: uniqueness of base-ten positional expansion; the lifted letter token is a second coordinate that does not alter the coefficient or place.

**Proposition P4 — Noninvertibility of stripped spelling.** If \(\pi_{\mathrm{glyph}}\) drops positions and zero cells, then \(\pi_{\mathrm{glyph}}(\operatorname{encode}(2))=\text{ب}\) and \(\pi_{\mathrm{glyph}}(\operatorname{encode}(2000))=\text{ب}\); 1,000 and 1,000,000 both project to غ. Therefore \(\pi_{\mathrm{glyph}}\circ\operatorname{encode}\) is not injective. **A complete address requires its positional lift/cycle tape.**

**Proposition P5 — Carry consistency.** A LIFF carry rewrite preserves \(\sum d_p10^p\). Together with the initial +1 injection, successor raises that value by exactly one. Proof: \(10\cdot10^p=10^{p+1}\), applied to each overflowing digit.

**Proposition P6 — Word valuation homomorphism.** Under a fixed grapheme-counting profile, \(A(uv)=A(u)+A(v)\); this follows from splitting the finite sum across the concatenation boundary.

**Counterexample C1 — No unique word from value.** **قص** and **قفي** both have native additive value \(190\): \(100+90=190\) and \(100+80+10=190\). Their spellings and word lengths differ. Hence the additive value is not a reversible natural-language encoder.

**Counterexample C2 — No auto-conversion of shadda.** قِطّ has 109 under bare-grapheme weighting and 118 under doubling of pronounced Ṭāʾ. A profile selection is necessary.

**Counterexample C3 — No arithmetic meaning from bit-mask succession.** Mask 1110₂ to 1000₂ is a decrease from 14 to 8 when read numerically; it is a RETURN transition in the control grammar. These are different interpretations of the same glyphs.

**Counterexample C4 — No single universal operator meaning for QITṬ.** Numerically 109 is not a hundreds terminal (900 is). QITṬ can designate a *composite path boundary* when declared; it cannot be inferred to be the end of all numbers or programs.

**Open proof obligations:** relational equivalence between distinct word programs; source-specific morphology; semantics of owner-claimed Arabic compositional meanings; normalization laws for hamza/alif variants; canonical order of operands when letters become operators; admission of any quantum-channel model; invertibility when a sideband is compressed.

## 8. Topological substrate: cyclic registry, tape tree and return paths

A "circle" must be stated as a structure, not inferred from an attractive visual arrangement. We provide several distinct topological objects:

**T1. Registry ring:** Add edges in the declared native numeric order, including an edge from Ghayn back to Alif. The geometric realization of this explicitly chosen graph is \(C_{28}\), a circle-like one-dimensional CW complex. It has 28 vertices and 28 edges, \(\beta_0=1,\beta_1=1\), and \(\pi_1\cong\mathbb Z\). If no edges are declared and the 28 glyphs are a discrete set, \(\beta_0=28,\beta_1=0\). The topology depends on the edge declaration, not the word "alphabet."

**T2. Period-three register base:** Beyond place 2, the phase \(\varphi(p)=p\bmod 3\) takes values in a three-state cycle \(C_3\). Absolute \(p\) is a lift of the phase; \(\lfloor p/3\rfloor\) distinguishes repeat excursions. The ray \(p\ge3\) has a boundary, so we call it a *directed phase lift* rather than claiming it is globally a covering space. A formal bi-infinite extension \(p\in\mathbb Z\) may be used when a true periodic covering model is useful, provided the restriction back to valid addresses is declared.

**T3. Address trie:** Decimal digit strings form a rooted prefix tree, with zero-bearing slot nodes if positional fidelity is needed. Any finite subtree is contractible (as a graph); its first homology is zero. Adding return edges creates cycles and changes that invariant. Numeric closeness, common string prefix and metric distance are three different relations.

**T4. Fibers of forgetful projections:** The projection from typed tape to visible glyph sequence has nontrivial fibers. For example, the fiber above one Bāʾ contains at least the encodings of 2, 2,000 and 2,000,000,000. A *fiber* is a set of preimages, not automatically a smooth fiber bundle. Recording the absolute place is a section choice for reconstructing an individual typed address.

**T5. Quotients and equivalence:** Quotienting tapes by native glyph projection merges distinct values and destroys the possibility of a well-defined decoder. An operator may descend to a quotient only if it respects the equivalence relation: \(x\sim y\Rightarrow F(x)\sim F(y)\). This congruence obligation matters for CALRC reverse computation and PolyIA canonicalization.

**T6. Temporal return topology:** The visible mask-transition graph has vertices 0000, 1000, 1100, 1110 and edges 0000–1000–1100–1110–1000. Its underlying undirected graph has \(|V|=4, |E|=4\), hence \(\beta_1=|E|-|V|+1=1\). The same rendered 1000 has distinct event generations. The graph's loop does not imply any physical waveform or quantum coherence.

**T7. Higher constructions:** A simplicial or cubical complex over concurrent register/control/morphology regions may be introduced only by declaring which compatible transitions form faces. Homology depends on those faces. Products of independently active automata are statechart products; concurrency does not on its own imply geometric dimension or a smooth manifold.

**T8. Topological research program:** Inspect graph connectivity, cycles, homology, induced maps under projections, kernel/fiber, covering/lifting, group actions, quotient congruence, automaton product complexes, persistent topology under bounded perturbations, and typed boundaries. These are *applicable mathematical questions*; only T1–T6 above have the specifically stated finite derivations.

This permits a Glass Atlas to present a 28-position visual ring and a cyclic 3-band register without suggesting those pictures are proofs of historical composition.

### PHANTOM and complex-plane phase charts, with address fidelity

The owner's picture of a return tunnel can be projected into a complex-plane chart without claiming an underlying quantum process. For \(p\ge3\), let \(k=\lfloor(p-3)/3\rfloor\), \(j=(p-3)\bmod3\), and define a *display coordinate*

\[
z(p)=(1+k)\exp(2\pi i j/3).
\]

The three phases of each cycle occupy equally spaced angles, and the next return increases radius while returning to phase angle zero: \(p=3\mapsto1\), \(p=4\mapsto e^{2\pi i/3}\), \(p=5\mapsto e^{4\pi i/3}\), \(p=6\mapsto2\). The ordered pair \((k,j)\), hence this discrete chart at fixed origin, identifies a high-place index uniquely. This is a **scale-preserving lift** of the three-phase projection. Drawing every \(z(p)\) on a single unit circle instead would collapse all the periods and lose the magnitude address.

A sum of complex coordinates over several occupied places need not uniquely identify the whole tape. The renderer must preserve the **indexed cell set** even if it displays the weighted points. This chart may be consumed by PHANTOM/SURFACE as a typed visualization after adaptation; it is not an assertion of amplitude, measured phase, Fourier spectrum, electric potential, or quantum hardware addressing.

### Topological domain coverage register

**Point-set topology:** explicit choice of discrete vertex sets, graph realizations, product spaces and continuity; topology is not inferred from printed ring geometry. **Graph/CW topology:** cycle, trie, edge attachments and Euler characteristic. **Algebraic topology:** path-connected components, fundamental group, cellular homology, homotopy equivalence and induced maps. **Covering/lifting:** three-phase lift with absolute-place sideband, with boundary qualification. **Quotient and fiber topology:** identified glyphs, nontrivial preimage classes, failure of quotient-descended decoding. **Order/Alexandrov topology:** optional address-prefix partial order, requires an explicit open-set convention. **Topological dynamics:** periodic phase and history-sensitive transition, distinct from numeric successor. **Computational topology/TDA:** finite complexes and persistent homology under declared perturbations are future probes, not completed measurements. **Differential topology/geometry, manifold theory, sheaves/cohomology and spectral sequences:** not established for this discrete registry; any future use must introduce suitable spaces, maps and exact evidence rather than borrow their terminology as proof.


## 9. Algebra, groups, categories, computation and limits

- **Algebraic substrate:** \((\mathbb N_0,+,0)\) is the numeric monoid; \((\Sigma_{28}^*,\cdot,\epsilon)\) is the free word monoid; \(A\) is a monoid homomorphism under a fixed additive profile. Decimal digit tapes carry their canonical arithmetic interpretation.
- **Group action:** the phase class \(\mathbb Z/3\mathbb Z\) acts on the abstract high-order band labels by rotation. It does *not* automatically act on numerical values without also transforming scale; shifting an address place by 3 multiplies a nonzero positional component by 1,000.
- **Semigroup of operations:** BIND, RELEASE, LIFF, and RETURN generally include partial or many-to-one behavior. Do not call this a group unless the chosen operation family satisfies closure and invertibility.
- **Category-oriented formulation:** typed registers/tapes/words may be objects and admitted translations/encodings may be morphisms. Composition and identity laws must be proved for the chosen category; encode-to-value and source-word inverse are not automatic isomorphisms.
- **Information theory:** positions and absent cells cannot be discarded while claiming perfect reconstruction; the observed many-to-one projection requires enough side information to select a fiber member.
- **Type theory:** an alias glyph is not an equality of typed cells. ALIF at \(p=0\), GHAYN at \(p=3\), and Boolean 1 are different inhabitants of different types.
- **Arithmetic complexity:** constructing a canonical tape requires \(\Theta(k)\) output symbols for \(k\) decimal places, with arithmetic cost depending on the arbitrary-precision integer model; local LIFF carry visits at most \(k+1\) positions.
- **Resource contract:** up to 1,024 decimal places, two-to-nine-letter source-program words, 4,096 recorded operator trace events per bounded session, exact nonnegative integer semantics. Resource exhaustion returns UNKNOWN/RESOURCE_LIMIT, never a fabricated proof.
- **Scientific basis:** no physical quantum state is inferred from the shape of a letter or the appearance of a Boolean bit. Quantum compilation is separately typed and requires explicit state/channel/basis/measurement contracts.

## 10. Full mathematical rake: the 23 SURFACE domains

The ordered domain IDs follow SURFACE's mathematical atlas. These are **review questions**, not claims that all 23 domains have been exhaustively solved.

| Domain ID | CALRC obligation / present scope |
|---|---|
| logic | Formal guards; syntax/semantic judgments; decidable local cell typing |
| set_theory | Finite 28-element set, digit set, word families and infinite address domain |
| type_theory | Distinct raw glyph, numeric value, tagged place, ṢIFR and operation types |
| arithmetic | Exact positional valuation, increment, carry, borrow and decimal/binary separation |
| algebra | Free word monoid, additive homomorphism, partial-operation semigroup |
| order_lattices | Numeric order distinct from glyph order and occupancy-information partial order |
| combinatorics | Formal words of lengths 2–9 and bounded legal traces; no claim about natural-language frequency |
| graph_theory | Registry cycle, phase cycle, address trie and control transition graph |
| automata_languages | EBNF, semantic guards, typestate, concurrent finite control |
| information_coding | Loss of glyph-only projection; source, position and profile sidebands |
| geometry | Visual embedding of register graph is chosen layout, not underlying metric evidence |
| topology | Ring/trie/phase/homology/quotient/fiber/return computations §8 |
| analysis_calculus | Discrete difference/successor; continuous derivatives not applicable without an extension |
| differential_equations | Not applicable to the present exact digit grammar without a declared dynamical model |
| spectral_harmonic | A formal three-phase periodic sequence may admit Fourier analysis; no physical spectrum inferred |
| probability_statistics | Applicable only to later sourced word/corpus distributions and uncertainty |
| optimization_control | Bounded minimal tape or grammar encodings; no global optimality asserted |
| numerical_analysis | Exact base-ten arithmetic; future approximate embeddings need error contracts |
| category_composition | Typed maps, functor candidates, quotient descent/congruence checks |
| physics_units | Not applicable to the registry alone; no force or temperature assigned to glyphs |
| quantum_information | Separate optional mapping; no qubit or quantum channel assertion |
| computation_complexity | Tape/output bounds, determinism, parser cost and operator trace budgets |
| metrology_uncertainty | No physical measurement asserted; future linguistic corpus alignment needs provenance and confidence |

## 11. GLASS Oracle and repository interface contracts

**GLASS / Substrate University:** The project owns the CALRC namespace, the public/private source boundary, a 28-entry canonical data registry, grammar/profile version IDs, proof obligations, typed relations and commission records. Register language, mathematics, and topology links in the Atlas without rewriting inherited University divisions. The existing native journal predeclares intents, applies concurrent regional transitions and publishes durable units on main.

**Computational Grammar Theory:** Reuse its separation of syntax, admissibility, relation semantics, state representation and cost profiles. Treat letter-address rewriting as an operational grammar over an explicitly represented tape, not as numeric folklore.

**Grammar in Numbers:** Reuse the distinction among mathematical number, numeral, symbol, arithmetic operation and machine execution. CALRC augments a canonical base-ten representation with a cyclic, typed glyph projection; it does not change the arithmetic value of ten.

**PolyIA:** Its pinned source provides finite typed alphabet/index structures and serialization (polyia/forms.py), bounded grammar cards and generators (polyia/generators.py), and a pure compiler/stack VM with separate AST evaluation (polyia/native.py). An adapter may register QITT/0.1 as a new, bounded alphabet and operational grammar **without modifying the preserved originals or claiming universal program synthesis**. Generate grammar cards for each \(\Sigma_{28}\) band, lift law, typed ṢIFR transitions, and proof/negative fixtures.

**PURL:** Represent a CALRC registry as a typed versioned resource; expose safe read-only state/address/manifest projections with GET, and durable BIND/LIFF/RELEASE operations through authorized POST operations and idempotent receipts. No new mutation-on-GET behavior is introduced. Existing PURL paths and rights remain authoritative.

**SEURL:** Preserve its independent URL-only state-machine grammar and namespace. CALRC may be carried as a typed payload/transition observation through an explicit bridge; neither protocol is silently redefined.

**SURFACE / PHANTOM / Quantum Oracle:** Treat the decimal digit tape, encoded bytes, bit-mask control, basis index and logical qubit ID as different types. SURFACE's actual native renderer consumes admissible computed fields only through adapters. The current CALRC package supplies mathematical descriptions, **not a deployed native renderer, physical experiment or demonstrated quantum advantage**.

**SNAD / Qur'anic research:** Source spellings, verses, morphology sources, qirāʾāt and interpretation are versioned separately. A numeric registry address is an additional projection; it cannot overwrite exact Qur'anic text or establish speaker intent or theological meaning.

**GLASS Hermes / Agency / Atlas:** Candidate oracles are structured services: REGISTER, PARSE, ADDRESS, INVERT-FIBER, LIFF, MORPH-PROFILE, TOPOLOGY, and PROVENANCE. Hermes may dispatch an oracle only through a registered contract, fixed resource budget and observable evidence; it does not promote an unproved linguistic hypothesis by replaying a self-authored example.

### Oracle/operator transition signature

| Operation | Input type | Output type | Guard and invariant |
|---|---|---|---|
| REGISTER | base glyph + source profile | native register ID/weight | only declared 28 glyphs; raw source retained |
| ADDRESS | exact nonnegative integer | canonical typed tape | digit bound and value round trip |
| PROJECT | tagged tape | visible glyphs + loss receipt | never claims reversible projection |
| INVERT_FIBER | visible glyphs + constraints | finite candidate tapes / UNKNOWN | requires place/cycle bounds; no unique answer implied |
| SIFR_ALLOCATE | fresh place + role | typed empty cell | GAP, ZERO, holder and reserved differ |
| BIND / RELEASE | typed holder and payload | bound/unbound holder | declared compatible type and generation |
| LIFF | canonical tape + increment event | canonical successor tape | carry is base-ten; atomic event receipt |
| GHAYN_RETURN | place \(3k\), \(k\ge1\), coefficient 1 | annotated Ghayn cell | absolute place/cycle unchanged |
| QITT_BOUNDARY | profiled token sequence + frame | boundary annotation or refusal | no automatic interpretation of ordinary words |
| BIT_FLIP | declared Boolean occupancy | toggled occupancy | neither integer add nor quantum gate by default |
| CONTROL_RETURN | MARK_3 mask state | RETURN_1 mask state | 1110→1000; generation increments |
| MORPH_PROFILE | exact source text + sourced profile | profiled tokens/analysis or UNKNOWN | no unsupported roots/definitions invented |
| TOPOLOGY_PROJECT | declared graph and face contract | combinatorial complex/invariants | no spatial/physical claims from layout |

These services are proposed as small pure or explicitly effect-typed **GLASS oracles**. Their adapters need observable tool receipts, independent replay and bounded resource contracts before runtime promotion. The oracle's product is a **typed mathematical witness or a classified refusal**, not a self-certified discovery.


## 12. Proposed source-facing address interface

Within an existing PURL server, the *proposed* CALRC resource would be addressable with routes such as:

~~~text
GET  /r/{id}/manifest
GET  /r/{id}/qitt/registry
GET  /r/{id}/qitt/address?decimal=109
GET  /r/{id}/qitt/word?profile=bare_graphemes&source_id=...
POST /r/{id}/ops/qitt-bind
POST /r/{id}/ops/qitt-liff
POST /r/{id}/ops/qitt-release
~~~

The route examples are **new adapter proposals** and not claims of existing deployment. A canonical address record would retain:

~~~text
protocol_id     QITT/0.1
registry_id     glass.qitt.registry/0.1
source_profile  bare_graphemes
decimal_value   109
cells           [2:1:LETTER:ق;1:0:SIFR_GAP:_;0:9:LETTER:ط]
cycle_tags      place 2/1/0, no high-cycle excursion
origin_ref      source word قط, preserved raw UTF-8
operator_scope  optional QITT_BOUNDARY; not inferred from the glyphs
~~~

This metadata also permits reversible recovery of the numerical address, while preserving the *word as a separate source object*.

## 13. Proof obligations, admission gates and publication status

The internal research statechart has concurrent regions:
**source-provenance**, **registry**, **grammar**, **operators**, **topology**, **integration**, **publication**. Declarations/intents precede effects, and actual publication has a separate receipt. Every observable error is preserved.

**Formal admission gates:**

1. **G1 / Alphabet:** exactly 28 unique glyph IDs, with the declared \(9+9+9+1\) native weights and proper Ṭāʾ/Tāʾ separation.
2. **G2 / Typed addressing:** every nonnegative in-scope integer has one canonical tagged tape and successful numeric round trip.
3. **G3 / Cyclic phases:** high-order lift obeys Alif-skip/Ghayn return and absolute-scale fidelity.
4. **G4 / ṢIFR:** no conflation of gap, zero, holder, missing or uninitialized.
5. **G5 / Word grammar:** bounded lengths; source spellings; opt-in diacritic/shadda/hamza rules; numeric value not mistaken for lexical meaning.
6. **G6 / Operations:** guards, resource bounds, admitted state transitions and replay witnesses.
7. **G7 / Negative controls:** raw glyph inversion ambiguity; 280/380 segmentation; 109/118 shadda profiles; 1110→1000 non-successor control.
8. **G8 / Topology:** topology only after graph/face declarations; homology and quotient relations with stated assumptions.
9. **G9 / Integration:** versioned PolyIA/PURL/SURFACE adapters without changing upstream semantics.
10. **G10 / Scientific status:** external history/novelty/linguistic or quantum claims remain unverified until separately commissioned.

**Actual status of this commission:** G1 has an authored full machine-readable registry; G2–G8 have formal definitions, derivations and explicit proposed fixtures; G9 is interface specification; G10 is an enforced evidentiary boundary. No code interpreter was installed, no scientific experimentation was performed, and no test suite/build was run for this writing commission. This text gives proof sketches, not machine-checked theorem proofs.

## 14. Source provenance and nomenclature

Source inspection was direct through the connected owner's GitHub repositories, **not through Google/web searching**. This writing commission read selected actual source/commission artifacts and used inherited GLASS inventory records; it does not claim every historical file in each repository was exhaustively inspected.

- [GLASS commission and statechart](GLASS_COMMISSION.md) and [native journal](../runtime/glass.hpp).
- [GLASS language profiles](../atlas/language-profiles.json) and [form contracts](../atlas/contracts.json).
- [SURFACE mathematical atlas](https://github.com/akadaan310/surface/blob/main/docs/MATHEMATICAL_ATLAS.md), [PHANTOM/PolyIA integration](https://github.com/akadaan310/surface/blob/main/docs/POLYIA_INTEGRATION.md).
- [PolyIA bounded forms](https://github.com/akadaan310/PolyIA/blob/bb6319acb88467b618f5a6f673f1867768223ce6/polyia/forms.py), [generators](https://github.com/akadaan310/PolyIA/blob/bb6319acb88467b618f5a6f673f1867768223ce6/polyia/generators.py), [compiler](https://github.com/akadaan310/PolyIA/blob/bb6319acb88467b618f5a6f673f1867768223ce6/polyia/native.py).
- [PURL specification](https://github.com/akadaan310/purl/blob/claude/purl-protocol-research-bxevq5/SPEC.md).
- [Computational Grammar Theory definitions](https://github.com/akadaan310/computationalgrammartheory/blob/ccr-04ad16b1-q42wck/DEFINITIONS.md).
- [Grammar in Numbers numeral research](https://github.com/akadaan310/grammarinnumbers/blob/claude/happy-newton-r2t17c/NUMBER_GRAMMAR.md).
- [SubstrateIO continuity protocol](https://github.com/akadaan310/substrateIO/blob/claude/research-substrate-bootstrap-bfd02a/PROTOCOL.md).
- [SNAD source/meaning separation](https://github.com/akadaan310/snad/blob/main/README.md).
- [SEURL namespace/machine](https://github.com/akadaan310/seurl/blob/master/README.md).

**Terminology contract:** "QITṬ" and the ṢIFR–LIFF operational reading originate in the owner's current proposed theory. "CALRC", "contextual glyph lift", "native-versus-positional valuation", and the specific formal rules/graphs are working technical names introduced here. Ordinary algebra, automata, positional notation, graph homology and information-loss terms retain their standard mathematical meanings.

**Next commission:** turn QITT/0.1 syntax and address functions into an independently replayable bounded interpreter; use the existing GLASS journal as parent; adapter-test strict glyph/slot/profile preservation against the PolyIA source contracts; record positive/negative fixtures with observable receipts; then commission historical/linguistic investigation only if explicitly authorized. Nothing here requires Google-based validation of the proposed theory.
