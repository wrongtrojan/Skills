# Reference - Quiz Markdown To Web

## Output Contract

Each run generates or updates:

```text
<project-root>/quiz_web/
  index.html
  css/quiz.css
  js/app.js
  js/quiz-data.js
  reports/build-report.json
```

## Input Contract

- Required config: `<project-root>/chapters.json`
- JSON array; each item needs:
  - `id`
  - `title`
  - `order`
  - `questionMd` (relative to `<project-root>`)
  - `answerMd` (relative to `<project-root>`)

Sample config: [templates/chapters.template.json](templates/chapters.template.json)

## Commands

### Package (recommended)

```bash
python scripts/package_quiz_web.py --project-root <project_root>
```

### Package strict

```bash
python scripts/package_quiz_web.py --project-root <project_root> --strict
```

### Validate only

```bash
python scripts/validate_quiz_markdown.py --project-root <project_root>
```

### Build only

```bash
python scripts/build_quiz_data.py --project-root <project_root> --output quiz_web/js/quiz-data.js --report-json quiz_web/reports/build-report.json
```

## Decision Rules

1. Validation failures block packaging.
2. In strict mode, warnings are treated as failures.
3. Prefer fixing markdown source files before using overrides.

## Schema Rules

- Main question numbering per section should be one style only:
  - `1. 2. 3.` or
  - `（1）（2）（3）`
- Question numbers should be continuous from 1.
- Answer numbers should cover all question numbers.

## Troubleshooting

- Section mismatch: align `##` titles and order.
- Missing answers: add missing numbers under `答案：`.
- Mixed numbering: choose one main numbering style.
