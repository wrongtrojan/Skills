# Dracula Style System (v2)

Preset-level visual policy for html-ppt-dracula v2. Runtime lives in `framework/dracula/`.

## Framework files

| File | Role |
|------|------|
| `tokens.css` | `:root` color/spacing tokens |
| `base.css` | body, deck, slide, inner, h1–h2, nav-dots, scroll lock |
| `runtime.js` | nav, lightbox, detail, keyboard, KaTeX hooks |
| `shell.html` | minimal 2-slide starter |

## Token baseline

Defined in `framework/dracula/tokens.css`:

```css
--bg: #1a1b26;
--bg-alt: #22232f;
--fg: #f8f8f2;
--muted: #6272a4;
--purple: #bd93f9;
--cyan: #8be9fd;
--green: #50fa7b;
--orange: #ffb86c;
--pink: #ff79c6;
--yellow: #f1fa8c;
--red: #ff5555;
--border: rgba(98, 114, 164, 0.35);
--radius: 12px;
--shadow: 0 24px 48px rgba(0, 0, 0, 0.35);
```

Fonts: **DM Sans** (UI), **JetBrains Mono** (labels/code).

## Layout (v2)

- `main.deck#deck` — scroll-snap, hidden scrollbar
- `.slide` — full viewport (`100vh` / `100dvh`)
- `.inner` — **max-width 1180px**, centered, vertical gap via flex
- Breakpoints: **820px** (stack grids, move nav dots bottom), **520px** (single-column screenshots)

## Decoration

- `base.css` — subtle corner gradients + line pattern on `body::before`
- `legacy.css` — optional extra radial layers + per-slide highlight (product decks)

## Interaction recipe

Cards, tiles, panels:

- hover: purple border accent, `translateY(-2px)`
- focus-visible: cyan outline where applicable
- lightbox/detail: backdrop + Escape closes, scroll locked via `html.lightbox-open` / `html.detail-open`

## Component CSS

Do not edit bundles for one-off slides unless the pattern is reusable. Prefer copying snippet HTML and tweaking content only.

When adding a new reusable pattern:

1. Add rules to the appropriate `components/_bundles/*.css`
2. Add example to `components/<cat>/<slug>/component.html`
3. Register in `components/registry.json` via `bootstrap_v2_library.py`

## Academic vs product

| Aspect | Academic (RE-seminar) | Product (legacy) |
|--------|----------------------|------------------|
| Kicker | `.section-kicker` | `.kicker` |
| Outlook | timeline, direction cards | `columns3` or `roadmapOverlay` |
| Width | 1180px | 1180px (v2 unified) |
| Bundles | flow + interactive | slides + legacy |
