# Skills

Reusable Cursor skill packages for structured workflows.

## html-ppt-dracula (v2)

Single-file HTML presentations with Dracula dark theme.

**Location:** `html-ppt-dracula/`

| What | Where |
|------|-------|
| Framework | `framework/dracula/` — tokens, base CSS, runtime JS, shell |
| Components | `components/` — 31 copy-paste snippets + `registry.json` |
| CSS bundles | `components/_bundles/` |
| Docs | `references/` — catalog, assembly, style, checklist |
| Examples | `examples/academic-seminar.md`, `examples/product-pitch.md` |
| Validate | `python html-ppt-dracula/scripts/validate_deck.py deck.html` |

**v2 changes:** No scaffold/manifest pipeline. Assemble decks manually from snippets. Max content width **1180px**. Removed `assets/`, `validation-rules/`, `scaffold_from_template.py`.

See `html-ppt-dracula/SKILL.md` for agent instructions.
