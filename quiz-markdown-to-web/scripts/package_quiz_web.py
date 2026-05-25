#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def run_cmd(command: list[str]) -> int:
    print("[INFO] run:", " ".join(command))
    return subprocess.run(command, check=False).returncode


def copy_asset(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"[INFO] write asset: {dst}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="One command packaging for quiz_web assets.")
    parser.add_argument("--project-root", required=True, help="Current project root path.")
    parser.add_argument("--chapters", default="chapters.json", help="Chapter config path relative to project root.")
    parser.add_argument("--overrides", default="overrides.json", help="Overrides path relative to project root.")
    parser.add_argument("--quiz-dir", default="quiz_web", help="Output quiz directory name/path relative to project root.")
    parser.add_argument("--strict", action="store_true", help="Enable strict validation and strict build.")
    parser.add_argument("--allow-overrides", action="store_true", help="Enable overrides in build.")
    parser.add_argument("--clean", action="store_true", help="Clean existing quiz_dir before packaging.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent
    templates_dir = skill_root / "templates"

    project_root = Path(args.project_root).resolve()
    quiz_dir = (project_root / args.quiz_dir).resolve()
    if args.clean and quiz_dir.exists():
        shutil.rmtree(quiz_dir)
        print(f"[INFO] removed old dir: {quiz_dir}")

    validate_cmd = [
        sys.executable,
        str(script_dir / "validate_quiz_markdown.py"),
        "--project-root",
        str(project_root),
        "--chapters",
        args.chapters,
    ]
    if args.strict:
        validate_cmd.append("--strict")
    if run_cmd(validate_cmd) != 0:
        print("[ERROR] validation failed; stop packaging.")
        return 1

    build_cmd = [
        sys.executable,
        str(script_dir / "build_quiz_data.py"),
        "--project-root",
        str(project_root),
        "--chapters",
        args.chapters,
        "--overrides",
        args.overrides,
        "--output",
        str(Path(args.quiz_dir) / "js" / "quiz-data.js"),
        "--report-json",
        str(Path(args.quiz_dir) / "reports" / "build-report.json"),
    ]
    if args.strict:
        build_cmd.append("--strict")
    if args.allow_overrides:
        build_cmd.append("--allow-overrides")
    if run_cmd(build_cmd) != 0:
        print("[ERROR] build failed; stop packaging.")
        return 1

    copy_asset(templates_dir / "index.html", quiz_dir / "index.html")
    copy_asset(templates_dir / "quiz.css", quiz_dir / "css" / "quiz.css")
    copy_asset(templates_dir / "app.js", quiz_dir / "js" / "app.js")

    print(f"[INFO] packaged quiz_web at: {quiz_dir}")
    print("PACKAGE_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
