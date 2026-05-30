# Editing Checklist (v2)

Use before finishing any deck.

## A. Core structure

- [ ] `main#deck` exists with `.slide` sections, each with unique `id`.
- [ ] `nav.nav-dots` hrefs match section ids in the same order.
- [ ] `SLIDE_IDS` / `var ids = [...]` matches section ids (see `runtime.js` or inline script).
- [ ] `python scripts/validate_deck.py deck.html` passes.

## B. Overlays (if used)

- [ ] Lightbox: all five ids present when `.arch-panel` or `.shot-tile` used.
- [ ] Detail: overlay + templates when `.detail-trigger` used; `data-detail-id` matches `<template id>`.
- [ ] Roadmap: `#roadmap-full*` nodes + `component.js` when `.roadmap-tile` used.
- [ ] Escape closes topmost overlay; deck scroll restores.

## C. CSS bundles

- [ ] `base.css` (+ needed `_bundles/*.css`) included — no missing layout.
- [ ] Product decks: include `legacy.css` if using `.kicker`, `.elevator`, extra decoration.
- [ ] KaTeX: `math/katex/head.html` linked when formulas present.

## D. Content quality

- [ ] No unresolved `[PLACEHOLDER]` tokens in publish output.
- [ ] Dark palette readable; no low-contrast body text on `--bg-alt`.
- [ ] Mobile: grids stack at 820px; nav dots move to bottom.

## E. New component (optional)

- [ ] Example HTML in `components/<cat>/<slug>/component.html`
- [ ] Bundle CSS updated; `component.css` comment points to bundle
- [ ] Entry added via `scripts/bootstrap_v2_library.py`
- [ ] Documented in `references/component-catalog.md`

## F. No v1 artifacts

- [ ] Do not use `assets/`, `validation-rules/`, or `scaffold_from_template.py`
- [ ] Registry is `components/registry.json` (v2 keys like `slide.cover`)
