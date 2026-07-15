#!/usr/bin/env python3
"""Convert Chinese meeting-summary Markdown to fixed-style HTML and A4 PDF."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import markdown
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: markdown. Install with: pip install markdown"
    ) from exc

SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STYLES = SKILL_ROOT / "templates" / "styles.css"

BUILTIN_NOWRAP_TERMS = [
    "Ker / Kernel",
    "Ker 层",
    "Ker 第一层",
    "Kernel",
    "Ker",
    "PPT",
    "poster",
    "AI+NX",
    "AI",
    "taster",
    "logo",
    "checklist",
]


def find_browser() -> Path:
    candidates = [
        shutil.which("chrome"),
        shutil.which("chrome.exe"),
        shutil.which("msedge"),
        shutil.which("msedge.exe"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return Path(candidate)
    raise SystemExit("No Chrome or Edge executable found for PDF generation")


def load_config(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["title", "subtitle", "meta", "toc"]
    missing = [key for key in required if key not in data]
    if missing:
        raise SystemExit(f"Config missing required fields: {', '.join(missing)}")
    if not isinstance(data["meta"], list) or not data["meta"]:
        raise SystemExit("Config field 'meta' must be a non-empty list of [label, value]")
    if not isinstance(data["toc"], list) or not data["toc"]:
        raise SystemExit("Config field 'toc' must be a non-empty list of section titles")
    return data


def protect_terms(text: str, extra_terms: list[str] | None = None) -> tuple[str, dict[str, str]]:
    terms = list(BUILTIN_NOWRAP_TERMS)
    if extra_terms:
        terms.extend(extra_terms)
    # Longer phrases first to avoid partial replacement.
    terms = sorted(set(terms), key=len, reverse=True)
    placeholders: dict[str, str] = {}
    protected = text
    for index, term in enumerate(terms):
        token = f"@@NOWRAP_{index}@@"
        placeholders[token] = f'<span class="nowrap">{html.escape(term)}</span>'
        protected = protected.replace(term, token)
    return protected, placeholders


def markdown_to_body(md_text: str, extra_terms: list[str] | None = None) -> str:
    protected, placeholders = protect_terms(md_text, extra_terms)
    body = markdown.markdown(protected, extensions=["extra", "sane_lists"])
    for token, replacement in placeholders.items():
        body = body.replace(token, replacement)
    body = re.sub(
        r"<code>(.*?)</code>",
        lambda match: f'<code><span class="nowrap">{match.group(1)}</span></code>',
        body,
    )
    return body


def render_html(body: str, config: dict, styles: str) -> str:
    title = html.escape(config["title"])
    subtitle = html.escape(config["subtitle"])
    meta_rows = "".join(
        f"<tr><td>{html.escape(str(label))}</td><td>{html.escape(str(value))}</td></tr>"
        for label, value in config["meta"]
    )
    toc_items = "".join(f"<li>{html.escape(str(item))}</li>" for item in config["toc"])
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>{title}</title><style>
{styles}
</style></head><body><section class="cover"><h1>{title}</h1><div class="subtitle">{subtitle}</div><table class="meta">{meta_rows}</table><div class="toc"><h2>目录</h2><ol>{toc_items}</ol></div></section><article>{body}</article></body></html>
"""


def print_pdf(browser: Path, html_path: Path, pdf_path: Path) -> None:
    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    if result.returncode != 0:
        cmd[1] = "--headless"
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr, file=sys.stderr)
            raise SystemExit(result.returncode)


def build(input_md: Path, config_path: Path, output_dir: Path, styles_path: Path) -> tuple[Path, Path]:
    config = load_config(config_path)
    styles = styles_path.read_text(encoding="utf-8")
    md_text = input_md.read_text(encoding="utf-8")
    body = markdown_to_body(md_text, config.get("nowrap_terms") or [])
    html_doc = render_html(body, config, styles)

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = input_md.stem
    html_path = output_dir / f"{stem}.html"
    pdf_path = output_dir / f"{stem}.pdf"
    html_path.write_text(html_doc, encoding="utf-8")

    browser = find_browser()
    print_pdf(browser, html_path, pdf_path)
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise SystemExit(f"PDF was not created: {pdf_path}")
    return html_path, pdf_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Chinese meeting-summary Markdown to styled HTML and A4 PDF."
    )
    parser.add_argument("--input", required=True, help="Path to Markdown source file")
    parser.add_argument("--config", required=True, help="Path to cover/meta config JSON")
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory for HTML/PDF output (default: current directory)",
    )
    parser.add_argument(
        "--styles",
        default=str(DEFAULT_STYLES),
        help="Optional CSS file override (default: templates/styles.css)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_md = Path(args.input)
    config_path = Path(args.config)
    output_dir = Path(args.output_dir)
    styles_path = Path(args.styles)

    if not input_md.exists():
        raise SystemExit(f"Input markdown not found: {input_md}")
    if not config_path.exists():
        raise SystemExit(f"Config not found: {config_path}")
    if not styles_path.exists():
        raise SystemExit(f"Styles not found: {styles_path}")

    html_path, pdf_path = build(input_md, config_path, output_dir, styles_path)
    print(f"HTML: {html_path}")
    print(f"PDF:  {pdf_path}")
    print(f"Size: {pdf_path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
