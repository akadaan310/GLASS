# GLASS UNISON Live/0.1 — A convergence calculus for local speech and Internet I/O

**Owner-defined goal, effective 2026-10-26:** an evidence-responsive instrument that captures locally authorized speech, draws actual algorithmic observations as they arrive, admits language uncertainty, asks for early human confirmation, and learns when not to predict. The goal is not infallibility; accuracy must be measured on independently confirmed and held-out examples.

**Source bases:** MUQRI app/analysis.py, app/rule_bind.py, app/waqf.py, app/ghunnah.py, app/tafkhim.py, app/letters.py, app/knowledge.py, app/verse_detect.py, its 40 ms posterior path and numeric measurements/1 contract; SURFACE original physics and renderer; GLASS QITṬ registered symbolic alphabet; NetGovComEduGovOrgEduGovComNet ACSP event/capability model. The [machine-readable Atlas](../atlas/unison-live-traces-v0.1.json) distinguishes 33 source families and runtime availability.

## 1. The state and update law

Let
\[
U_t=(c_t,x_t,z_t,p_t,\theta_t,h_t,r_t,a_t)
\]
where c = capture and permission state; x = measured local acoustic features; z = source/model/trace availability; p = candidate language evidence; theta = decision threshold; h = human confirmation history; r = authorized stream and cursor state; a = separate optional AST/QITṬ address frame. All source evidence is versioned. The guarded transition
\[
U_{t+1}=T(U_t,\mathrm{capture},\mathrm{observe},\mathrm{confirm},\mathrm{publish})
\]
allows an UNKNOWN output. The same glyph or source frame may have multiple typed interpretations without collapsing spoken phonemes into numeric word values.

### Local acoustic clock

The first APK uses 16,000 PCM16 samples/s and 1,024-sample frames (64 ms). It computes:
\[
RMS_t=\sqrt{N^{-1}\sum_n x_t[n]^2},\quad
ZCR_t=(N-1)^{-1}\sum_{n>0}[\mathrm{sign}(x_t[n])\neq\mathrm{sign}(x_t[n-1])].
\]
Coarse Goertzel bands at 180, 400, 850, 1,750 and 3,350 Hz provide an explicit *spectral centroid proxy* \(\sum_k f_kE_k/\sum_kE_k\), positive spectral flux \(\sum_k(E_k(t)-E_k(t-1))_+/\sum_kE_k\), and fractional low/mid/high energy. Normalized autocorrelation supplies only a pitch *proxy* if strong periodicity exists. Noise-floor-adjusted speech/pause heuristics are **not** MUQRI Waqf/Sakt verdicts.

Android Canvas draws concentric ink rings from observed RMS and finite amplitude/flux histories. Optional OS on-device ASR has its own RMS callback; it is a distinct capture mode, not simultaneous AudioRecord capture and not the canonical native SURFACE CPU renderer.

### Language clock

The first 30 completed human confirmations are a calibration bootstrap; changing from a confirmed Arabic label to a confirmed English label increments a switch count. A label with insufficient evidence is UNKNOWN. A candidate from PCM-only coarse spectral features is capped at 0.60 confidence *hint* because these features are not a reliable stand-alone language recognizer.

Android API 31+ offers an **on-device SpeechRecognizer** only when the OS reports an installed service. Android API 34+ can request detected languages and switching (depending on locally downloaded models and recognizer support). No cloud fallback or network speech recognizer is ever chosen. Local transcripts are not placed in the numerical event stream.

The prototype software threshold, based on observed agreement A and disagreement D with human confirmation, is:
\[
\widehat q_t=(A_t+1)/(A_t+D_t+2),\qquad
\theta_t=\operatorname{clamp}(0.70+0.18(1-\widehat q_t),0.70,0.88).
\]
This is not calibrated Bayesian posterior probability. Promotion to reliable prediction requires independent human labeling, confusion matrices across authentic Arabic/English switches, held-out metrics, false-prompt rates, calibration error and abstention coverage. Predictions are **proposed** until accepted; nonprediction is a valid action.

### GASology: proposed working discipline

**GASology** names Grammar–Admissibility–Stability of the I/O transition: which event types may execute under source/permission guards, which perturbations actually change the result, and whether confirmation evidence causes stable improvement without self-certification. It is new project nomenclature, not a verified external scientific field.

