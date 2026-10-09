---
name: math-notes-pdf
description: Proofreads Chinese math or probability Obsidian notes, then exports a plain A4 PDF with numbered headings, real lists, full-width rules, and a light watermark. Use when the user asks to fix 错别字 or formula subscripts in study notes and convert Markdown to a simple PDF, or mentions Obsidian notes, XeLaTeX, pandoc, or a watermark such as 水印.
---

# Math Notes PDF

Turn an Obsidian math note into a simple PDF. Edit the source only for corrections. Do all layout fixes in a build copy.

## Source edits

Change the note only when the user asked for corrections. Allowed:

- Typos and wrong characters (`Poission` → `Poisson`, `曲弦` → `曲线`)
- Obvious mistakes that contradict the note's own definition
- Missing subscripts (`pX` → `p_X`, `Nt` → `N_t`) and stray formula symbols

Do not reflow paragraphs, insert blank lines, or restyle punctuation in the source. Obsidian already renders tight lists and headings.

## Build

From this skill directory:

```bash
python scripts/build_pdf.py \
  --input path/to/notes.md \
  --title "Document Title" \
  --watermark 木马 \
  --output path/to/notes.pdf
```

The script writes a temporary build copy, then runs pandoc + xelatex. It deletes the build copy when the PDF is written.

Requirements: `pandoc`, `xelatex` (TeX Live with `ctex`), and `typst` when the note embeds SVG via `![[figure.svg]]`.

## Style

Keep these unless the user asks otherwise:

- A4, Song body (`SimSun`), Hei headings (`SimHei`), 11pt, linestretch 1.18
- Centered title, no date, page numbers only (`plain` page style)
- Numbered headings: a top-level `##` note becomes 1, 1.1, 1.1.1, never 0.1
- Ordered lists stay lists, with space between items
- Section rules span the full text width
- Watermark is large, diagonal, and light (`black!10`)

Do not use a variable CJK font such as `Noto Serif SC`. `xdvipdfmx` rejects it with `Invalid font: -1`.

## Verify

Render page 1 and one later page that contains a list and a `---` rule. Check:

- The title is visible and is not numbered `0.1`
- `1.` items are separate lines, not glued to the lead-in sentence
- Subheadings are their own headings
- Rules run the width of the text block
- The watermark is readable but pale
- The source Markdown is unchanged except requested corrections

## Pitfalls the build script already handles

- Pandoc does not treat `1.` or `##` as a list or heading when the previous line is a paragraph. The build copy inserts a blank line first.
- A line of `---` is both a rule and a YAML fence. Replace it with a full-width `\rule` instead of leaving `---`.
- `#` is a section and `##` is a subsection. If the note's top heading is `##`, shift heading levels by `-1` or the first section number is `0.1`.
- `![[name.svg]]` is Obsidian syntax. Convert the SVG to PDF with typst, then include that PDF. XeLaTeX does not embed SVG.
- `--number-sections` turns on running headers once real `\section` commands exist. Force `\pagestyle{plain}`.
