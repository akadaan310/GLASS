# GLASS Ω / Clockworld

**Standalone research screen:** [index.html](index.html). Save/open it in a modern browser. No build, external font, JavaScript library, API keys, model provider, location data or network connection required. Use the **Fullscreen** button where supported. The layout adapts to narrow/mobile screens.

## Screens

**MECHANICS:** live mathematical Canvas2D Lissajous/oscillator field, sampled observations, synthetic 4-bit control, bit-level event stream, frequency/speed/sampling controls, pause/step/reset, and explicit *injected* fault. Running time is simulated from animation frames; this is not hardware-cycle telemetry.

**HOMELESS:** synthetic seeded population of 68 fictional households (167 persons in the present fixture). All movement policy logic operates at household level and retains member identities. Housed, sheltered and unsheltered are provisional projection states; it is not a real population count and cannot replace HOMELESS's Unity-native product. The offered policies have illustrative immediate-score opportunity costs, not calibrated social impact.

**TERMINAL:** local finite command interpreter (no LLM, shell or server). The command plane admits only HELP, TRACE, FLIP bit 0..3, FREQ 0.25..4, STEP 1..64, WORLD HOUSING/SHELTER/HOLD, RESET, PAUSE, PLAY, and PROPOSE / ADMIT. A proposal can be stored with no effect until ADMIT. This demonstrates a deterministic automaton gate for possible future LLM output, not a complete LLM connector or remote commissioning service.

**ATLAS:** six mathematical foundations for event derivative, cycles, lifetime charge, sampling loss, happens-before and opportunity cost.

## Native reference

Run in the **repository root**:

~~~sh
g++ -std=c++20 -O2 -Wall -Wextra -pedantic tests/encycled_test.cpp -o /tmp/encycled-test
/tmp/encycled-test
g++ -std=c++20 -O2 -Wall -Wextra -pedantic runtime/encycled_cli.cpp -o /tmp/encycled
/tmp/encycled trace
~~~

The native core lives in runtime/encycled.hpp, and the science is at [docs/ENCYCLED_CALCULUS.md](../../docs/ENCYCLED_CALCULUS.md). Browser and native implementations are **separate reference kernels**; scientific and output parity is a future gate.

## Evidence / known limits

The native test and CLI passed on the author's isolated Linux tool container with compiler output inspected and a JSON trace parsed. Node 22 syntax verification passed for the standalone HTML script. A headless Chromium screenshot attempt timed out (also on a minimal test page), so this delivery does **not** assert browser rendering acceptance, GPU performance, Android compatibility or Unity gameplay. The current browser event log is volatile, bounded and process-local; it is not an installed GLASS persistent publisher. The procedural visualization is a model, not captured electrical data.

GLASS, SURFACE and HOMELESS preserve separate runtime/product requirements. Never promote a simulated outcome into physical observation, real demographics, or a scientific novelty claim.
