# Academic Seminar Deck

Pattern for literature survey / lab seminar (~15 min).

## Suggested slide flow

1. **Cover** — `slide.cover` + `typography.sectionKicker`
2. **Outline** — `content.timeline` + `typography.partBanner`
3. **Background** — `layout.archWrap` + `content.bullets` + `math.katex`
4. **Method slides** — `layout.splitRow`, `flow.iclLayout`, `content.dataTable`
5. **Deep dives** — `content.card` + `interactive.detailSystem` (templates per paper)
6. **Map / directions** — `layout.directionCard` or `content.timeline`
7. **Thanks** — `slide.thanks`

## CSS bundles

```
typography.css
layout.css
content.css
flow.css
interactive.css
slides.css
```

Skip `legacy.css` unless you want extra background layers.

## Runtime

- Inline RE-seminar script **or** `framework/dracula/runtime.js` with matching `SLIDE_IDS`
- KaTeX from `components/math/katex/head.html`
- Detail overlay required when using `.detail-trigger`

## Reference

Full example: `Article/presentation/RE-seminar.html`

Validate:

```bash
python scripts/validate_deck.py "d:/UniversityStudy/Profession/Research/Article/presentation/RE-seminar.html"
```
