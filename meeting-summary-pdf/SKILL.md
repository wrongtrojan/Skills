---
name: meeting-summary-pdf
description: Converts Chinese meeting/retrospective Markdown into fixed-style HTML and A4 PDF with cover, TOC, and CJK nowrap protection. Use when exporting meeting summaries, 复盘总结, formal Chinese docs, or Markdown to HTML to PDF with the seminar summary style.
disable-model-invocation: true
---

# Meeting Summary PDF

## Purpose

Export a Chinese Markdown document to:

- styled `.html` (cover + meta table + TOC + body)
- A4 `.pdf` via headless Chrome/Edge

Use the fixed style from seminar/retrospective summaries (`复盘会议总结` / `meeting-summary-pdf`).

## Required inputs

1. Markdown source (UTF-8), e.g. `第三次研讨会复盘会议总结2.md`
2. Cover config JSON (see [examples/config.example.json](examples/config.example.json))

## Workflow

1. Prepare or update the Markdown body.
2. Create/update a config JSON with `title`, `subtitle`, `meta`, `toc`, optional `nowrap_terms`.
3. Run:

```bash
python meeting-summary-pdf/scripts/build_pdf.py \
  --input path/to/doc.md \
  --config path/to/config.json \
  --output-dir path/to/output
```

4. Spot-check the PDF text layer for CJK wrap issues (`AI 领域`, `7 月 2 日`, etc.).
5. If mixed Chinese/English terms still split, add them to `nowrap_terms` and rebuild.

## Style constraints

Keep these fixed unless the user asks for a design change:

- A4, margins ~17mm/16mm
- Cover page with title, subtitle, 4-row meta table, TOC
- Body fonts: Microsoft YaHei / SimSun
- CJK-safe wrapping: `line-break: strict` + `.nowrap` spans
- No browser header/footer on PDF

## Agent checklist

- [ ] Config title matches document H1 / desired PDF title
- [ ] TOC entries match `##` sections
- [ ] `nowrap_terms` covers known mixed tokens
- [ ] HTML and PDF written to `--output-dir`
- [ ] PDF size > 0 and text extractable

## Additional resources

- Config fields and troubleshooting: [reference.md](reference.md)
- Default CSS: [templates/styles.css](templates/styles.css)
- Example config: [examples/config.example.json](examples/config.example.json)
