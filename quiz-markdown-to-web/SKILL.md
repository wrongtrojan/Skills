---
name: quiz-markdown-to-web
description: Packages markdown question banks into a ready-to-open quiz_web website in the current project. Use when the user asks to validate chapter markdown, generate quiz HTML assets, or build interactive exercise pages from question/answer files.
disable-model-invocation: true
---

# Quiz Markdown To Web

## Purpose

Use this skill to generate/update `<project-root>/quiz_web/` with all required assets:

- `index.html`
- `css/quiz.css`
- `js/app.js`
- `js/quiz-data.js`
- `reports/build-report.json`

## Required Inputs

- Project has `<project-root>/chapters.json`
- Chapter config entries contain `id/title/order/questionMd/answerMd`
- Question/answer markdown follow [spec/markdown-schema.md](spec/markdown-schema.md)

## Workflow

Run one command:

```bash
python scripts/package_quiz_web.py --project-root <project_root>
```

Strict mode:

```bash
python scripts/package_quiz_web.py --project-root <project_root> --strict
```

Behavior:

1. Validate markdown
2. Build `quiz-data.js`
3. Write/update `quiz_web` template assets
4. Output build report

## New Chapter Quick Start

1. Create or update `<project-root>/chapters.json` from [templates/chapters.template.json](templates/chapters.template.json)
2. Add chapter markdown paths in config
3. Re-run package command

Open:

`<project-root>/quiz_web/index.html`

## Additional Resources

- Contract and behavior: [reference.md](reference.md)
- Usage examples: [examples.md](examples.md)
