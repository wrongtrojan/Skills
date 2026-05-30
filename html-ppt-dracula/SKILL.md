---
name: html-ppt-dracula
description: Build or edit single-file HTML presentations with Dracula v2 framework and copy-paste component library (no scaffold).
disable-model-invocation: true
---

# HTML PPT Dracula (v2)

Create full-screen scroll-snap HTML decks by assembling **framework + component snippets**. There is no code generator — you copy HTML/CSS/JS into one file.

## Source of truth

| Resource | Path |
|----------|------|
| Framework | `framework/dracula/` (`tokens.css`, `base.css`, `runtime.js`, `shell.html`) |
| Components | `components/<category>/<slug>/component.html` |
| CSS bundles | `components/_bundles/*.css` |
| Registry | `components/registry.json` (31 keys) |
| Catalog | `references/component-catalog.md` |

## Required reading

1. `references/style-system.md` — tokens, 1180px layout, bundles
2. `references/assembly-guide.md` — step-by-step deck build
3. `references/component-catalog.md` — all component keys
4. `references/editing-checklist.md` — pre-delivery checks

## Workflow

1. Copy `framework/dracula/shell.html` or an example deck.
2. Include `base.css` + required `_bundles` (see component `component.css` comments).
3. Paste slide content from `components/**/component.html`.
4. Sync `nav.nav-dots`, section ids, and `SLIDE_IDS` in `runtime.js`.
5. Add overlays (lightbox, detail, roadmap) once if needed.
6. Validate:

```bash
python scripts/validate_deck.py path/to/deck.html
```

Draft mode (allow bracket placeholders):

```bash
python scripts/validate_deck.py path/to/deck.html --allow-placeholders
```

## Bootstrap library

Regenerate component folders + registry after catalog changes:

```bash
python scripts/bootstrap_v2_library.py
```

## Deck patterns

- **Academic seminar** — see `examples/academic-seminar.md` (timeline, arch-wrap, detail, KaTeX)
- **Product pitch** — see `examples/product-pitch.md` (elevator, capabilities, screens, takeaways)

## Hard constraints

- Single HTML file output (CSS/JS may be inline or linked for authoring).
- Keep scroll-snap, dot nav, keyboard paging (`↑/↓`, `Home/End`), Escape closes overlays.
- Section ids == nav hrefs == script id array.
- No unresolved `[PLACEHOLDER]` in published decks.
- Do not use removed v1 paths (`assets/`, `scaffold_from_template.py`, `validation-rules/`).

## Adding a component

1. Add example HTML + README under `components/<category>/<slug>/`.
2. Add styles to the appropriate `_bundles/*.css`.
3. Extend `COMPONENTS` in `scripts/bootstrap_v2_library.py` and run it.
4. Document in `references/component-catalog.md`.

## Reference implementation

`d:\UniversityStudy\Profession\Research\Article\presentation\RE-seminar.html` — full academic deck with inline CSS (equivalent bundles extracted in v2).
