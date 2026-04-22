#!/usr/bin/env python3
"""Validate the current lightweight Reviewable Runs log schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
LOGS_DIR = REPO_ROOT / "reviewable-runs" / "logs"

REQUIRED_V2_COMMON = {
    "kind",
    "schema_version",
    "timestamp",
    "run_id",
    "boundary",
    "task",
    "verification",
}

REQUIRED_LIFECYCLE = REQUIRED_V2_COMMON | {
    "package",
    "stage",
    "action",
    "success",
    "execution",
    "evidence",
    "failure_or_risk",
    "workflow_doc",
    "status_path",
}

REQUIRED_LAUNCH_PACK = REQUIRED_V2_COMMON | {
    "package",
    "stage",
    "task_brief",
    "workflow_doc",
    "required_context",
    "suggested_commands",
    "expected_outputs",
    "done_when",
    "blocking_issues",
}

REQUIRED_WORKFLOW_LAUNCH_PACK = REQUIRED_V2_COMMON | {
    "package",
    "workflow_id",
    "workflow_kind",
    "workflow_doc",
    "required_context",
    "suggested_commands",
    "expected_outputs",
    "blocking_issues",
    "recommended_gates",
}

REQUIRED_WORKFLOW_RUN = REQUIRED_V2_COMMON | {
    "package",
    "workflow_id",
    "workflow_kind",
    "action",
    "success",
    "execution",
    "evidence",
    "failure_or_risk",
    "workflow_doc",
}

REQUIRED_GATE_CHECK = REQUIRED_V2_COMMON | {
    "package",
    "gate_id",
    "decision",
    "status",
    "required_artifacts",
    "missing_artifacts",
    "recommended_workflow",
    "recommended_validator",
    "proof_mode",
}


def require_mapping(value: Any, context: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{context} must be an object")


def require_list(value: Any, context: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        errors.append(f"{context} must be a list")


def validate_v2(path: Path, data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    kind = data.get("kind")
    if kind == "harness_launch_pack":
        required = REQUIRED_LAUNCH_PACK
    elif kind == "workflow_launch_pack":
        required = REQUIRED_WORKFLOW_LAUNCH_PACK
    elif kind == "workflow_run":
        required = REQUIRED_WORKFLOW_RUN
    elif kind == "gate_check":
        required = REQUIRED_GATE_CHECK
    else:
        required = REQUIRED_LIFECYCLE
    missing = sorted(required - data.keys())
    if missing:
        errors.append(f"missing required keys: {', '.join(missing)}")

    for key in ["boundary", "task", "verification"]:
        require_mapping(data.get(key), key, errors)

    boundary = data.get("boundary", {})
    if isinstance(boundary, dict):
        for key in ["type", "reason", "external_side_effect", "approval_required", "approval_status"]:
            if key not in boundary:
                errors.append(f"boundary missing {key}")

    task = data.get("task", {})
    if isinstance(task, dict):
        for key in ["objective", "stop_condition", "non_goals"]:
            if key not in task:
                errors.append(f"task missing {key}")
        if "non_goals" in task:
            require_list(task["non_goals"], "task.non_goals", errors)

    verification = data.get("verification", {})
    if isinstance(verification, dict):
        require_list(verification.get("checks"), "verification.checks", errors)
        if "residual_risk" not in verification:
            errors.append("verification missing residual_risk")

    if kind in {"lifecycle_stage_run", "workflow_run"}:
        require_mapping(data.get("execution"), "execution", errors)
        require_mapping(data.get("evidence"), "evidence", errors)
        require_mapping(data.get("failure_or_risk"), "failure_or_risk", errors)

    if errors:
        rel = path.relative_to(REPO_ROOT).as_posix()
        return [f"{rel}: {error}" for error in errors]
    return []


def main() -> int:
    errors: list[str] = []
    legacy: list[str] = []

    for path in sorted(LOGS_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        schema_version = data.get("schema_version")
        if schema_version is None:
            legacy.append(path.relative_to(REPO_ROOT).as_posix())
            continue
        if schema_version != 2:
            errors.append(f"{path.relative_to(REPO_ROOT).as_posix()}: unsupported schema_version {schema_version!r}")
            continue
        errors.extend(validate_v2(path, data))

    if errors:
        for error in errors:
            print(error)
        return 1

    print(
        json.dumps(
            {
                "checked_dir": LOGS_DIR.relative_to(REPO_ROOT).as_posix(),
                "legacy_logs_grandfathered": legacy,
                "status": "reviewable run logs OK",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
