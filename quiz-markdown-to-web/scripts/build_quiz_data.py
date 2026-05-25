#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

MAIN_QUESTION_RE = re.compile(r"^\s*(\d+)\.\s+")
PAREN_QUESTION_RE = re.compile(r"^\s*[（(](\d+)[)）]\s*")
NUMBERED_ANSWER_RE = re.compile(
    r"^\s*(?:[-*]\s*)?[（(]?(\d+)[)）](?:[.:：\s]|$)|^\s*(\d+)\.\s+"
)
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
ANSWER_MARKER_RE = re.compile(r"(?:\*\*)?答案(?:：|:)(?:\*\*)?", re.MULTILINE)


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def normalize(text: str) -> str:
    return text.strip("\n").strip()


def split_sections(markdown: str) -> Tuple[str, List[Tuple[str, str]]]:
    matches = list(SECTION_RE.finditer(markdown))
    if not matches:
        return normalize(markdown), []

    intro = normalize(markdown[: matches[0].start()])
    sections: List[Tuple[str, str]] = []
    for idx, match in enumerate(matches):
        section_title = normalize(match.group(1))
        body_start = match.end()
        body_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(markdown)
        section_body = normalize(markdown[body_start:body_end])
        sections.append((section_title, section_body))
    return intro, sections


def split_questions(section_body: str) -> Tuple[str, List[dict]]:
    lines = section_body.split("\n")
    has_main_numbering = any(MAIN_QUESTION_RE.match(line) for line in lines)
    question_re = MAIN_QUESTION_RE if has_main_numbering else PAREN_QUESTION_RE
    blocks: List[Tuple[str, List[str]]] = []
    preamble_lines: List[str] = []
    current_label = ""
    current_lines: List[str] = []
    in_code = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code

        question_match = question_re.match(line) if not in_code else None
        if question_match:
            if current_label:
                blocks.append((current_label, current_lines))
            elif current_lines:
                preamble_lines.extend(current_lines)
            current_label = (question_match.group(1) or "").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_label:
        blocks.append((current_label, current_lines))
    elif current_lines:
        preamble_lines.extend(current_lines)

    questions = [
        {"label": label, "stem": normalize("\n".join(chunk))}
        for label, chunk in blocks
        if normalize("\n".join(chunk))
    ]
    preamble = normalize("\n".join(preamble_lines))
    return preamble, questions


def extract_answer_body(section_body: str) -> str:
    marker = ANSWER_MARKER_RE.search(section_body)
    if not marker:
        return normalize(section_body)
    line_start = section_body.rfind("\n", 0, marker.start())
    if line_start == -1:
        line_start = 0
    else:
        line_start += 1
    return normalize(section_body[line_start:])


def split_answer_items(answer_body: str) -> Dict[int, str]:
    if not answer_body:
        return {}

    lines = answer_body.split("\n")
    items: Dict[int, List[str]] = {}
    current_num = None
    current_lines: List[str] = []
    in_code = False

    def flush() -> None:
        nonlocal current_num, current_lines
        if current_num is None:
            return
        text = normalize("\n".join(current_lines))
        if text:
            items.setdefault(current_num, [])
            items[current_num].append(text)
        current_num = None
        current_lines = []

    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code

        match = NUMBERED_ANSWER_RE.match(line) if not in_code else None
        if match:
            flush()
            current_num = int(match.group(1) or match.group(2))
            current_lines = [line]
        elif current_num is not None:
            current_lines.append(line)

    flush()
    return {k: normalize("\n\n".join(v)) for k, v in items.items()}


def fallback_answers(answer_body: str, question_count: int) -> Dict[int, str]:
    if not answer_body:
        return {}
    if question_count <= 1:
        return {1: answer_body}
    chunks = [normalize(chunk) for chunk in re.split(r"\n\s*\n", answer_body) if normalize(chunk)]
    if len(chunks) >= question_count:
        return {idx + 1: chunks[idx] for idx in range(question_count)}
    return {idx + 1: answer_body for idx in range(question_count)}


def parse_chapters_config(chapters_path: Path) -> List[dict]:
    chapters = json.loads(read_utf8(chapters_path))
    if not isinstance(chapters, list):
        raise ValueError("chapters config must be a json array")
    required = {"id", "title", "order", "questionMd", "answerMd"}
    for idx, item in enumerate(chapters):
        if not isinstance(item, dict):
            raise ValueError(f"chapter entry #{idx+1} must be an object")
        missing = required - set(item.keys())
        if missing:
            raise ValueError(f"chapter entry #{idx+1} missing keys: {sorted(missing)}")
    chapters.sort(key=lambda item: item.get("order", 0))
    return chapters


