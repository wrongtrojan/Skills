# Examples - Quiz Markdown To Web

## Example 1: One-command packaging

```bash
python scripts/package_quiz_web.py --project-root d:/path/to/your/project
```

Outcome:

- `quiz_web/index.html` ready to open
- `quiz_web/js/quiz-data.js` refreshed
- `quiz_web/reports/build-report.json` written

## Example 2: Strict packaging

```bash
python scripts/package_quiz_web.py --project-root d:/path/to/your/project --strict
```

Use this mode before publishing shared quiz content.

## Example 3: Build only (custom output)

```bash
python scripts/build_quiz_data.py --project-root d:/path/to/your/project --output quiz_web/js/quiz-data.js --report-json quiz_web/reports/build-report.json
```

## Example 4: Use overrides for legacy chapters

When a legacy chapter cannot be standardized immediately, enable overrides:

```bash
python scripts/package_quiz_web.py --project-root d:/path/to/your/project --allow-overrides
```
