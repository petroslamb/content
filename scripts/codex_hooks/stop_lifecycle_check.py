#!/usr/bin/env python3
"""
Codex Stop hook that pressure-tests lifecycle assertions against status.yaml and
the tracked workflow rules.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
PUBLICATIONS_DIR = REPO_ROOT / "publications"
PYTHON_BIN = REPO_ROOT / ".venv" / "bin" / "python"
CHECKER = REPO_ROOT / "scripts" / "check_package_lifecycle.py"
AUTO_CONTINUE_CODES = {
    "readme_stage_mismatch",
    "research_missing_blueprint_path",
    "research_blueprint_path_missing_file",
    "research_blueprint_path_out_of_package",
    "research_blueprint_path_invalid_type",
    "essay_iteration_missing_governing_brief",
    "essay_iteration_missing_packet_scaffold",
    "essay_iteration_prewrite_gate_missing",
    "essay_iteration_prewrite_gate_blocked",
    "essay_iteration_candidate_opened_before_prewrite_clearance",
    "research_has_packet_scaffold",
}
LIFECYCLE_ASSERTION_RE = re.compile(
    r"\b(stage|research|essay[_ ]iteration|governing brief|blueprint|packet|next step|ready to draft|draft gate|prewrite|candidate authorized|writable)\b",
    re.IGNORECASE,
)


def emit_continue() -> None:
    print(json.dumps({"continue": True}))


def resolve_package_from_cwd(cwd_value: str | None) -> str | None:
    if not cwd_value:
        return None
    cwd = Path(cwd_value).resolve()
    candidates = [cwd, *cwd.parents]
    for candidate in candidates:
        status_path = candidate / "status.yaml"
        if not status_path.exists():
            continue
        try:
            return candidate.relative_to(PUBLICATIONS_DIR).as_posix()
        except ValueError:
            continue
    return None


def resolve_package_from_transcript(transcript_path_value: str | None) -> str | None:
    if not transcript_path_value:
        return None
    transcript_path = Path(transcript_path_value)
    if not transcript_path.exists():
        return None

    tail = transcript_path.read_text(errors="ignore")[-12000:]
    package_keys: list[str] = []
    for status_path in PUBLICATIONS_DIR.glob("**/status.yaml"):
        package_key = status_path.parent.relative_to(PUBLICATIONS_DIR).as_posix()
        pattern = re.compile(rf"\b(?:publications/)?{re.escape(package_key)}\b")
        if pattern.search(tail):
            package_keys.append(package_key)
    package_keys = sorted(set(package_keys))
    if len(package_keys) == 1:
        return package_keys[0]
    return None


def run_lifecycle_check(package_key: str) -> dict | None:
    python_bin = PYTHON_BIN if PYTHON_BIN.exists() else Path(sys.executable)
    process = subprocess.run(
        [str(python_bin), str(CHECKER), "--package", package_key, "--format", "json"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if process.returncode != 0:
        return None
    try:
        return json.loads(process.stdout)
    except json.JSONDecodeError:
        return None


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        emit_continue()
        return

    last_message = payload.get("last_assistant_message") or ""
    if not isinstance(last_message, str) or not LIFECYCLE_ASSERTION_RE.search(last_message):
        emit_continue()
        return

    package_key = resolve_package_from_cwd(payload.get("cwd"))
    if package_key is None:
        package_key = resolve_package_from_transcript(payload.get("transcript_path"))
    if package_key is None:
        emit_continue()
        return

    report = run_lifecycle_check(package_key)
    if not report or not report.get("success"):
        emit_continue()
        return

    issues = [
        issue for issue in report.get("issues", [])
        if issue.get("code") in AUTO_CONTINUE_CODES
    ]
    if not issues:
        emit_continue()
        return

    messages = "; ".join(issue["message"] for issue in issues[:2])
    print(
        json.dumps(
            {
                "decision": "block",
                "reason": (
                    f"Re-check {package_key} against status.yaml, config.blueprint_path, and the matching workflow doc "
                    f"before finalizing. Lifecycle warnings: {messages}"
                ),
            }
        )
    )


if __name__ == "__main__":
    main()