def chapter_to_data(chapter_cfg: dict, overrides: dict, project_root: Path) -> Tuple[dict, List[str]]:
    chapter_id = chapter_cfg["id"]
    question_md = (project_root / chapter_cfg["questionMd"]).resolve()
    answer_md = (project_root / chapter_cfg["answerMd"]).resolve()

    question_text = read_utf8(question_md)
    answer_text = read_utf8(answer_md)

    intro, question_sections = split_sections(question_text)
    _, answer_sections = split_sections(answer_text)
    answer_by_title = {title: body for title, body in answer_sections}

    chapter_data = {"id": chapter_id, "title": chapter_cfg["title"], "intro": intro, "sections": []}
    warnings: List[str] = []
    chapter_overrides = overrides.get(chapter_id, {})

    for section_index, (title, q_body) in enumerate(question_sections, start=1):
        section_id = f"{chapter_id}-s{section_index}"
        preamble, questions = split_questions(q_body)

        answer_section_body = answer_by_title.get(title, "")
        answer_body = extract_answer_body(answer_section_body)
        numbered_answers = split_answer_items(answer_body)
        if not numbered_answers:
            numbered_answers = fallback_answers(answer_body, len(questions))
        elif len(questions) == 1 and 1 not in numbered_answers and answer_body:
            numbered_answers = {1: answer_body}

        section_questions = []
        section_override = chapter_overrides.get(section_id, {})
        for question_index, question in enumerate(questions, start=1):
            reference = numbered_answers.get(question_index, "")
            override_value = section_override.get(str(question_index - 1))
            if override_value:
                reference = normalize(override_value)
            if not reference:
                warnings.append(f"[WARN] {chapter_id} {section_id} Q{question_index} has no matched reference answer.")
            section_questions.append(
                {
                    "id": f"{section_id}-q{question_index}",
                    "label": question["label"] or str(question_index),
                    "stem": question["stem"],
                    "reference": reference,
                }
            )

        chapter_data["sections"].append(
            {"id": section_id, "title": title, "preamble": preamble, "questions": section_questions}
        )

    return chapter_data, warnings


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build quiz_web/js/quiz-data.js from chapter markdown.")
    parser.add_argument("--project-root", required=True, help="Current project root path.")
    parser.add_argument("--chapters", default="chapters.json", help="Chapter config path relative to project root.")
    parser.add_argument("--overrides", default="overrides.json", help="Overrides path relative to project root.")
    parser.add_argument("--output", default="quiz_web/js/quiz-data.js", help="Output JS path relative to project root.")
    parser.add_argument(
        "--report-json",
        default="quiz_web/reports/build-report.json",
        help="Build report json path relative to project root.",
    )
    parser.add_argument("--strict", action="store_true", help="Fail build when warnings exist.")
    parser.add_argument("--allow-overrides", action="store_true", help="Read overrides json if present.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    chapters_path = (project_root / args.chapters).resolve()
    overrides_path = (project_root / args.overrides).resolve()
    output_path = (project_root / args.output).resolve()
    report_path = (project_root / args.report_json).resolve()

    try:
        chapters = parse_chapters_config(chapters_path)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] invalid chapters config: {exc}")
        return 1

    overrides = {}
    if args.allow_overrides and overrides_path.exists():
        overrides = json.loads(read_utf8(overrides_path))

    chapter_results = []
    all_warnings: List[str] = []
    chapter_stats = []
    for chapter in chapters:
        chapter_data, warnings = chapter_to_data(chapter, overrides, project_root)
        chapter_results.append(chapter_data)
        all_warnings.extend(warnings)
        section_count = len(chapter_data["sections"])
        question_count = sum(len(section["questions"]) for section in chapter_data["sections"])
        chapter_stats.append({"id": chapter_data["id"], "title": chapter_data["title"], "sections": section_count, "questions": question_count})

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("window.QUIZ_DATA = " + json.dumps(chapter_results, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "projectRoot": str(project_root),
        "outputPath": str(output_path),
        "chaptersPath": str(chapters_path),
        "strict": args.strict,
        "allowOverrides": args.allow_overrides,
        "chapterStats": chapter_stats,
        "warnings": all_warnings,
        "warningCount": len(all_warnings),
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[INFO] generated={output_path}")
    print(f"[INFO] report={report_path}")
    print(f"[INFO] chapters={len(chapter_stats)} warnings={len(all_warnings)} strict={args.strict}")
    for chapter in chapter_stats:
        print(f"[INFO] {chapter['id']}: sections={chapter['sections']} questions={chapter['questions']}")
    for warning in all_warnings:
        print(warning)

    if args.strict and all_warnings:
        print("[ERROR] strict mode enabled and warnings found; build failed.")
        return 1

    print("BUILD_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
