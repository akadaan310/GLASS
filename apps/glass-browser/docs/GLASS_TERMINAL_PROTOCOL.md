# GLASS Terminal Protocol / 0.1 — state-bearing web-overlay research

**Authority:** User-approved local GLASS browser operation, no shared login or automatic screen access.

## Address algebra

A GLASS address is a typed request for a local resource. It is not an assertion that the public Internet uses a proprietary transport. Standard web pages continue over HTTPS with TLS verification. The internal address scheme is a local resource **overlay** with explicit effect categories:

```
glass-address   = "glass://terminal/v1/", query
query           = "state" | "spell?word=", percent-encoded-utf8-word
# Everything else is REFUSED in 0.1.
```

The typed general plan for a future resource envelope is `T=(namespace,identity,session,clock,operation,authority,provenance,idempotency,shape)`. `READ` is pure, `PREPARE` stages work, `COMMIT` mutates only with an explicit authorization envelope, and `REVOKE` invalidates a capability. A URL string alone is **never** proof of authority to control the device or a website session. In the delivered engine the only admitted routes are read-only.

## Browser session coordinates

`S=(engine,profile_id,session_id,principal,epoch,navigation_events,storage_partition,consent_grants)`. A tab is a view, **not** a profile. A separate login on the same site requires a properly isolated browser storage partition and user-performed authentication. Never export or clone another browser's cookies without express user approval and the site's permitted mechanism.

The prototype contains `normal` and `private` Android process modes. The process distinction isolates local WebView directories; the private profile needs crash-safe guaranteed deletion before privacy parity is certified. Beyond this source increment, GeckoView supports `GeckoSessionSettings.Builder.contextId` and `usePrivateMode` for more explicit multi-profile partitions. Each persistent profile requires an auditable birth/expiry/scope and user-controlled deletion.

## Clock-bearing observation

Each observation is `(epoch,seq,monotonic_ns,kind,origin,detail,source,accuracy,missing_span,hash)`. App navigation events are direct app telemetry; JPEG frame samples are `MediaProjection` images at up to 1 Hz during user authorization. Screen lock, consent denial, projection stop, process death, data eviction and protected-window redaction must never be interpolated into apparently complete screen history. The current C++ ledger uses monotonic order and versioned state transitions; the Java journal gives source-order hash links. Without signatures or external anchoring, a local hash chain is not hostile-tamper-proof.

## Four regional finite state machines

```
PROJECTION: IDLE -> CONSENT_REQUESTED -> CAPTURING -> GAP_STOPPED
                                 \-> DENIED_GAP
PROFILE: NORMAL | PRIVATE_PROCESS -> CLOSED/CLEANUP_ATTEMPTED
TERMINAL: READ_ONLY -> PARSE -> GUARD -> RESULT / REFUSED
BINARY: MAGIC -> CLASSIFY -> PARSER_CANDIDATE / UNKNOWN -> STOP
```

A statechart may be in these regions simultaneously, with event source identity and no hidden authority escalation. User can revoke projection at any moment from the device notification/system chip. `BOOT_COMPLETED` does not auto-launch screen capture.

## Zero-one and QITṬ overlay

`BIT` records are binary written states; Arabic registers are a second orthographic/numeric projection, not a universal encryption code. A letter's native weight, reading timestamp, board position and word composition are separate. The 14 disconnected-initials symbol class is a research annotation, not case. `spell` preserves the original UTF-8 word alongside a lossy Unicode skeleton profile with honest flagging of unknown glyphs. Meanings and Qur'anic semantics need separately sourced lexical/corpus records.

## Shared-object gate semantics

C ABI `glass_gate_v1` is a size-limited, pure byte-buffer interface. The sample gate computes an 8-bit Hamming distance between input bytes and exports `glass_gate_entry`; the host regression uses `dlopen`. A production loader MUST require matching ABI, allowlisted library identity, packaged signature/integrity, versioned capability, and resource quotas. This ABI **cannot** run Windows PE/DLL files merely because their names match. Static analysis via LIEF/LLVM is separate from platform emulation via Wine/Box64; user-supplied executables must not be loaded into this Android app process.

## Generators-of-generators commission

`SCOPE → SOURCE_PIN → PLAN → PROPOSE → TYPECHECK → BUDGET → ADMIT → BUILD → OBSERVE → REPLAY → AUDIT → PUBLISH/ROLLBACK`.

A generator recipe is a typed, versioned DAG with an operator name, dependency pins, effect budget, source/reviewer and reproducibility fixture; never an arbitrary shell command from a web page. Installation/signing requires an explicit user-approved build target, distinct debug/release signing and verified artifact provenance. GitHub CI may build the source and publish an **artifact**, not automatically sideload an APK or self-modify installed Android code.

An unattached ChatGPT conversation does **not** receive remote access to this browser. Future pairing requires a separately implemented two-way authenticated channel, user-reviewed permissions, a visible session indicator, revocation and mutually observable connection receipts.
