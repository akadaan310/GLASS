# GLASS Clock Oracle · symbol-only Earth-time terminal

**The complete program is here.** The frontend is HTML/Canvas with one typing field and tappable operator glyphs. The backend is standard-library Python, runnable in **Android Termux**, Linux, macOS or a custom SSH terminal. **No new hosting service, login, button, or GitHub checkout on your phone is required** once you've received the ZIP.

## Android / Termux (run the server on the same phone)

Save the ZIP provided by ChatGPT into your Android Downloads folder, open Termux and run:

```sh
pkg install python tzdata
mkdir -p ~/glass-clock
python -m zipfile -e /sdcard/Download/GLASS_Clock_Oracle_009.zip ~/glass-clock
cd ~/glass-clock
sh start-glass.sh
```

If Termux cannot read shared Downloads, run `termux-setup-storage` once and approve Android storage access, or move the ZIP into Termux using your ordinary file manager. `tzdata` supplies IANA zone rules when supported by Python `zoneinfo` through its TZPATH. If the OS doesn't expose the database, the independent Python `tzdata` package (`python -m pip install tzdata`) is a fallback.

Then, **on the same phone**, open Chrome at:

**http://127.0.0.1:8765/**

The website and the server both live inside Termux. Keep the Termux process alive while accessing GLASS. Android can suspend/terminate background apps, so this is a running local server, not an uninterruptible always-on service.

On a laptop/server you can run `python3 server.py --port 8765`. To use your remote Oracle machine from a phone, establish a deliberate encrypted SSH tunnel or a reviewed authenticated HTTPS reverse proxy; this first version intentionally refuses listening on 0.0.0.0 and does not invent remote access.

## Type symbols only

All commands are local symbolic expressions. You may write them adjacent to each other, separated with whitespace, `;` or `·`:

```text
۞ ⊕ ⌛ ◷
⟳[America/New_York,Asia/Dubai,Asia/Kathmandu]
⌖[0,45] ☼[0,45]
∆[America/New_York,Asia/Dubai]
ϕ[60]
λ⟳[Asia/Dubai]
∅
⟦ ۞ ⊕ ⟳[Asia/Dubai] ⟧
```

The operator glyph is the instruction; zone names, latitude/longitude and period numbers are typed **operands** inside `[ ]`, not English command verbs. Glyph taps insert the operator skeleton at the cursor. **No click-to-run controls exist.** Each accepted expression returns a typed explanation and a calculated value. A `λ` expression generates copyable shell/Python source, **never executes it**. To test one command directly in Termux without a browser:

```sh
python3 oracle.py '۞ ⊕ ⟳[Asia/Dubai] λ⟳[Asia/Dubai]'
```

## Mathematics

- `۞`: browser **device** wall-clock observation (client-reported). This can differ from the actual server host clock.
- `⊕`: host UTC instant; POSIX time is not a physical atomic TAI time scale and does not enumerate positive leap-second labels.
- `⌛`: host server wall time; don't conflate POSIX epoch with CPU timer cycles.
- `◷`: elapsed monotonic clock since GLASS process creation; its epoch is arbitrary and **cannot be compared numerically across hosts**.
- `⟳[...]`: named IANA civil zones with DST, historical and political rules; latitude/longitude alone are **not** sufficient to recover an official time-zone name.
- `⌖[latitude,longitude]`: Earth geometric coordinates, unit sphere and a 15-degree longitude wedge. 24 wedges make 360°, but those are not 24 legal time zones.
- `☼[latitude,longitude]`: mean solar clock `UTC + 4×longitude minutes`, plus the approximate NOAA equation of time and solar altitude (latitude affects elevation and day/night geometry).
- `∆[zone1,zone2]`: difference of signed UTC offsets at the same observation instant, including unusual +05:45 offsets and fold boundaries.
- `ϕ[period_seconds]`: normalized periodic angle on a process clock. `∅`: unobserved/non-time state, not numeric zero.
- `λ`: safe **code generation**, with an independently bounded source grammar. Generated shell scripts are not executed in the browser or backend.

The front end uses `Intl.DateTimeFormat` when offline and **marks the GLASS server as UNKNOWN** until `/api/time` succeeds. A network time offset estimate uses a sampled server wall reading and browser midpoint estimate; its `~ RTT/2` label is indicative latency, not a rigorous clock accuracy bound or NTP synchronization. The web UI only talks to the **local** Python backend. Typed text is not persisted by default; there is no user location API, search tool, credential collection or external network request.

Official references: [IANA time-zone data](https://www.iana.org/time-zones), [Python zoneinfo](https://docs.python.org/3/library/zoneinfo.html), [NOAA solar equations](https://gml.noaa.gov/grad/solcalc/solareqns.PDF), [MDN Intl.DateTimeFormat](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat).

## Code / tests

```sh
# Core and HTTP acceptance (works with Python standard library only):
python3 -m unittest discover -s tests -p 'test_clock.py' -v
python3 -m unittest discover -s tests -p 'test_http.py' -v
# Optional Chromium tests require Python Playwright + a working Chromium binary:
python3 -m unittest discover -s tests -p 'test_browser.py' -v
node --check client.js
python3 -m py_compile oracle.py server.py
```

The tests include known DST transition instants, fractional-hour offsets, UTC/monotonic distinctions, solar/wedge calculations, shell generator guards, malicious operators, and local HTTP requests. The optional browser harness skips when Playwright is not installed. Browser screenshots may be produced with fixture-backed HTML if the test runner blocks loopback navigation; that distinction is documented in `evidence/browser.json`.

**Deployment status:** GLASS is locally runnable in Termux and source-published to GitHub/main. This task does not claim `glass.com` has been configured, an Oracle VM connected, or this file has been installed on your phone.
