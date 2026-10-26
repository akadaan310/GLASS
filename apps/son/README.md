# SON/0.1 — GLASS programmable URL and Unison tape

**Start:** open [index.html](index.html) in a browser or use Python CLI [son.py](son.py). GLASS deploy path is planned as `https://glass.com/?son=s1.<base64url payload>`; this repository has not verified the domain is serving SON.

Input is typing-only. Each line is an independent Boolean-style query (maximum four). The glyph rolodex and live inspectors show token/operator order and four-bit matrix projections. Tapping a symbol inserts its ASCII keyword. There are no buttons, automatic searches, credential capture, background web access, or external LLM integration. Links may be opened intentionally by tapping.

## Use

```sh
python3 son.py demo > demo.json
python3 son.py compile '"clock-bearing states" site:github.com'
python3 son.py batch examples.txt
python3 son.py rewrite '"sun" site:nasa.gov' sun moon
python3 -m unittest discover -s tests -p 'test_son.py' -v
node tests/test_browser.mjs
```

The output carries the local source AST, lexical byte-addressed tape, source sha256, symbol sequence, 4×4 matrix before and after XOR perturbation, labeled ideal quantum statevector simulation, Google search projection, local logical event trace, and a combined four-lane interleaving. Compiler examples are safe local transformations; Google URLs are not called unless explicitly opened.

The tiny URL glyph namespace does not eliminate the need to store any large backing corpus. Long URLs are refused rather than inventing a nonexistent storage service. Only author-approved rewrites produce new versioned program records.

Full mathematical and trust contract: [SON_UNISON_PROTOCOL.md](../../docs/SON_UNISON_PROTOCOL.md). Existing GLASS/QITṬ and Encycled sources are preserved. The Google operator projection has limited Boolean fidelity because Google Search is not a general propositional theorem prover.
