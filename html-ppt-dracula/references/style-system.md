# Dracula Preset Style System

This file defines the `dracula` preset. Keep it as preset-level policy, not core runtime logic.

## Preset Identity

- Dark-first background (`--bg`, `--bg-alt`)
- Low-noise geometric/radial decoration
- Sparse high-contrast accents (purple/cyan/pink)
- Subtle motion only (`translateY(-1px/-2px)`)

## Token Baseline

Use these defaults in `:root`:

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

## Preset Layout Constraints

- `main.deck#deck` keeps scroll-snap and hidden scrollbar
- `.slide` keeps full viewport rhythm (`100vh/100dvh`)
- default max content width near `1100px`
- breakpoints stay at `820px`, `520px` unless user asks otherwise

## Interaction Constraints

Shared hover/focus recipe for cards/tiles/panels:

- border accent toward purple
- small lift transform
- cyan focus-visible ring for keyboard users

Lightbox interaction remains required:

- close by close button/backdrop/Escape
- lock scroll while open

## Variant-specific Preset Notes

- `outlook.columns`: no overlay runtime needed.
- `outlook.roadmapOverlay`: include roadmap full-screen overlay styles and large title/list scale.

## Extension Guidance

When adding a new component variant under Dracula preset:

1. reuse existing token palette
2. match existing interaction recipe
3. keep readability first (avoid heavy glow/blur)
4. if unique visuals are needed, scope in component css instead of changing base shell globally


