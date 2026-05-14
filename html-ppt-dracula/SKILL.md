---
name: html-ppt-dracula
description: Create or update a single-file HTML presentation using a hybrid component orchestration protocol (natural language default + manifest precise control) with Dracula style preset.
disable-model-invocation: true
---

# HTML PPT Dracula Skill (Hybrid Components)

Build concise full-screen HTML slides by composing registered components into one output file.

## Dispatch Protocol

This skill uses a hybrid assembly model:

1. **Natural-language default**: if user asks "make/edit a deck" without precision controls, use preset defaults.
2. **Precise control**: if manifest is provided, manifest wins for component selection and content fields.
3. **Direct override**: if no manifest, `--components` can replace preset defaults.

Priority for component selection:

`manifest.components` > `--components` > `preset.defaultComponents`

## Source of Truth

- Registry: `components/registry.json`
- Contract reference: `components/schema.md`
- Base shell: `assets/base/shell.html`
- Section/variant snippets: `assets/components/<section>/<variant>/`
- Rule files: `validation-rules/<component-key>.json`

Never hardcode business components in orchestration logic. Read registry and compose dynamically.

## Required Reading Order

1. `references/style-system.md`
2. `references/component-spec.md`
3. `components/schema.md`
4. `references/editing-checklist.md`

## Build Workflow

1. Resolve enabled components with hybrid priority.
2. Load `assets/base/shell.html`.
3. Inject selected section snippets (`component.html`) in order.
4. Inject optional overlays/styles/scripts declared by each component.
5. Replace placeholders for title/repo/text fields.
6. Run validator (`core + enabled component rules`).
7. Ensure unresolved placeholders are cleared (unless explicitly validating draft mode).
8. Fix all failures before delivery.

## Script Commands

Natural-language/default path (preset):

```bash
python "C:/Users/24051/.cursor/skills/html-ppt-dracula/scripts/scaffold_from_template.py" --output "path/to/output.html" --preset dracula
```

Manifest precision path:

```bash
python "C:/Users/24051/.cursor/skills/html-ppt-dracula/scripts/scaffold_from_template.py" --output "path/to/output.html" --manifest "path/to/manifest.json"
```

Custom component list path:

```bash
python "C:/Users/24051/.cursor/skills/html-ppt-dracula/scripts/scaffold_from_template.py" --output "path/to/output.html" --components "cover.basic,elevator.basic,capabilities.cards4,screens.grid8Lightbox,architecture.dualSvgZoom,outlook.roadmapOverlay,takeaways.cards3,thanks.basicFooter"
```

Validation:

```bash
python "C:/Users/24051/.cursor/skills/html-ppt-dracula/scripts/validate_structure.py" "path/to/output.html"
```

Allow placeholders in draft-only validation:

```bash
python "C:/Users/24051/.cursor/skills/html-ppt-dracula/scripts/validate_structure.py" "path/to/output.html" --allow-placeholders
```

Strict optional-asset mode during scaffold:

```bash
python "C:/Users/24051/.cursor/skills/html-ppt-dracula/scripts/scaffold_from_template.py" --output "path/to/output.html" --preset dracula --strict-assets
```

## New Component 5-Step Method

1. Create snippet directory: `assets/components/<section>/<variant>/`.
2. Add `component.html` (plus optional `overlay.html`, `component.css`, `component.js`).
3. Register metadata in `components/registry.json` (`requires/conflicts/requiredIds/requiredClasses`).
4. Add `validation-rules/<component-key>.json` when custom hooks/markers exist.
5. Verify by running scaffold + validator on a deck that enables this component.

## Hard Constraints

- Keep single-file output.
- Keep dot-nav, scroll-snap, keyboard navigation, and lightbox close semantics.
- Keep dark Dracula style unless user explicitly requests another preset/theme.
- Keep validator zero false-positive for disabled components.
- Keep `requires/conflicts` constraints validated for enabled components.
- Keep publish outputs free of unresolved placeholders (`[PLACEHOLDER]` tokens).

## Recommended Delivery Workflow

1. Scaffold deck (`--preset` or `--manifest`).
2. Run strict scaffold check once before release (`--strict-assets`).
3. Run validator in default mode (placeholder checks enabled).
4. Only use `--allow-placeholders` for temporary draft validation.
5. Perform manual visual preview after validator passes.


