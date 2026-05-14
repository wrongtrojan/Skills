#!/usr/bin/env python3
"""Generate a modular HTML deck from registry + component snippets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SECTION_LABELS = {
    "s-cover": "Cover",
    "s-elevator": "One line",
    "s-cap": "Capabilities",
    "s-shots": "UI",
    "s-arch": "Architecture",
    "s-out": "Roadmap",
    "s-take": "Takeaways",
    "s-thanks": "Thanks",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scaffold modular HTML PPT from registry.")
    parser.add_argument("--output", required=True, help="Output HTML path.")
    parser.add_argument("--preset", default="dracula", help="Preset key in registry.")
    parser.add_argument("--components", default="", help="Comma-separated component keys.")
    parser.add_argument("--manifest", default="", help="Manifest JSON path.")
    parser.add_argument("--title", default="研讨会分享", help="Main title.")
    parser.add_argument("--project", default="ContextMap", help="Project name in <title>.")
    parser.add_argument("--subtitle", default="多模态资料 → 大纲 · 溯源 · 验证", help="Cover subtitle.")
    parser.add_argument("--repo-url", default="https://github.com/wrongtrojan/ContextMap", help="Repo URL for thanks footer.")
    parser.add_argument("--repo-text", default="github.com/wrongtrojan/ContextMap", help="Repo text for thanks footer.")
    parser.add_argument("--license-text", default="MIT", help="License text in thanks footer.")
    return parser


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_keys(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def dedupe_keep_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for v in values:
        if v not in seen:
            seen.add(v)
            result.append(v)
    return result


def resolve_component_keys(
    registry: dict[str, Any],
    preset: str,
    cli_components: list[str],
    manifest_data: dict[str, Any],
) -> list[str]:
    presets = registry.get("presets", {})
    preset_defaults = presets.get(preset, {}).get("defaultComponents", [])
    manifest_components = manifest_data.get("components", [])

    # Hybrid priority: manifest > explicit CLI component list > preset defaults.
    if manifest_components:
        keys = manifest_components
    elif cli_components:
        keys = cli_components
    else:
        keys = preset_defaults
    return dedupe_keep_order(list(keys))


def validate_dependencies(components_by_key: dict[str, dict[str, Any]], keys: list[str]) -> None:
    known = set(components_by_key.keys())
    selected = set(keys)
    for key in keys:
        if key not in known:
            raise ValueError(f"Unknown component key: {key}")

    for key in keys:
        meta = components_by_key[key]
        for req in meta.get("requires", []):
            if req not in selected:
                raise ValueError(f"Component {key} requires {req}")
        for bad in meta.get("conflicts", []):
            if bad in selected:
                raise ValueError(f"Component {key} conflicts with {bad}")


def apply_replacements(content: str, values: dict[str, str]) -> str:
    for key, val in values.items():
        content = content.replace(key, val)
    return content


def read_optional(skill_root: Path, rel_path: str) -> str:
    if not rel_path:
        return ""
    full = skill_root / rel_path
    if not full.exists():
        return ""
    return full.read_text(encoding="utf-8").strip()


def build_nav(section_ids: list[str]) -> str:
    lines = []
    for sid in section_ids:
        label = SECTION_LABELS.get(sid, sid)
        lines.append(f'    <a href="#{sid}" aria-label="{label}">{label}</a>')
    return "\n".join(lines)


def main() -> int:
    args = build_parser().parse_args()
    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    registry_path = skill_root / "components" / "registry.json"
    shell_path = skill_root / "assets" / "base" / "shell.html"
    output_path = Path(args.output).expanduser().resolve()

    if not registry_path.exists():
        raise FileNotFoundError(f"Registry not found: {registry_path}")
    if not shell_path.exists():
        raise FileNotFoundError(f"Base shell not found: {shell_path}")

    manifest_data: dict[str, Any] = {}
    if args.manifest:
        manifest_path = Path(args.manifest).expanduser().resolve()
        manifest_data = load_json(manifest_path)

    registry = load_json(registry_path)
    components = registry.get("components", [])
    components_by_key = {item["key"]: item for item in components}

    manifest_preset = manifest_data.get("preset")
    effective_preset = manifest_preset or args.preset

    keys = resolve_component_keys(
        registry=registry,
        preset=effective_preset,
        cli_components=parse_keys(args.components),
        manifest_data=manifest_data,
    )
    validate_dependencies(components_by_key, keys)

    replacements = {
        "[分享标题]": manifest_data.get("title", args.title),
        "[项目名]": manifest_data.get("project", args.project),
        "[分享主标题]": manifest_data.get("title", args.title),
        "[副标题]": manifest_data.get("subtitle", args.subtitle),
        "[一句话定位]": manifest_data.get("positioning", "项目定位"),
        "[核心对象]": manifest_data.get("core_object", "多模态资料"),
        "[核心能力1]": manifest_data.get("core_capability_1", "结构化大纲"),
        "[核心能力2]": manifest_data.get("core_capability_2", "证据溯源"),
        "[仓库链接]": manifest_data.get("repo_url", args.repo_url),
        "[仓库地址]": manifest_data.get("repo_text", args.repo_text),
        "[License]": manifest_data.get("license_text", args.license_text),
    }

    section_htmls: list[str] = []
    overlay_htmls: list[str] = []
    style_chunks: list[str] = []
    script_chunks: list[str] = []
    section_ids: list[str] = []

    for key in keys:
        meta = components_by_key[key]
        html_path = skill_root / meta["html"]
        html_raw = html_path.read_text(encoding="utf-8")
        html_filled = apply_replacements(html_raw, replacements)
        section_htmls.append(html_filled)
        section_ids.append(meta["section"])

        overlay_raw = read_optional(skill_root, meta.get("overlay", ""))
        if overlay_raw:
            overlay_htmls.append(apply_replacements(overlay_raw, replacements))

        css_raw = read_optional(skill_root, meta.get("css", ""))
        if css_raw:
            style_chunks.append(css_raw)

        js_raw = read_optional(skill_root, meta.get("script", ""))
        if js_raw:
            script_chunks.append(js_raw)

    shell = shell_path.read_text(encoding="utf-8")
    shell = apply_replacements(shell, replacements)
    shell = shell.replace("{{NAV_ITEMS}}", build_nav(section_ids))
    shell = shell.replace("{{SECTIONS_HTML}}", "\n".join(section_htmls))
    shell = shell.replace("{{EXTRA_OVERLAYS}}", "\n".join(overlay_htmls))
    shell = shell.replace("{{COMPONENT_STYLES}}", ("\n\n" + "\n\n".join(style_chunks) + "\n") if style_chunks else "")
    shell = shell.replace("{{COMPONENT_SCRIPTS}}", ("\n\n" + "\n\n".join(script_chunks) + "\n") if script_chunks else "")
    shell = shell.replace("{{SECTION_IDS_JSON}}", json.dumps(section_ids, ensure_ascii=False))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(shell, encoding="utf-8")
    print(f"Generated: {output_path}")
    print(f"Preset: {effective_preset}")
    print(f"Components: {', '.join(keys)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

