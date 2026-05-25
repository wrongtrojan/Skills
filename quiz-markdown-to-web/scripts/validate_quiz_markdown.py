#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Tuple

SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
MAIN_QUESTION_RE = re.compile(r"^\s*(\d+)\.\s+")
PAREN_QUESTION_RE = re.compile(r"^\s*[（(](\d+)[)）]\s*")
ANSWER_MARKER_RE = re.compile(r"(?:\*\*)?答案(?:：|:)(?:\*\*)?", re.MULTILINE)
NUMBERED_ANSWER_RE = re.compile(
    r"^\s*(?:[-*]\s*)?[（(]?(\d+)[)）](?:[.:：\s]|$)|^\s*(\d+)\.\s+"
)


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def normalize(text: str) -> str:
    return text.strip("\n").strip()


def split_sections(markdown: str) -> List[Tuple[str, str]]:
    matches = list(SECTION_RE.finditer(markdown))
    sections: List[Tuple[str, str]] = []
    for idx, match in enumerate(matches):
        title = normalize(match.group(1))
        body_start = match.end()
        body_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(markdown)
        sections.append((title, normalize(markdown[body_start:body_end])))
    return sections


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


def extract_question_numbers(section_body: str) -> Tuple[List[int], List[str]]:
    lines = section_body.split("\n")
    issues: List[str] = []
    in_code = False
    main_hits = sum(1 for line in lines if MAIN_QUESTION_RE.match(line))
    paren_hits = sum(1 for line in lines if PAREN_QUESTION_RE.match(line))
    if main_hits > 0 and paren_hits > 0:
        issues.append("mixed main numbering styles (1. and （1）) in one section")

    question_re = MAIN_QUESTION_RE if main_hits > 0 else PAREN_QUESTION_RE
    numbers: List[int] = []
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        m = question_re.match(line)
        if m:
            numbers.append(int(m.group(1)))
    return numbers, issues


def extract_answer_numbers(section_body: str) -> List[int]:
    marker = ANSWER_MARKER_RE.search(section_body)
    body = section_body if marker is None else section_body[marker.start() :]
    lines = body.split("\n")
    numbers: List[int] = []
    in_code = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
        if in_code:
            continue
        m = NUMBERED_ANSWER_RE.match(line)
        if m:
            numbers.append(int(m.group(1) or m.group(2)))
    return numbers


def check_sequence(nums: List[int]) -> bool:
    return not nums or nums == list(range(1, len(nums) + 1))


def validate_chapter(chapter: dict, project_root: Path, strict: bool) -> List[str]:
    issues: List[str] = []
    chapter_id = chapter["id"]
    question_path = (project_root / chapter["questionMd"]).resolve()
    answer_path = (project_root / chapter["answerMd"]).resolve()
    if not question_path.exists():
        return [f"[ERROR] {chapter_id}: question file not found: {question_path}"]
    if not answer_path.exists():
        return [f"[ERROR] {chapter_id}: answer file not found: {answer_path}"]

    q_sections = split_sections(read_utf8(question_path))
    a_sections = split_sections(read_utf8(answer_path))
    q_titles = [title for title, _ in q_sections]
    a_titles = [title for title, _ in a_sections]
    if q_titles != a_titles:
        level = "ERROR" if strict else "WARN"
        issues.append(f"[{level}] {chapter_id}: section titles mismatch between question and answer files")

    answer_by_title = {title: body for title, body in a_sections}
    for section_idx, (title, q_body) in enumerate(q_sections, start=1):
        sec_tag = f"{chapter_id}#{section_idx}:{title}"
        question_numbers, style_issues = extract_question_numbers(q_body)
        for issue in style_issues:
            level = "ERROR" if strict else "WARN"
            issues.append(f"[{level}] {sec_tag}: {issue}")

        if not question_numbers:
            issues.append(f"[WARN] {sec_tag}: no question numbers detected")
            continue

        level = "ERROR" if strict else "WARN"
        if len(set(question_numbers)) != len(question_numbers):
            issues.append(f"[{level}] {sec_tag}: duplicated question numbers {question_numbers}")
        if not check_sequence(question_numbers):
            issues.append(f"[{level}] {sec_tag}: question numbers should be continuous from 1, got {question_numbers}")

        answer_numbers = extract_answer_numbers(answer_by_title.get(title, ""))
        if len(question_numbers) == 1 and not answer_numbers:
            continue
        if not answer_numbers:
            issues.append(f"[{level}] {sec_tag}: no answer numbers detected")
            continue
        if len(set(answer_numbers)) != len(answer_numbers):
            issues.append(f"[{level}] {sec_tag}: duplicated answer numbers {answer_numbers}")
        if not check_sequence(answer_numbers):
            issues.append(f"[{level}] {sec_tag}: answer numbers should be continuous from 1, got {answer_numbers}")

        q_set, a_set = set(question_numbers), set(answer_numbers)
        missing = sorted(q_set - a_set)
        extra = sorted(a_set - q_set)
        if missing:
            issues.append(f"[{level}] {sec_tag}: missing answers for questions {missing}")
        if extra:
            issues.append(f"[WARN] {sec_tag}: extra answer numbers {extra}")
    return issues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate chapter markdown by schema.")
    parser.add_argument("--project-root", required=True, help="Current project root path.")
    parser.add_argument("--chapters", default="chapters.json", help="Chapter config path relative to project root.")
    parser.add_argument("--strict", action="store_true", help="Treat structural issues as errors.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    chapters_path = (project_root / args.chapters).resolve()

    try:
        chapters = parse_chapters_config(chapters_path)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] invalid chapters config: {exc}")
        return 1

    all_issues: List[str] = []
    for chapter in chapters:
        all_issues.extend(validate_chapter(chapter, project_root, args.strict))

    errors = [item for item in all_issues if item.startswith("[ERROR]")]
    warnings = [item for item in all_issues if item.startswith("[WARN]")]
    print(f"[INFO] chapters={len(chapters)} errors={len(errors)} warnings={len(warnings)} strict={args.strict}")
    for issue in all_issues:
        print(issue)

    if errors:
        return 1
    print("VALIDATION_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
