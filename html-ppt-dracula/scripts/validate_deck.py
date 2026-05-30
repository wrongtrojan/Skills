#!/usr/bin/env python3
"""Core validation for html-ppt-dracula v2 decks (no scaffold/manifest)."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CORE_MARKERS = [
    'id="deck"',
    'class="nav-dots"',
    'e.key === "Escape"',
]

LIGHTBOX_MARKERS = [
    'id="lightbox"',
    'id="lightbox-backdrop"',
    'id="lightbox-close"',
    'id="lightbox-img"',
    'id="lightbox-cap"',
]

DETAIL_MARKERS = [
    'id="detail-overlay"',
    'id="detail-backdrop"',
    'id="detail-close"',
    'id="detail-title"',
    'id="detail-body"',
]

PLACEHOLDER_PATTERN = re.compile(
    r"\[(?:[^\]]*[\u4e00-\u9fff][^\]]*|[^\]]*_[^\]]*)\]"
)


def strip_non_content(html: str) -> str:
    """Remove script/style and inline math before placeholder scan."""
    text = re.sub(r"<script[\s\S]*?</script>", "", html, flags=re.I)
    text = re.sub(r"<style[\s\S]*?</style>", "", text, flags=re.I)
    text = re.sub(r"\$\$[\s\S]*?\$\$", "", text)
    text = re.sub(r"\$[^$\n]+\$", "", text)
    return text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate html-ppt v2 deck structure.")
    parser.add_argument("html_file", help="Deck HTML file path.")
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Do not fail on unresolved [PLACEHOLDER] tokens.",
    )
    parser.add_argument("--placeholder-report-limit", type=int, default=20)
    return parser


def extract_section_ids(html: str) -> list[str]:
    return re.findall(r'<section[^>]+id="([^"]+)"', html)


def extract_nav_ids(html: str) -> list[str]:
    nav_match = re.search(r'<nav[^>]*class="[^"]*nav-dots[^"]*"[^>]*>(.*?)</nav>', html, re.S)
    if not nav_match:
        return []
    return re.findall(r'href="#([^"]+)"', nav_match.group(1))


def extract_script_ids(html: str) -> list[str]:
    match = re.search(r"var\s+ids\s*=\s*(\[[^\]]*\]);", html)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    match = re.search(r"var\s+SLIDE_IDS\s*=\s*(\[[^\]]*\]);", html)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    return []


def extract_unresolved_placeholders(html: str) -> list[tuple[int, str]]:
    unresolved: list[tuple[int, str]] = []
    for line_no, line in enumerate(html.splitlines(), start=1):
        for token in PLACEHOLDER_PATTERN.findall(line):
            unresolved.append((line_no, token))
    return unresolved


def main() -> int:
    args = build_parser().parse_args()
    html_path = Path(args.html_file).expanduser().resolve()
    if not html_path.exists():
        print(f"ERROR: file not found: {html_path}")
        return 2

    html = html_path.read_text(encoding="utf-8", errors="replace")
    issues: list[str] = []

    for marker in CORE_MARKERS:
        if marker not in html:
            issues.append(f"Missing core marker: {marker}")

    if 'id="lightbox"' in html:
        for marker in LIGHTBOX_MARKERS:
            if marker not in html:
                issues.append(f"Missing lightbox marker: {marker}")

    if 'id="detail-overlay"' in html:
        for marker in DETAIL_MARKERS:
            if marker not in html:
                issues.append(f"Missing detail overlay marker: {marker}")

    section_ids = extract_section_ids(html)
    nav_ids = extract_nav_ids(html)
    js_ids = extract_script_ids(html)

    if not section_ids:
        issues.append("No <section id=…> slides found.")
    if section_ids != nav_ids:
        issues.append(f"Nav href IDs mismatch. sections={section_ids} nav={nav_ids}")
    if js_ids and section_ids != js_ids:
        issues.append(f"Script ids array mismatch. sections={section_ids} js={js_ids}")
    if not js_ids:
        issues.append("Missing script ids array (var ids = [...] or SLIDE_IDS in runtime.js linked inline).")

    placeholders = extract_unresolved_placeholders(strip_non_content(html))
    if placeholders and not args.allow_placeholders:
        issues.append(f"Unresolved placeholders found: {len(placeholders)}")
        for line_no, token in placeholders[: args.placeholder_report_limit]:
            issues.append(f"[placeholder] {token} at line {line_no}")

    if issues:
        print("VALIDATION FAILED")
        for item in issues:
            print(f"- {item}")
        return 1

    print("OK: deck validated.")
    print(f"- file: {html_path}")
    print(f"- sections: {len(section_ids)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
