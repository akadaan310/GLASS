# GLASS — The Chronogram Alphabet / 0.1

**New named research profile:** Clock-bearing Unison syntax for local symbolic computation. Linked by source references to GLASS/QITṬ letter registers, the owner's Encycled Calculus and the GLASS operator-terminal research. The profile is not claimed to be a historical Arabic computation system, a formal proof of original mathematics or a new physical time standard.

## 1. Clock-bearing state

Let a measured record be:

\[
C=(\mathrm{epoch},\tau_w,\tau_m,\mathcal Z,\varphi,\mathrm{source},\mathrm{uncertainty}),
\]

where \(\tau_w\) is a host wall-clock POSIX instant, \(\tau_m\) is a monotonic tick at the same host, \(\mathcal Z\) is an explicitly versioned political/IANA zone rule, and \(\varphi\) is a normalized cyclic phase. Clock domains have **different semantics**. A software `time.time_ns()` reports an OS wall time whose nominal units are nanoseconds but whose actual error/resolution depends on the host. It is not evidence of physically recording each transistor event. Client/server offsets require an independent synchronization protocol; a request/response midpoint is only an estimate affected by network and execution jitter.

The symbol grammar is intentionally smaller than a shell, and its generated shell source is an artifact, not an executed side effect. Its operator namespace is **new**, separate from the inherited QITṬ numeric weights and the original 28-letter UNISON compiler roles.

## 2. Grammar, parser and source maps

```ebnf
Program      = { FrameOpen | Expression | FrameClose }, { Separator } ;
Expression   = "۞" | "⊕" | "⌛" | "◷" | "∅"
             | Zones | Earth | Solar | Difference | Phase | Generator ;
FrameOpen    = "⟦" ; FrameClose = "⟧" ;
Zones        = "⟳", "[", Zone, { ",", Zone }, "]" ;
Earth        = "⌖", "[", Latitude, ",", Longitude, "]" ;
Solar        = "☼", "[", Latitude, ",", Longitude, "]" ;
Difference   = "∆", "[", Zone, ",", Zone, "]" ;
Phase        = "ϕ", "[", PeriodSeconds, "]" ;
Generator    = "λ", ("۞" | "⊕" | "⌛" | "◷" | Zones | Earth | Solar | Difference | Phase);
Separator    = whitespace | ";" | "·" ;
Zone         = supported IANA ZoneInfo key (not inferred from longitude) ;
Latitude     = decimal in [-90,90] ;
Longitude    = decimal in [-180,180] ;
PeriodSeconds= decimal in [0.1,86400] ;
```

Finite contracts: 2,048 characters, 24 top-level operators, up to eight named zones per rotor, 512 operand characters, nested generator depth at most three, bounded client/server response. Parsed AST nodes preserve Unicode character spans and original UTF-8 byte spans. All unrecognized strings are refused rather than silently interpreted as arbitrary code.

## 3. Mean solar, apparent solar and Earth's angular geometry

Longitude \(\lambda\) is east-positive from Greenwich; latitude \(\phi\) is north-positive. A geometric twenty-four-wedge partition uses \(15^\circ\) longitudinal spans. For the solar model:

\[
T_{\mathrm{mean,solar}} \approx T_{\mathrm{UTC}} + 4\lambda\ \mathrm{minutes}.
\]

The solar equation-of-time correction \(E(t)\) yields:

\[
T_{\mathrm{apparent,solar}}\approx T_{\mathrm{mean,solar}}+E(t).
\]

The actual reference formula is the NOAA fractional-year approximation and solar-declination model used in `oracle.py`. Solar hour angle \(h=\mathrm{TST}/4-180^\circ\). Approximate elevation follows:

\[
\sin\alpha=\sin\phi\sin\delta+\cos\phi\cos\delta\cos h.
\]

The sphere embedding is \((x,y,z)=(\cos\phi\cos\lambda,\cos\phi\sin\lambda,\sin\phi)\). The sun-angle model is approximate and does not claim GPS data, precision ephemerides, atmospheric refraction, exact sunrise/sunset or SI laboratory clock synchronization.

A lawful *civil* UTC offset uses IANA zone rules \(\mathcal{Z}(t)\), not \(\lfloor(\lambda+180^\circ)/15^\circ\rfloor\). Civil zone boundaries follow national and historical policy; daylight rules change. IANA names and timestamp provenance are first-class metadata. Our `∆` subtracts two zone offsets at one same UTC instant; local clock labels can repeat (fold) or skip (gap) near DST events.

## 4. A typed non-time

`∅` represents `UNKNOWN / NO OBSERVATION / CLOCK NOT AVAILABLE`; it is neither the integer zero nor an asserted metaphysical absence of time. The server can be offline while the device clock still ticks; the UI displays an explicit UNKNOWN for that independent domain. On the same note, a sleeping or powered-off Android process cannot keep measuring its own screen or monotonic samples. A missing measurement remains a gap, never fabricated continuity.

## 5. Shell translation as language teaching

In GLASS `λ⟳[Asia/Dubai]` is an admitted **pure translation** to a sandbox-independent *instructional shell/Python script* that demonstrates `zoneinfo.ZoneInfo`. No arbitrary source can become a shell instruction by entering extra characters. The user can **copy** the resulting script by tapping it and execute it in their own trusted shell. Code generation is not a claim of a virtual machine or installed OS extension.

The contract connects to GLASS Oracle division families through typed event fields: `expr.source`, `expr.char_span`, `expr.byte_span`, `operator`, `lesson`, `status`, `values`, and `event_trace`. Future approved adapters may link the same Clock Oracle AST to QITṬ registry addresses, PURL/SEURL addresses, PolyIA finite generators, and Encycled event journals; none are silently invoked by this v0.1 server.

## 6. Reference clock layers and verified behavior

- Source: OS wall and monotonic clocks (Python stdlib); browser Date/Intl time (JavaScript).
- Civil time: Python `zoneinfo` backed by IANA (available TZDB installation dependent).
- Solar geometry: NOAA approximate formulas. Longitude time displacement of **4 minutes per degree**; latitude influences solar elevation rather than legal offset.
- Tested fixed instants: New York's 2026 March spring DST jump and November repeated hour; Nepal +05:45; Earth longitude boundaries; solar shifts and unit sphere; symbolic grammar refusals; local HTTP endpoints and safe no-execute `λ` output.

The implementation includes a local security boundary: HTTP binds to 127.0.0.1 by default with same-origin requests; no directory browsing, arbitrary shell/VM effect, geolocation request or automatic external API usage.
