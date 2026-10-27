# GLASS Alphabet Search — Computational Gift Charter v0.1

**Commission:** Owner Abed Kadan, 2026-10-27. **Company:** GLASS. **Audience:** an independent research demonstration offered in gratitude to Google / Alphabet Inc. **Affiliation:** none claimed. **Implementation:** [Alphabet Search Laboratory](../apps/glass-oracle/alphabet-search.html). **Research foundation:** [QITṬ cyclic register science](QITT_CYCLIC_ARABIC_REGISTER_CALCULUS.md), [canonical register artifact](../atlas/qitt-register-v0.1.json), [existing SON query laboratory](../apps/glass-oracle/son.html).

## Intellectual foundation and provenance

The owner proposes a universal computational presentation for the Arabic-derived 28-symbol letter registry. This is a **new computational reinterpretation** of the QITṬ model: the existing registered sequence is partitioned into nine units (1–9), nine tens (10–90), nine hundreds (100–900), plus one thousands/return anchor (1000); zero (ṢIFR) is a **typed cell condition**, not a 29th base letter. For positions beyond thousands, the QITṬ/0.1 projection cycles through band types under an explicitly declared place index.

**Do not confuse** (a) a letter's historic spelling and shape, (b) historical abjad numerical conventions, (c) the owner's modern QITṬ extension, (d) Egyptian hieroglyphic writing, and (e) the standard code paths of Google Search. These are distinct claims and data sources. GLASS can present a contemporary *hieroglyph-inspired* visual language, but must not say that hieroglyphs historically implemented the register scheme without evidence. The historical Arabic genealogy remains in inspectable source metadata and documents even when a public visualization uses abstract symbols.

## Three orthogonal kinds of weight

1. **Native register weight**, R(letter): the original QITṬ 28-base-table value.
2. **Positional weight**, V(p,d)=d*10^p: the actual decimal magnitude held by coefficient d at place p. If the symbol R02 occurs at p=3, it can stand for 2000 contextually without changing its native table value of 2.
3. **Morphological weight**, W(root,pattern,features): an **Arabic linguistic pattern of derivation/inflection**, not an abjad number and not an unconditional meaning-transfer. A pattern can be represented as typed rewrite/transducer constraints on a root and feature bundle. Examples are domain-declared and individually validated.

The owner's broader **48 morphology forms** are not a verified canonical inventory in the currently inspected QITṬ dossier. Reserve a versioned morphology-adapter namespace and accept only reviewed mappings with sources, fixtures and documented context. Never present invented 48 transformations as accepted Arabic morphology. Sample design:
```json
{"schema":"glass.morphology.profile/0.1","root":["ف","ع","ل"],"pattern":"فَعَلَ","features":{"tense":"perfect","person":"3","number":"singular","gender":"masculine"},"surface":"فَعَلَ","status":"illustrative","evidence":[]}
```
For the computational reinterpretation, a morphology-like rule may map a typed symbolic AST to a new AST with preserved and changed features; such a mapping is an **engineered analogy**, not an assertion that natural-language inflection is identical to code generation.

## Search grammar and transport

**Input** natural search text, quotes, exclusions, `site:`, `filetype:`, `after:`, `before:`, explicit `OR`, with exact tokens shown in the UI. Compiler steps:
```
input -> bounded tokenize -> classify recognized operators -> preserve original query
      -> encodeURIComponent(query) -> https://www.google.com/search?q=<encoded>
```
First release is **transparent pass-through**, not semantic rewriting; every token transformation is visible. Google itself evaluates the query and returns its own results. Official documented operator descriptions: https://support.google.com/websearch/answer/2466433?hl=en

Do **not** construct an unlicensed Google Search scraper or automatically harvest results via curl. Google Search Central says unapproved automated queries violate its policies: https://developers.google.com/search/docs/essentials/spam-policies . The official Custom Search JSON API is closed to new customers and existing integrations have a stated 2027 transition: https://developers.google.com/custom-search/v1/overview . For in-app results later, evaluate currently supported Google Programmable Search Elements or other appropriately licensed APIs; preserve provider attribution and API terms.

## Search algebra (research extension, not implemented by v0.1)

A query plan can have typed nodes `TERM`, `PHRASE`, `AND`, `OR`, `EXCLUDE`, `SITE`, `FILETYPE`, `DATE_RANGE`, `GROUP`. AND/OR/query grouping behavior in Google Search is not guaranteed to match arbitrary Boolean algebra, so maintain distinction between a **GLASS formal query algebra** and **provider-supported rendering**. Use supported operator subset, emit warnings or alternative requests for unsupported expressions, and preserve a source-to-render mapping.

A future on-device pipeline may compile phrases into operator candidates. A phrase like `cats` is not itself a guaranteed taxonomy, a verified morphological analysis, or a real-time search result. The same input should produce the same local query plan under pinned schema+version+profile; search results from Google are time-varying and do not satisfy that local determinism claim.

## UI and disclosure

Use liquid glass layers, quiet radiance, interactive computational bands, and a search field as the primary touch point. The first page uses glass-backed panels, query/operator tokens, 28 register identifiers and a live weighted-place trace. It deliberately does **not** display a fake Google result list or pretend to be Google's own product.

A later glyph renderer may use original abstract icons, carefully licensed motifs and non-literal hieroglyph-inspired arrangements. The visible interface may avoid Arabic words for visual universality; **its 'About the register' provenance must always document the Arabic root and the modern owner-originated extension**.

## Testing and deployment status

This web file was added to GLASS main under `apps/glass-oracle/alphabet-search.html`. It is a static research front end and does not require an LLM, secret key or backend request. **No production deployment, device screenshot verification, Google API authorization, or independent historical review is asserted.** It is not yet attached to the root GLASS site's navigation.

Acceptance criteria for next unit: evaluate with an actual browser at mobile+desktop viewport; verify each operator and URL encoding; check keyboard accessibility; verify 0/9/90/900/1000/1900/2000/10000 fixture cells against source registry; create source-mapped morphology proof pack; support explicit feature-gated provider integration under the relevant product terms.

## Transfer to forthcoming Arabic Register repository

When the owner creates `Arabic Register`, give it independent custodianship of source tables, profile versioning, Arabic morphology fixtures and provenance. GLASS should **reference pinned releases** or validated checksums rather than fork and silently drift the scientific source. The gift's visual branding belongs to GLASS, not to Google / Alphabet Inc. unless a separate agreement is obtained.
