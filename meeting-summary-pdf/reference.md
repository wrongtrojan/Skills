# meeting-summary-pdf Reference

## Config schema

| Field | Type | Required | Meaning |
|-------|------|----------|---------|
| `title` | string | yes | Cover H1 and HTML `<title>` |
| `subtitle` | string | yes | Cover subtitle under H1 |
| `meta` | `[label, value][]` | yes | Cover meta table rows (typically 4) |
| `toc` | `string[]` | yes | Cover directory entries |
| `nowrap_terms` | `string[]` | no | Extra phrases wrapped with `white-space: nowrap` |

Example: [examples/config.example.json](examples/config.example.json)

## Built-in nowrap terms

The script always protects these longer-first tokens:

- `Ker / Kernel`, `Ker 层`, `Ker 第一层`, `Kernel`, `Ker`
- `PPT`, `poster`, `AI+NX`, `AI`
- `taster`, `logo`, `checklist`

Add more via `nowrap_terms` when PDF text layer still shows awkward splits
(e.g. dates like `7 月 12 日`, spans like `5-10 分钟`).

## Pipeline

1. Read Markdown UTF-8
2. Replace nowrap phrases with temporary tokens
3. Convert with `markdown` extensions `extra` + `sane_lists`
4. Restore nowrap `<span class="nowrap">...</span>`
5. Wrap inline `<code>` content with nowrap
6. Inject cover + TOC + [templates/styles.css](templates/styles.css)
7. Write `.html` beside selected output directory
8. Headless Chrome/Edge: `--print-to-pdf` + `--no-pdf-header-footer`

## Browser discovery (Windows)

Probe order:

1. `chrome` / `chrome.exe` / `msedge` / `msedge.exe` on PATH
2. `C:\Program Files\Google\Chrome\Application\chrome.exe`
3. `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`
4. `C:\Program Files\Microsoft\Edge\Application\msedge.exe`
5. `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`

If missing, install Chrome or Edge, or put the binary on PATH.

## CLI

```bash
python scripts/build_pdf.py \
  --input path/to/doc.md \
  --config path/to/config.json \
  --output-dir path/to/output \
  [--styles path/to/custom.css]
```

Outputs:

- `<stem>.html`
- `<stem>.pdf`

where `<stem>` is the Markdown filename without extension.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Mixed CN/EN term breaks across lines | Add phrase to `nowrap_terms` and rebuild |
| PDF not created | Check Chrome/Edge installed; inspect script stderr |
| Console path shows mojibake | Harmless on some GBK consoles; verify with Python `Path.exists()` |
| ReportLab-style bad CJK wrap | Do not use ReportLab for this style; use this script |
| Body H1 duplicated on first page | Expected: first article H1 is CSS-hidden; cover carries the title |

## Dependencies

- Python 3.10+
- `markdown` (`pip install markdown`)
- Google Chrome or Microsoft Edge
