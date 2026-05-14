# Editing Checklist (Core + Enabled Components)

Use this checklist before finishing any generated/edited deck.

## A. Core Mandatory Checks

- [ ] `main#deck`, `nav.nav-dots`, `#lightbox` and child ids exist.
- [ ] Section ids == nav href ids == script `ids` array order.
- [ ] Keyboard paging and Escape-close behavior remain valid.
- [ ] `python scripts/validate_structure.py <output.html>` passes.

## B. Enabled Component Checks (conditional)

For each enabled component in final HTML (`data-component-key`):

- [ ] required ids/classes from registry are present.
- [ ] rule file markers (if configured) are present.
- [ ] no conflict pair is enabled simultaneously.
- [ ] every enabled component's `requires` dependencies are enabled.
- [ ] no duplicate component key is enabled.

## C. Preset Visual Checks (Dracula)

- [ ] dark palette identity remains intact.
- [ ] interactive elements keep consistent hover/focus style.
- [ ] background decoration does not reduce readability.
- [ ] breakpoints (`820px`, `520px`) still behave as expected.
- [ ] no unresolved placeholder tokens remain (for example `[能力1]`, `[URL_1]`).

## D. Extension Acceptance (new component path)

When introducing a new component:

- [ ] snippet files created under `assets/components/<section>/<variant>/`
- [ ] registry entry added (with requires/conflicts/required fields)
- [ ] validation rule added if custom markers/hooks exist
- [ ] scaffold + validator both pass with new component enabled
- [ ] run scaffold with `--strict-assets` at least once before release


