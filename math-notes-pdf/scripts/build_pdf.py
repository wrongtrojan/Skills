"""Build a plain numbered PDF from an Obsidian math note without editing the source."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HEADING = re.compile(r"^#{1,6}\s")
ORDERED = re.compile(r"^\d+\.\s")
WIKI_SVG = re.compile(r"!\[\[([^]]+?\.svg)\]\]")


def latex_escape(text: str) -> str:
    return (
        text.replace("\\", r"\textbackslash{}")
        .replace("&", r"\&")
        .replace("%", r"\%")
        .replace("#", r"\#")
        .replace("_", r"\_")
        .replace("{", r"\{")
        .replace("}", r"\}")
    )


def top_heading_level(lines: list[str]) -> int | None:
    levels = [len(line) - len(line.lstrip("#")) for line in lines if HEADING.match(line.strip())]
    return min(levels) if levels else None


def prepare_body(source: Path, build_dir: Path) -> tuple[Path, int]:
    lines = source.read_text(encoding="utf-8").splitlines()
    shift = -1 if top_heading_level(lines) == 2 else 0
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        is_heading = HEADING.match(stripped) is not None
        is_item = ORDERED.match(stripped) is not None
        is_rule = stripped.startswith("---") and set(stripped) <= set("- \t")
        if (is_heading or is_item) and out and out[-1].strip():
            prev_item = ORDERED.match(out[-1].strip()) is not None
            if not (is_item and prev_item):
                out.append("")
        if is_rule:
            if out and out[-1].strip():
                out.append("")
            out.append(r"\noindent\rule{\linewidth}{0.4pt}")
            out.append("")
            continue
        svg = WIKI_SVG.fullmatch(stripped)
        if svg:
            pdf = convert_svg(source.parent / svg.group(1), build_dir)
            out.append(r"\begin{center}")
            out.append(r"\includegraphics[width=0.92\textwidth]{" + pdf.as_posix() + "}")
            out.append(r"\end{center}")
            continue
        out.append(line)
    body = build_dir / "body.md"
    body.write_text("\n".join(out) + "\n", encoding="utf-8")
    return body, shift


def convert_svg(svg: Path, build_dir: Path) -> Path:
    if not svg.is_file():
        raise SystemExit(f"Missing figure: {svg}")
    if shutil.which("typst") is None:
        raise SystemExit("typst is required to embed Obsidian SVG figures")
    typ = build_dir / f"{svg.stem}.typ"
    pdf = build_dir / f"{svg.stem}.pdf"
    typ.write_text(
        f'#set page(width: auto, height: auto, margin: 0pt)\n#image("{svg.as_posix()}")\n',
        encoding="utf-8",
    )
    subprocess.run(["typst", "compile", str(typ), str(pdf)], check=True)
    return pdf


def write_header(build_dir: Path, title: str, watermark: str) -> Path:
    header = build_dir / "header.tex"
    header.write_text(
        r"""\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{eso-pic}
\usepackage{enumitem}
\newfontfamily\wmfont{SimSun}
\AddToShipoutPictureBG{%
  \AtPageCenter{%
    \makebox(0,0){%
      \rotatebox{32}{\textcolor{black!10}{\wmfont\fontsize{88}{88}\selectfont """
        + latex_escape(watermark)
        + r"""}}%
    }%
  }%
}
\ctexset{
  section = {format = \Large\bfseries\heiti, aftername = \hspace{0.55em}, beforeskip = 18pt, afterskip = 8pt},
  subsection = {format = \large\bfseries\heiti, aftername = \hspace{0.45em}, beforeskip = 13pt, afterskip = 5pt},
  subsubsection = {format = \normalsize\bfseries\heiti, aftername = \hspace{0.4em}, beforeskip = 10pt, afterskip = 4pt},
}
\setlist[enumerate]{leftmargin=2.15em, itemsep=0.45em, topsep=0.55em, parsep=0pt, partopsep=0pt, labelsep=0.45em}
\renewcommand{\maketitle}{%
  \begin{center}
    {\zihao{-2}\bfseries\heiti """
        + latex_escape(title)
        + r"""\par}
    \vspace{0.55em}
    {\color{black!40}\rule{0.28\textwidth}{0.45pt}\par}
  \end{center}
  \vspace{0.9em}
}
\pagestyle{plain}
\AtBeginDocument{\hypersetup{hidelinks}}
""",
        encoding="utf-8",
    )
    return header


def build(source: Path, output: Path, title: str, watermark: str) -> None:
    for tool in ("pandoc", "xelatex"):
        if shutil.which(tool) is None:
            raise SystemExit(f"Missing required tool: {tool}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="math-notes-pdf-") as tmp:
        build_dir = Path(tmp)
        body, shift = prepare_body(source, build_dir)
        header = write_header(build_dir, title, watermark)
        cmd = [
            "pandoc",
            str(body),
            "-o",
            str(output),
            "--pdf-engine=xelatex",
            f"--include-in-header={header}",
            "--number-sections",
            f"--shift-heading-level-by={shift}",
            "-M",
            f"title={title}",
            "-V",
            "documentclass=ctexart",
            "-V",
            "CJKmainfont=SimSun",
            "-V",
            "CJKsansfont=SimHei",
            "-V",
            "fontsize=11pt",
            "-V",
            "linestretch=1.18",
            "-V",
            "geometry:margin=2.35cm",
        ]
        subprocess.run(cmd, check=True)
    if not output.is_file() or output.stat().st_size == 0:
        raise SystemExit("PDF was not written")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--watermark", default="木马")
    args = parser.parse_args()
    if not args.input.is_file():
        raise SystemExit(f"Input not found: {args.input}")
    try:
        build(args.input, args.output.resolve(), args.title, args.watermark)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(exc.returncode) from exc
    print(args.output.resolve())


if __name__ == "__main__":
    sys.exit(main())
