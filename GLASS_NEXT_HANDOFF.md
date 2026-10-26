# GLASS — Next-Agent Handoff (single-task)

**Date:** 2026-10-26  
**Canonical repository:** https://github.com/akadaan310/GLASS (branch `main`).  
**User's immediate goal:** Open the actual GLASS typing-only website on their Android phone through their **custom terminal**, not a GitHub code viewer. The Railway connection is prompting for reconnection. **Do not depend on Railway or initiate another full research commission.**

## Already available

- Working source for the primary GLASS Oracle: [`apps/glass-oracle/index.html`](apps/glass-oracle/index.html). This is the **single-page, self-contained HTML** with the evolving Unison glyph Rolodex and text input. No buttons, no standard search interface.
- SON symbolic URL view: [`apps/glass-oracle/son.html`](apps/glass-oracle/son.html). It is supplemental; prioritize the main site.
- SON protocol documentation: [`docs/SON_UNISON_PROTOCOL.md`](docs/SON_UNISON_PROTOCOL.md).
- Prior GitHub source publication **does not prove** `glass.com` is deployed or that a custom terminal is connected. Do not claim either without an actual response from the device/server.

## One task to finish

1. **Use the user's authorized custom terminal** (or ask them only to connect/open it if no device access exists). Check Python or another minimal static-server runtime. No need to install a framework, clone the repository, or connect Railway.
2. On **Android Termux**, the minimal standalone path is:

   ```sh
   pkg install -y python curl
   mkdir -p ~/glass && cd ~/glass
   curl -fL https://raw.githubusercontent.com/akadaan310/GLASS/main/apps/glass-oracle/index.html -o index.html
   python -m http.server 8787 --bind 127.0.0.1
   ```

   On the **same phone**, open `http://127.0.0.1:8787/` in its browser. This is a local static preview; it works only while the terminal server is running. **Run these commands on the user's device only with their authorization**, not in an unrelated sandbox. If Termux is unavailable, use any existing terminal/static-file server equivalent.
3. Verify by actually opening the page and testing continuous typing, glyph motion and touch selection; preserve observed errors. Do not invent a live test.
4. For outside-the-phone access or `glass.com`, set up a **user-authorized authenticated HTTPS tunnel or hosting origin** and verify domain/DNS access. Never expose the local unauthenticated server to the public Internet by simply binding to `0.0.0.0`. Custom domain ownership/configuration is **not verified**.
5. Give the user **one real browser URL that opens the running UI**, or the exact missing authorization/blocker. Keep the reply short.

## Operating constraints

Preserve the current one-input aesthetic and all existing GLASS sources. Avoid large research digressions, new repositories, paid infrastructure, background work without a running authorized service, and claims that URL addressing means lossless compression of arbitrary data. Treat this handoff as a **hosting/preview continuation only**. If editing source, append a small verified commit to `GLASS/main`; no force pushes. No Railway action is needed while disconnected.

**Acceptance:** An actual page loads from the user's terminal/authorized host, accepts typing, shows glyphs, and the URL is accessible to the user. Otherwise report `NOT DEPLOYED` and what access is required.
