#!/usr/bin/env python3
"""Validate modular html-ppt-dracula outputs (core + enabled components)."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


CORE_MARKERS = [
    'id="deck"',
    'class="nav-dots"',
    'id="lightbox"',
    'id="lightbox-backdrop"',
    'id="lightbox-close"',
    'id="lightbox-img"',
    'id="lightbox-cap"',
    'e.key === "Escape"',
]
PLACEHOLDER_PATTERN = re.compile(r"\[[A-Za-z\u4e00-\u9fff][A-Za-z0-9_\-\u4e00-\u9fff]*\]")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate html-ppt modular structure.")
    parser.add_argument("html_file", help="Generated html file path.")
    parser.add_argument("--manifest", default="", help="Manifest JSON path.")
    parser.add_argument("--components", default="", help="Comma-separated component keys.")
    parser.add_argument("--preset", default="dracula", help="Preset fallback if keys are not explicit.")
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Do not fail when unresolved [PLACEHOLDER] tokens are found.",
    )
    parser.add_argument(
        "--placeholder-report-limit",
        type=int,
        default=20,
        help="Max unresolved placeholders to include in validation output.",
    )
    return parser


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_keys(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def has_id(html: str, target: str) -> bool:
    return re.search(rf'id="{re.escape(target)}"', html) is not None


def has_class(html: str, class_name: str) -> bool:
    pattern = rf'class="[^"]*\b{re.escape(class_name)}\b[^"]*"'
    return re.search(pattern, html) is not None


def extract_section_ids(html: str) -> list[str]:
    return re.findall(r'<section[^>]+id="([^"]+)"', html)


def extract_nav_ids(html: str) -> list[str]:
    return re.findall(r'<a[^>]+href="#([^"]+)"', html)


def extract_script_ids(html: str) -> list[str]:
    match = re.search(r"var\s+ids\s*=\s*(\[[^\]]*\]);", html)
    if not match:
        return []
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return []


def extract_component_keys_from_html(html: str) -> list[str]:
    return re.findall(r'data-component-key="([^"]+)"', html)


def resolve_enabled_keys(
    html: str,
    registry: dict[str, Any],
    preset: str,
    manifest_data: dict[str, Any],
    cli_keys: list[str],
) -> list[str]:
    if manifest_data.get("components"):
        return list(manifest_data["components"])
    if cli_keys:
        return cli_keys
    html_keys = extract_component_keys_from_html(html)
    if html_keys:
        return html_keys
    return list(registry.get("presets", {}).get(preset, {}).get("defaultComponents", []))


def validate_component_dependencies(
    enabled_keys: list[str],
    components_by_key: dict[str, dict[str, Any]],
) -> list[str]:
    issues: list[str] = []
    selected = set(enabled_keys)
    reported_conflicts: set[tuple[str, str]] = set()

    for key in enabled_keys:
        meta = components_by_key.get(key)
        if not meta:
            continue

        for required_key in meta.get("requires", []):
            if required_key not in selected:
                issues.append(f"[{key}] missing required component: {required_key}")

        for conflicting_key in meta.get("conflicts", []):
            if conflicting_key not in selected:
                continue
            pair = tuple(sorted((key, conflicting_key)))
            if pair in reported_conflicts:
                continue
            reported_conflicts.add(pair)
            issues.append(f"[{key}] conflicts with enabled component: {conflicting_key}")

    return issues


def extract_unresolved_placeholders(html: str) -> list[tuple[int, str]]:
    unresolved: list[tuple[int, str]] = []
    for line_no, line in enumerate(html.splitlines(), start=1):
        for match in PLACEHOLDER_PATTERN.findall(line):
            unresolved.append((line_no, match))
    return unresolved


def find_duplicate_keys(keys: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for key in keys:
        if key in seen:
            duplicates.add(key)
        seen.add(key)
    return sorted(duplicates)


def main() -> int:
    args = build_parser().parse_args()
    html_path = Path(args.html_file).expanduser().resolve()
    if not html_path.exists():
        print(f"ERROR: file not found: {html_path}")
        return 2

    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    registry_path = skill_root / "components" / "registry.json"
    if not registry_path.exists():
        print(f"ERROR: registry not found: {registry_path}")
        return 2

    registry = load_json(registry_path)
    components_by_key = {item["key"]: item for item in registry.get("components", [])}

    manifest_data: dict[str, Any] = {}
    if args.manifest:
        manifest_data = load_json(Path(args.manifest).expanduser().resolve())

    html = html_path.read_text(encoding="utf-8", errors="replace")
    issues: list[str] = []

    for marker in CORE_MARKERS:
        if marker not in html:
            issues.append(f"Missing core marker: {marker}")

    section_ids = extract_section_ids(html)
    nav_ids = extract_nav_ids(html)
    js_ids = extract_script_ids(html)

    if section_ids != nav_ids:
        issues.append(f"Nav href IDs mismatch. sections={section_ids} nav={nav_ids}")
    if section_ids != js_ids:
        issues.append(f"Script ids array mismatch. sections={section_ids} js={js_ids}")

    enabled_keys = resolve_enabled_keys(
        html=html,
        registry=registry,
        preset=args.preset,
        manifest_data=manifest_data,
        cli_keys=parse_keys(args.components),
    )
    duplicate_keys = find_duplicate_keys(enabled_keys)
    for dup in duplicate_keys:
        issues.append(f"Duplicate enabled component key: {dup}")

    issues.extend(validate_component_dependencies(enabled_keys, components_by_key))
    expected_sections = [components_by_key[key]["section"] for key in enabled_keys if key in components_by_key]
    if expected_sections and section_ids != expected_sections:
        issues.append(f"Component section order mismatch. sections={section_ids} expected={expected_sections}")

    unresolved_placeholders = extract_unresolved_placeholders(html)
    if unresolved_placeholders and not args.allow_placeholders:
        limit = max(0, args.placeholder_report_limit)
        shown = unresolved_placeholders[:limit] if limit else []
        issues.append(f"Unresolved placeholders found: {len(unresolved_placeholders)}")
        for line_no, token in shown:
            issues.append(f"[placeholder] {token} at line {line_no}")
        if len(unresolved_placeholders) > len(shown):
            hidden_count = len(unresolved_placeholders) - len(shown)
            issues.append(f"[placeholder] ... {hidden_count} more not shown")

    for key in enabled_keys:
        meta = components_by_key.get(key)
        if not meta:
            issues.append(f"Unknown enabled component in validator: {key}")
            continue

        for req_id in meta.get("requiredIds", []):
            if not has_id(html, req_id):
                issues.append(f"[{key}] Missing required id: {req_id}")
        for req_class in meta.get("requiredClasses", []):
            if not has_class(html, req_class):
                issues.append(f"[{key}] Missing required class: {req_class}")

        rule_path_raw = meta.get("validationRule", "")
        if not rule_path_raw:
            continue
        rule_path = skill_root / rule_path_raw
        if not rule_path.exists():
            continue
        rule = load_json(rule_path)
        for marker in rule.get("requiredMarkers", []):
            if marker not in html:
                issues.append(f"[{key}] Missing rule marker: {marker}")
        for req_id in rule.get("requiredIds", []):
            if not has_id(html, req_id):
                issues.append(f"[{key}] Missing rule id: {req_id}")
        for req_class in rule.get("requiredClasses", []):
            if not has_class(html, req_class):
                issues.append(f"[{key}] Missing rule class: {req_class}")

    if issues:
        print("VALIDATION FAILED")
        for item in issues:
            print(f"- {item}")
        return 1

    print("OK: structure validated.")
    print(f"- file: {html_path}")
    print(f"- sections: {len(section_ids)}")
    print(f"- enabled components: {', '.join(enabled_keys)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