## 2. Source trace inventory and what is *not* packaged

The live Android implementation provides measured RMS, peak, ZCR, coarse frequency energy, flux, onset, silence and pitch proxy. MUQRI's phoneme-CTC posteriors, Viterbi, identity likelihood margin, the ten characteristic/sifaat heads, madd counts, ghunnah, tafkhim, waqf and calibrated learner scores remain **separate model-backed capabilities** in MUQRI. None is fabricated on the phone by coloring the screen. Embedding Python alone would not package the missing acoustic weights, CPU/GPU backend or reference corpus.

Read exact availability, units and source paths in atlas/unison-live-traces-v0.1.json. A future phone model must undergo measured runtime benchmarks and numeric parity with MUQRI before it can claim recitation grading.

## 3. NET × COMMUNET combinatorial grammar

The exact repository name parses as:

Net [Gov, Com, Edu, Gov, Org, Edu, Gov, Com] Net.

With multiplicity Gov=3, Com=2, Edu=2, Org=1, there are
\[
8!/(3!\,2!\,2!\,1!)=1680
\]
distinct inner permutations. If each of the eight slots independently selects one of five known categories, the raw possible strings number \(5^8=390625\). A symbolic combination has **no implicit real DNS authority**, government identity, data classification or Internet protocol privilege.

ACSP already separates resource ownership, awareness, authority, events and checkpoint. The new GLASS-LIVE/0.1 route reuses those design principles without silently minting ACSP capabilities. GET never mutates.

- Local capture and reactive ink run entirely offline.
- Only opt-in HTTPS events leave the device; the Java publisher rejects absent room/key and discards raw audio/transcripts altogether.
- The production server separately validates a small allowlist of numeric and categorical features, uses immutable PostgreSQL rows, authenticated append/read, idempotency keys, and bounded reconnecting SSE.
- Public visitors see automatically generated protocol heartbeats. They never see live private microphone records.
- Vercel serverless streams are **bounded**, not permanent sockets. Reconnect and cursor replay reproduce continuity.

## 4. Independent mathematical surfaces

A monotonic sample frame clock is not the same as a server timestamp, a QITṬ decimal register, a bit word, a quantum basis address or a star's physical reference frame. Typed adapters with declared units and loss preserve differences.

The surface rendering function may be written:
\[
I_t=\mathcal R(\mathrm{trace}_{0:t},\mathrm{annotation},\mathrm{permissions},\mathrm{view})
\]
where I is actual computed ink. Ink can react to acoustic pressure proxies without claiming to solve the full wave equation. A future physically calibrated acoustic field requires material parameters, boundary conditions and solver/measurement comparisons. Quantum behavior requires independent complex-amplitude or channel state; binary storage alone is not a quantum simulation.

## 5. Security and acceptance

On first app opening: microphone OFF, Internet event publisher OFF, no autoplay, no audio sample stored. Start PCM, Offline ASR and WAV import are explicit user actions; onPause stops active capture and streaming. Untrusted audio file imports accept only bounded RIFF/WAV PCM16 mono 16k; no audio playback occurs. Secret bearer tokens are entered by the user and are not baked into the APK.

The first implementation is an **independently packaged GLASS Android Canvas client**, rather than a modification of SURFACE's current native APK. Its algorithmic trace adapter can be consumed by the native SURFACE ink engine after actual Android/ABI verification. The original renderer, models and evidence remain unchanged.

### Acceptance not yet satisfied

A downloadable signed APK cannot be claimed until a real Android SDK build, artifact SHA-256 and user-device launch exist. The present model container has no Android SDK or registered owned Gateway server. The first connected GitHub Actions attempt failed before a runner was assigned, so its status is **BUILD BLOCKED** until a usable builder is available. Code and build scripts are nevertheless committed.

The connected Vercel ACSP source includes a GLASS terminal, Postgres migration and private stream endpoints. Deployment requires environment read/write keys and branch configuration; authoring a route is not proof that a production domain serves it.

**Epistemic rule:** a correct trace, a human confirmation, a number match, a Qur'anic recitation meaning, a rendered color, an inferred star position and a scientific claim require different kinds of evidence.
