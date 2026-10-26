# UNISON / GLASS — 114-profile Oracle Game v0.2

## Fixed admission contract
114 board profiles = four explicitly distinct Arabic 28-slot game boards (two hijāʾī, two abjad; each pair retains independent membership/history) plus 110 curated language/script locale profiles. Those 110 require Unicode CLDR main exemplar import before making claims of their actual alphabet contents. Language != script != alphabet; 9, 10, 11, 28, 29, 30, 40, 300 are optional game board cardinalities, not universal natural language properties.

## Event language
`⟦Λ:profile ⊗ Ω:grapheme ⊗ Γ:operator ⊙ τ:clock Π:evidence⟧ → ۞`
Grapheme → script candidate → typed oracle → behavioral recipes. User taps a grapheme to inspect its witness/operation. Typing is optional and autonomous GLASS events continue regardless.

## Player
`P=(player_id, membership, layer, board, capabilities, cursor)`. No architectural player-count ceiling, but actual workers and storage must be finite and quota-governed. Every placement is validated against the selected board slot and appended to a causal event log. No arbitrary client-supplied layer grants owner privileges. A player can participate on multiple boards through explicit membership edges.

## Speech
Web SpeechRecognition may require remote processing and isn't supported in all browsers. Trigger only with an explicit user action; expose provider/privacy status. File transcription needs an installed authorized backend and must report unavailability rather than fabricate a transcript.

## Executable reference delivered separately
The v0.2 ZIP includes a full-screen static immersive web app, 114-profile JSON, scripted typing/oracle inspection, and a Python game-state fixture. Proofs currently cover registry cardinality/uniqueness, JS syntax and a 1000-player event sample. This source archive is not automatically on GitHub main.

## Implementation gates
(1) Import CLDR 49 exemplar datasets with provenance and licensing (2) grapheme normalization and script extensions (3) type-checked grammar and generator cards (4) Redis presence + durable PostgreSQL event history (5) rich writing/reading/audio features via permissioned adapters (6) synchronized browser and APK projections (7) untrusted language input escape/normalization (8) tests, observed browser frame, then Vercel deployment.
