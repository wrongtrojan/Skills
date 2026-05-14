# Component Registry Schema

This document defines the contract for `components/registry.json`.

## Top-level

- `version` string
- `presets` object
- `components` array

## Preset Contract

```json
{
  "description": "Human-readable note",
  "defaultComponents": ["component.keyA", "component.keyB"]
}
```

## Component Contract

Each component entry supports:

- `key` (required): unique key, format `section.variant`
- `section` (required): target section id, e.g. `s-out`
- `variant` (required): variant name
- `html` (required): relative path to section snippet
- `overlay` (optional): relative path to overlay snippet appended outside `main#deck`
- `script` (optional): relative path to JS fragment appended after base runtime
- `requiredIds` (required): ids that must exist if this component is enabled
- `requiredClasses` (required): class names that must exist if enabled
- `requires` (optional): list of keys that must also be enabled
- `conflicts` (optional): list of keys that cannot be enabled together
- `defaultEnabled` (required): whether preset defaults may auto-include it
- `validationRule` (optional): relative path to component validation rule json

## Validation Rule Contract

Rule file structure in `validation-rules/*.json`:

```json
{
  "requiredMarkers": ["text marker 1", "text marker 2"],
  "requiredIds": ["id-a", "id-b"],
  "requiredClasses": ["class-a", "class-b"]
}
```

All checks are string/regex-lite presence checks in final HTML output.

## Extension Workflow

To add a new component:

1. Add snippet(s) under `assets/components/<section>/<variant>/`.
2. Add one registry entry with `key`, `html`, dependencies, and validation rule path.
3. Add `validation-rules/<key>.json` if component has custom hooks/ids.
4. Run scaffold + validator with that component enabled.

