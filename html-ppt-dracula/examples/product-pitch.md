# Product Pitch Deck

Pattern for demo day / internal product share (~10 min).

## Suggested slide flow

1. **Cover** — `slide.cover` (use `.kicker` from legacy or `.section-kicker`)
2. **Elevator** — `slide.elevator`
3. **Capabilities** — `content.capabilitiesGrid`
4. **Screenshots** — `interactive.screensGrid` + `interactive.lightbox`
5. **Architecture** — `layout.archWrap` (optional)
6. **Roadmap** — `layout.columns3` **or** `interactive.roadmapOverlay` (not both)
7. **Takeaways** — `slide.takeaways`
8. **Thanks** — `slide.thanks`

## CSS bundles

```
typography.css
layout.css
content.css
interactive.css
slides.css
legacy.css
```

## Runtime

- `framework/dracula/runtime.js` — handles `.shot-tile` and `.arch-panel`
- Append `interactive/roadmap-overlay/component.js` if using roadmap tiles

## Assembly tips

- Use placehold.co or real screenshot URLs in `data-src` / `<img src>`.
- Keep 8 tiles max in two rows for balance.
- Footer link in thanks: real repo URL, no `[仓库链接]` placeholders.

## Validate

```bash
python scripts/validate_deck.py path/to/pitch.html
```
