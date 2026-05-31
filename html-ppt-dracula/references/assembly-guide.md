# Assembly Guide (v2)

Build a single-file HTML deck by **copy-paste assembly** — no scaffold script.

## 1. Start from shell

Copy `framework/dracula/shell.html` or duplicate an existing deck (e.g. `RE-seminar.html`).

## 2. Link framework CSS

In `<head>`:

```html
<link rel="stylesheet" href="path/to/framework/dracula/base.css" />
```

`base.css` imports `tokens.css`. Max content width is **1180px** (`.inner`).

## 3. Add component bundles

Merge needed bundles into one `<style>` block or link them:

| Deck type | Typical bundles |
|-----------|-----------------|
| Academic seminar | typography, layout, content, flow, interactive, slides |
| Product pitch | typography, layout, content, interactive, slides, **legacy** |

See `components/<category>/<slug>/component.css` comments for bundle paths.

## 4. Compose slides

For each slide:

```html
<section class="slide" id="s-unique-id">
  <div class="inner">
    <!-- paste from components/.../component.html -->
  </div>
</section>
```

Use `references/component-catalog.md` to pick snippets.

## 5. Sync navigation

1. Add `<a href="#s-unique-id">Label</a>` in `nav.nav-dots` **in slide order**.
2. Set the same ids in `framework/dracula/runtime.js` → `SLIDE_IDS` (or inline `var ids = [...]`).

Section ids, nav hrefs, and script array **must match exactly**.

## 6. Overlays (once per deck)

Append after `</main>` if used:

- `interactive/lightbox/component.html` — always for arch/screens
- `interactive/detail-system/component.html` — detail triggers + templates
- `interactive/content-modal/component.html` + `component.js` — JSON/text modal (pair with `code/highlight-js/head.html`)
- `interactive/roadmap-overlay/component.html` + `component.js` — roadmap variant

`<template id="detail-…">` blocks can live anywhere in `<body>`.

## 7. Runtime

```html
<script src="path/to/framework/dracula/runtime.js"></script>
```

Or inline the script from `runtime.js` and set `var ids = [...]` at the top.

For KaTeX, paste `components/math/katex/head.html` in head + before runtime.

For JSON/text modals, paste `components/code/highlight-js/head.html` and append `components/interactive/content-modal/component.js` after runtime.

For roadmap overlay, append `components/interactive/roadmap-overlay/component.js` after runtime.

## 8. Validate

```bash
python scripts/validate_deck.py path/to/deck.html
```

Fix all errors before delivery.

## Example decks

- `examples/academic-seminar.md` — survey / paper reading flow
- `examples/product-pitch.md` — elevator, capabilities, screenshots
