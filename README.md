# Skills

Reusable Cursor skill packages for structured workflows.

| Skill | Purpose | Agent entry |
|-------|---------|-------------|
| [html-ppt-dracula](html-ppt-dracula/) | Single-file HTML slide decks (Dracula theme) | `html-ppt-dracula/SKILL.md` |
| [quiz-markdown-to-web](quiz-markdown-to-web/) | Markdown question banks → static `quiz_web/` site | `quiz-markdown-to-web/SKILL.md` |

---

## html-ppt-dracula (v2)

Single-file HTML presentations with Dracula dark theme, scroll-snap navigation, and a copy-paste component library.

**Location:** `html-ppt-dracula/`

| What | Where |
|------|-------|
| Framework | `framework/dracula/` — tokens, base CSS, runtime JS, shell |
| Components | `components/` — **34** copy-paste snippets + `registry.json` |
| CSS bundles | `components/_bundles/` |
| Syntax highlighting | `vendor/highlightjs/` — local Dracula theme + highlight.js (works with `file://`) |
| Docs | `references/` — catalog, assembly, style, checklist |
| Examples | `examples/academic-seminar.md`, `examples/product-pitch.md` |
| Validate | `python html-ppt-dracula/scripts/validate_deck.py deck.html` |
| Regenerate registry | `python html-ppt-dracula/scripts/bootstrap_v2_library.py` |

**Notable components:** `interactive.contentModal` (JSON/text modal), `content.evalList`, `code.highlightJs`.

**v2 notes:** No scaffold/manifest pipeline — assemble decks manually from snippets. Max content width **1180px**. Removed v1 paths (`assets/`, `validation-rules/`, `scaffold_from_template.py`).

For JSON modals, copy `vendor/highlightjs/` beside your deck and include `components/code/highlight-js/head.html` in `<head>`.

See [`html-ppt-dracula/SKILL.md`](html-ppt-dracula/SKILL.md) for agent instructions.

---

## quiz-markdown-to-web

Packages markdown question/answer chapters into a ready-to-open static quiz site under `<project-root>/quiz_web/`.

**Location:** `quiz-markdown-to-web/`

| What | Where |
|------|-------|
| Agent workflow | `SKILL.md` |
| Contract & commands | `reference.md` |
| Usage examples | `examples.md` |
| Markdown schema | `spec/markdown-schema.md` |
| Chapter config template | `templates/chapters.template.json` |
| Web templates | `templates/index.html`, `templates/quiz.css`, `templates/app.js` |
| Build scripts | `scripts/package_quiz_web.py`, `build_quiz_data.py`, `validate_quiz_markdown.py` |

**Required project inputs:**

- `<project-root>/chapters.json` — chapter list with `id`, `title`, `order`, `questionMd`, `answerMd`
- Question/answer markdown files referenced by the config

**Quick start:**

```bash
python quiz-markdown-to-web/scripts/package_quiz_web.py --project-root <project_root>
```

Strict validation:

```bash
python quiz-markdown-to-web/scripts/package_quiz_web.py --project-root <project_root> --strict
```

**Output:**

```text
<project-root>/quiz_web/
  index.html
  css/quiz.css
  js/app.js
  js/quiz-data.js
  reports/build-report.json
```

Open `<project-root>/quiz_web/index.html` in a browser when the build finishes.

See [`quiz-markdown-to-web/SKILL.md`](quiz-markdown-to-web/SKILL.md) for agent instructions.
