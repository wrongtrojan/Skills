# Component Contract (Core + Variant)

## Core Runtime Contract (always required)

- `main.deck#deck`
- `nav.nav-dots` with anchors mapped to section ids
- `var ids = [...]` in script and same order as section ids/nav ids
- lightbox nodes:
  - `#lightbox`
  - `#lightbox-backdrop`
  - `#lightbox-close`
  - `#lightbox-img`
  - `#lightbox-cap`

Core behavior:

- scroll-snap slides
- active nav dot via `IntersectionObserver`
- keyboard paging (`ArrowUp/ArrowDown`, `PageUp/PageDown`, `Home/End`)
- Escape closes lightbox

## Registry-driven Component Contract

Each enabled component must be present in `components/registry.json` with:

- `key`, `section`, `variant`, `html`
- `requiredIds`, `requiredClasses`
- `requires`, `conflicts`
- optional: `overlay`, `css`, `script`, `validationRule`

Each rendered section should expose:

- `data-component-key="<key>"` on `<section>`

## Default Dracula Catalog (section + variant)

- `cover.basic`
- `elevator.basic`
- `capabilities.cards4`
- `screens.grid8Lightbox`
- `architecture.dualSvgZoom`
- `outlook.columns` or `outlook.roadmapOverlay` (mutually exclusive)
- `takeaways.cards3`
- `thanks.basicFooter`

## Variant Notes

- **`outlook.columns`**: static three-column summary.
- **`outlook.roadmapOverlay`**: interactive 2x2 tile summary + full overlay details. Requires:
  - `#roadmap-full`
  - `#roadmap-full-title`
  - `#roadmap-full-body`
  - `#roadmap-full-close`
  - `#roadmap-full-backdrop`

## Extension Rule

When adding a new component:

1. add snippet assets under `assets/components/<section>/<variant>/`
2. register component metadata in registry
3. add optional validation rule json
4. ensure no hardcoded changes in scaffold/validator core paths


