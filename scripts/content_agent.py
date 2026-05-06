#!/usr/bin/env python3
"""Deterministic Phase 2 content-agent facade.

Phase 2.4 adds status, next-action, review-gate inspection, and gate-decision
commands over the Phase 2.1-2.3 file-backed contracts and evidence. The facade
reports enforcement and trace readiness without promoting package state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import shutil
import subprocess
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from check_workflow_yaml_contracts import (
    POLICY_SENSITIVE_ENFORCEMENT_SURFACES,
    REQUIRED_ENFORCEMENT_SURFACES,
    REQUIRED_TRACE_ITEMS,
    VALID_GATE_DECISIONS,
    VALID_ENFORCEMENT_POSTURES,
    path_covered,
    validate_workflow_yaml_contracts,
)
from essay_iteration_support import build_packet_paths
from harness import (
    build_next_action,
    evaluate_gate,
    load_harness_policy,
    load_package_scripts,
    log_gate_check,
    validate_harness_policy,
)
from lifecycle import (
    PUBLICATIONS_DIR,
    REPO_ROOT,
    STAGES,
    WORKFLOWS_DIR,
    active_umbrella_route,
    coerce_package_key,
    load_gate_contracts,
    load_pipeline_profiles,
    load_status_ref,
)


CONTENT_AGENT_VERSION = 1
VALID_RUN_MODES = {"exploratory", "governed_continuous"}
HASHABLE_FILE_LIMIT_BYTES = 5_000_000
REVIEWABLE_RUNS_DIR = REPO_ROOT / "reviewable-runs"
RESOLVED_RUNS_DIR = REVIEWABLE_RUNS_DIR / "resolved-runs"
RUN_RECORDS_DIR = REVIEWABLE_RUNS_DIR / "logs"
REVIEW_GATES_DIR = REVIEWABLE_RUNS_DIR / "gates"
VALID_TERMINAL_STATUSES = {"completed", "gated", "failed", "deferred", "rejected", "superseded"}
VALID_GATE_ARTIFACT_STATUSES = {"pending", "resolved"}
PROMOTED_OUTPUT_STATE_KEYS = {
    "authority_order",
    "claim_state",
    "contradiction_state",
    "validation_state",
    "trace_state",
}
DEFAULT_RECENT_LIMIT = 5


def repo_relpath(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def load_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{repo_relpath(path)} must contain a YAML mapping.")
    return data


def workflow_yaml_paths() -> list[Path]:
    return sorted(
        path
        for path in WORKFLOWS_DIR.glob("*/workflow.yaml")
        if path.parent.name != "skills"
    )


def load_workflow_yaml_contracts() -> dict[str, dict[str, Any]]:
    contracts: dict[str, dict[str, Any]] = {}
    for path in workflow_yaml_paths():
        data = load_mapping(path)
        workflow_id = data.get("workflow_id")
        if not isinstance(workflow_id, str) or not workflow_id:
            continue
        contracts[workflow_id] = {
            "path": path,
            "data": data,
        }
    return contracts


def get_dotted_value(data: dict[str, Any], dotted_key: str) -> Any:
    current: Any = data
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def package_relative_or_repo_path(value: str, package_path: Path) -> Path:
    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return candidate
    if value.startswith("publications/"):
        return REPO_ROOT / value
    package_candidate = package_path / value
    if package_candidate.exists():
        return package_candidate
    return REPO_ROOT / value


def substitute_placeholders(value: str, placeholders: dict[str, Any]) -> str:
    result = value
    for key, replacement in placeholders.items():
        if replacement is None:
            continue
        if isinstance(replacement, (str, int, float, bool)):
            result = result.replace("{" + key + "}", str(replacement))
    return result


def build_placeholders(package_key: str | None, status_data: dict[str, Any] | None) -> dict[str, Any]:
    config = status_data.get("config", {}) if status_data else {}
    placeholders: dict[str, Any] = {
        "package": package_key,
        "package_name": package_key.split("/")[-1] if package_key else None,
        "revision": status_data.get("revision") if status_data else None,
    }
    if isinstance(config, dict):
        placeholders.update(config)
        markdown_path = config.get("markdown_path")
        if isinstance(markdown_path, str):
            placeholders["live_draft_path"] = markdown_path
            placeholders["markdown_path"] = markdown_path
            live_draft = REPO_ROOT / markdown_path
            placeholders["live_draft_stem"] = live_draft.stem
            placeholders["live_draft_dir"] = live_draft.parent.relative_to(REPO_ROOT).as_posix()
    return placeholders


def build_runtime_placeholders(
    package_key: str | None,
    status_data: dict[str, Any] | None,
    runtime_inputs: dict[str, str] | None,
) -> dict[str, Any]:
    placeholders = build_placeholders(package_key, status_data)
    placeholders.update(runtime_inputs or {})
    return placeholders


def hash_file(path: Path) -> dict[str, Any]:
    size = path.stat().st_size
    if size > HASHABLE_FILE_LIMIT_BYTES:
        payload = f"{repo_relpath(path)}\0{size}\0{path.stat().st_mtime_ns}".encode()
        return {
            "type": "file_metadata_sha256",
            "sha256": hashlib.sha256(payload).hexdigest(),
            "size_bytes": size,
        }
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {
        "type": "file_sha256",
        "sha256": digest.hexdigest(),
        "size_bytes": size,
    }


def hash_directory_listing(path: Path) -> dict[str, Any]:
    digest = hashlib.sha256()
    count = 0
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        if ".git" in candidate.parts:
            continue
        rel = candidate.relative_to(path).as_posix()
        stat = candidate.stat()
        digest.update(f"{rel}\0{stat.st_size}\0{stat.st_mtime_ns}\n".encode())
        count += 1
    return {
        "type": "directory_listing_sha256",
        "sha256": digest.hexdigest(),
        "file_count": count,
    }


def hash_path(path: Path) -> dict[str, Any]:
    if path.is_dir():
        return hash_directory_listing(path)
    return hash_file(path)


def first_existing_path(patterns: list[str], placeholders: dict[str, Any], package_path: Path) -> Path | None:
    for pattern in patterns:
        rendered = substitute_placeholders(pattern, placeholders)
        candidate = package_relative_or_repo_path(rendered, package_path)
        if candidate.exists():
            return candidate
    return None


def nearest_blueprint(package_path: Path) -> Path | None:
    roots = [package_path]
    for parent in package_path.parents:
        if parent == PUBLICATIONS_DIR.parent:
            break
        if parent == PUBLICATIONS_DIR:
            continue
        try:
            parent.relative_to(PUBLICATIONS_DIR)
        except ValueError:
            continue
        roots.append(parent)
    for root in roots:
        for pattern in ("*blueprint*.md", "*plan*.md", "*brief*.md"):
            matches = sorted(root.glob(pattern))
            if matches:
                return matches[0]
    return None


def parent_evidence_surface(package_path: Path) -> Path | None:
    try:
        package_path.relative_to(PUBLICATIONS_DIR)
    except ValueError:
        return None
    parent = package_path.parent
    if parent == PUBLICATIONS_DIR:
        return None
    for relpath in ("papers/index.md", "papers", "sources/index.md", "sources"):
        candidate = parent / relpath
        if candidate.exists():
            return candidate
    return None


def fallback_path(fallback: Any, placeholders: dict[str, Any], package_path: Path) -> Path | None:
    if isinstance(fallback, list):
        candidates = [item for item in fallback if isinstance(item, str)]
        existing = first_existing_path(candidates, placeholders, package_path)
        if existing:
            return existing
        for item in candidates:
            if item.startswith("parent package"):
                parent_surface = parent_evidence_surface(package_path)
                if parent_surface:
                    return parent_surface
        return None
    if not isinstance(fallback, str):
        return None
    if "nearest package or parent file" in fallback:
        return nearest_blueprint(package_path)
    rendered = substitute_placeholders(fallback, placeholders)
    candidate = package_relative_or_repo_path(rendered, package_path)
    if candidate.exists():
        return candidate
    return None


def resolve_context_dependency(
    dependency: dict[str, Any],
    package_key: str | None,
    package_path: Path | None,
    status_data: dict[str, Any] | None,
    runtime_inputs: dict[str, str],
) -> dict[str, Any]:
    dependency_id = str(dependency.get("id", "unknown"))
    required = dependency.get("required") is True
    record_hash = dependency.get("record_hash") is True
    placeholders = build_placeholders(package_key, status_data)
    base_path = package_path or REPO_ROOT

    resolved_paths: list[Path] = []
    input_value: Any = None
    status = "resolved"
    reason = None

    if isinstance(dependency.get("path"), str):
        rendered = substitute_placeholders(dependency["path"], placeholders)
        if "{package}" in rendered:
            status = "not_evaluated"
            reason = "package argument not supplied"
        else:
            candidate = package_relative_or_repo_path(rendered, base_path)
            if candidate.exists():
                resolved_paths.append(candidate)
            else:
                status = "missing"
                reason = f"path does not exist: {rendered}"
    elif isinstance(dependency.get("source"), str):
        source = dependency["source"]
        input_keys = [dependency_id]
        if source.startswith("cli."):
            input_keys.append(source.split(".", 1)[1])
        input_value = next((runtime_inputs[key] for key in input_keys if key in runtime_inputs), None)
        if input_value in (None, ""):
            status = "input_required" if required else "not_supplied"
            reason = f"runtime input not supplied for {source}"
    elif package_key is None or package_path is None or status_data is None:
        status = "not_evaluated"
        reason = "package argument not supplied"
    elif isinstance(dependency.get("path_from_status"), str):
        status_value = get_dotted_value(status_data, dependency["path_from_status"])
        if isinstance(status_value, str) and status_value.strip():
            candidate = package_relative_or_repo_path(substitute_placeholders(status_value, placeholders), package_path)
            if candidate.exists():
                resolved_paths.append(candidate)
            else:
                fallback = fallback_path(dependency.get("fallback"), placeholders, package_path)
                if fallback:
                    resolved_paths.append(fallback)
                else:
                    status = "missing"
                    reason = f"status path {dependency['path_from_status']} does not resolve: {status_value}"
        else:
            fallback = fallback_path(dependency.get("fallback"), placeholders, package_path)
            if fallback:
                resolved_paths.append(fallback)
            else:
                status = "missing"
                reason = f"status field is missing: {dependency['path_from_status']}"
    elif isinstance(dependency.get("status_field"), str):
        status_value = get_dotted_value(status_data, dependency["status_field"])
        if status_value in (None, "", []):
            status = "missing"
            reason = f"status field is missing: {dependency['status_field']}"
        else:
            input_value = status_value
    elif isinstance(dependency.get("glob"), list):
        for pattern in dependency["glob"]:
            if not isinstance(pattern, str):
                continue
            rendered = substitute_placeholders(pattern, placeholders)
            if "{package}" in rendered:
                continue
            resolved_paths.extend(sorted((REPO_ROOT).glob(rendered)))
        if not resolved_paths:
            status = "missing" if required else "not_present"
            reason = "no files matched declared glob"
    else:
        status = "not_evaluated"
        reason = "dependency has no path, status_field, source, or glob resolver"

    payload: dict[str, Any] = {
        "id": dependency_id,
        "required": required,
        "status": status,
    }
    if reason:
        payload["reason"] = reason
    if input_value not in (None, ""):
        payload["value"] = input_value
    if resolved_paths:
        payload["paths"] = [repo_relpath(path) for path in resolved_paths]
        if record_hash:
            payload["hashes"] = {
                repo_relpath(path): hash_path(path)
                for path in resolved_paths
            }
    return payload


def normalize_command(command: str) -> str:
    return " ".join(command.replace("{package_key}", "{package}").split())


def command_is_covered(command: str, declared_commands: set[str]) -> bool:
    normalized = normalize_command(command)
    for declared in declared_commands:
        if normalized == declared:
            return True
        if normalized.startswith(declared + " "):
            return True
        if declared.startswith(normalized + " "):
            return True
        pattern = re.escape(declared)
        pattern = re.sub(r"\\\{[^}]+\\\}", r"[^ ]+", pattern)
        if re.fullmatch(pattern, normalized):
            return True
    return False


def split_command(command: str) -> list[str]:
    try:
        tokens = shlex.split(command)
    except ValueError:
        return []
    while tokens and "=" in tokens[0] and not tokens[0].startswith("-"):
        key = tokens[0].split("=", 1)[0]
        if key.replace("_", "").isalnum():
            tokens.pop(0)
            continue
        break
    return tokens


def command_availability(command: str, package_scripts: dict[str, str]) -> tuple[bool, str]:
    tokens = split_command(command)
    if not tokens:
        return False, "command could not be parsed"
    binary = tokens[0]

    if binary == "npm" and len(tokens) >= 3 and tokens[1] == "run":
        script_name = tokens[2]
        if script_name in package_scripts:
            return True, f"npm script exists: {script_name}"
        return False, f"package.json is missing npm script: {script_name}"

    if binary == "content-agent":
        if (REPO_ROOT / "content-agent").exists() or shutil.which("content-agent"):
            return True, "content-agent entrypoint exists"
        return False, "content-agent entrypoint is missing"

    binary_path = REPO_ROOT / binary
    if binary.startswith(".venv/bin/") and binary_path.exists():
        if binary.endswith("/python") and len(tokens) >= 2 and tokens[1].endswith(".py"):
            script_path = REPO_ROOT / tokens[1]
            if "{" not in tokens[1] and not script_path.exists():
                return False, f"python script is missing: {tokens[1]}"
        return True, f"repo-local binary exists: {binary}"

    if "/" in binary:
        if binary_path.exists():
            return True, f"repo path exists: {binary}"
        if "{" in binary:
            return True, "command contains runtime placeholder"
        return False, f"command path is missing: {binary}"

    if shutil.which(binary):
        return True, f"system command exists: {binary}"
    return False, f"command is not available on PATH: {binary}"


def add_finding(
    findings: list[dict[str, Any]],
    severity: str,
    surface: str,
    posture: str,
    message: str,
    workflow_id: str | None = None,
    path: Path | str | None = None,
    evidence: dict[str, Any] | None = None,
) -> None:
    item: dict[str, Any] = {
        "severity": severity,
        "surface": surface,
        "posture": posture,
        "message": message,
    }
    if workflow_id:
        item["workflow_id"] = workflow_id
    if path is not None:
        item["path"] = repo_relpath(path) if isinstance(path, Path) else path
    if evidence:
        item["evidence"] = evidence
    findings.append(item)


def missing_context_severity(mode: str) -> str:
    return "error" if mode == "governed_continuous" else "warning"


def evidence_yaml_paths(directory: Path) -> list[Path]:
    if not directory.exists():
        return []
    return sorted([*directory.glob("*.yaml"), *directory.glob("*.yml")])


def sha256_like(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"(sha256:)?[0-9a-f]{64}", value) is not None


def require_artifact_keys(
    artifact: dict[str, Any],
    required: set[str],
    context: str,
    path: Path,
    findings: list[dict[str, Any]],
    surface: str = "trace_completeness",
    posture: str = "detect",
) -> None:
    missing = sorted(key for key in required if key not in artifact)
    if missing:
        add_finding(
            findings,
            "error",
            surface,
            posture,
            f"{context} is missing required keys: {', '.join(missing)}.",
            path=path,
        )


def require_artifact_mapping(
    artifact: dict[str, Any],
    key: str,
    context: str,
    path: Path,
    findings: list[dict[str, Any]],
    surface: str = "trace_completeness",
    posture: str = "detect",
) -> dict[str, Any]:
    value = artifact.get(key)
    if not isinstance(value, dict):
        add_finding(
            findings,
            "error",
            surface,
            posture,
            f"{context}.{key} must be a mapping.",
            path=path,
        )
        return {}
    return value


def require_artifact_list(
    artifact: dict[str, Any],
    key: str,
    context: str,
    path: Path,
    findings: list[dict[str, Any]],
    surface: str = "trace_completeness",
    posture: str = "detect",
) -> list[Any]:
    value = artifact.get(key)
    if not isinstance(value, list):
        add_finding(
            findings,
            "error",
            surface,
            posture,
            f"{context}.{key} must be a list.",
            path=path,
        )
        return []
    return value


def validate_artifact_repo_path(
    value: Any,
    context: str,
    path: Path,
    findings: list[dict[str, Any]],
    *,
    required: bool = True,
    surface: str = "trace_completeness",
    posture: str = "detect",
) -> None:
    if value in (None, ""):
        if required:
            add_finding(
                findings,
                "error",
                surface,
                posture,
                f"{context} must reference a repo path.",
                path=path,
            )
        return
    if not isinstance(value, str):
        add_finding(
            findings,
            "error",
            surface,
            posture,
            f"{context} must be a string repo path.",
            path=path,
        )
        return
    if re.match(r"^[a-z]+://", value):
        return
    if "{" in value:
        return
    candidate = REPO_ROOT / value
    if not candidate.exists():
        add_finding(
            findings,
            "error",
            surface,
            posture,
            f"{context} points to a missing repo path: {value}.",
            path=path,
        )


def validate_hash_mapping(
    hashes: Any,
    expected_paths: list[Any],
    context: str,
    path: Path,
    findings: list[dict[str, Any]],
) -> None:
    if not isinstance(hashes, dict):
        add_finding(
            findings,
            "error",
            "trace_completeness",
            "detect",
            f"{context}.hashes must be a mapping keyed by repo path.",
            path=path,
        )
        return
    for relpath in expected_paths:
        if not isinstance(relpath, str):
            continue
        hash_record = hashes.get(relpath)
        if not isinstance(hash_record, dict):
            add_finding(
                findings,
                "error",
                "trace_completeness",
                "detect",
                f"{context}.hashes is missing hash record for {relpath}.",
                path=path,
            )
            continue
        if not sha256_like(hash_record.get("sha256")):
            add_finding(
                findings,
                "error",
                "trace_completeness",
                "detect",
                f"{context}.hashes[{relpath}] must include a sha256 digest.",
                path=path,
            )


def validate_context_or_artifact_refs(
    entries: list[Any],
    context: str,
    path: Path,
    findings: list[dict[str, Any]],
    *,
    hashes_required: bool,
) -> None:
    for index, entry in enumerate(entries):
        entry_context = f"{context}[{index}]"
        if not isinstance(entry, dict):
            add_finding(
                findings,
                "error",
                "trace_completeness",
                "detect",
                f"{entry_context} must be a mapping.",
                path=path,
            )
            continue
        if not isinstance(entry.get("id"), str) or not entry["id"]:
            add_finding(
                findings,
                "error",
                "trace_completeness",
                "detect",
                f"{entry_context} must define a non-empty id.",
                path=path,
            )
        paths = entry.get("paths", [])
        if "path" in entry and "paths" not in entry:
            paths = [entry["path"]]
        if not isinstance(paths, list):
            add_finding(
                findings,
                "error",
                "trace_completeness",
                "detect",
                f"{entry_context}.paths must be a list.",
                path=path,
            )
            paths = []
        for relpath in paths:
            validate_artifact_repo_path(relpath, f"{entry_context}.paths", path, findings)
        if hashes_required and paths:
            validate_hash_mapping(entry.get("hashes"), paths, entry_context, path, findings)


def validate_workflow_ref(
    workflow: dict[str, Any],
    context: str,
    path: Path,
    findings: list[dict[str, Any]],
) -> None:
    require_artifact_keys(workflow, {"workflow_id", "workflow_version", "workflow_hash"}, context, path, findings)
    if not isinstance(workflow.get("workflow_id"), str) or not workflow["workflow_id"]:
        add_finding(findings, "error", "trace_completeness", "detect", f"{context}.workflow_id must be non-empty.", path=path)
    if not isinstance(workflow.get("workflow_version"), int):
        add_finding(findings, "error", "trace_completeness", "detect", f"{context}.workflow_version must be an integer.", path=path)
    if not sha256_like(workflow.get("workflow_hash")):
        add_finding(findings, "error", "trace_completeness", "detect", f"{context}.workflow_hash must be a sha256 digest.", path=path)
    validate_artifact_repo_path(workflow.get("contract_path"), f"{context}.contract_path", path, findings, required=False)
    if isinstance(workflow.get("step_id"), str) and not workflow["step_id"]:
        add_finding(findings, "error", "trace_completeness", "detect", f"{context}.step_id must be non-empty when present.", path=path)


def validate_package_ref(
    package: dict[str, Any],
    context: str,
    path: Path,
    findings: list[dict[str, Any]],
) -> None:
    require_artifact_keys(package, {"path", "status_path"}, context, path, findings)
    validate_artifact_repo_path(package.get("path"), f"{context}.path", path, findings)
    validate_artifact_repo_path(package.get("status_path"), f"{context}.status_path", path, findings)
    if "status_hash" in package and not sha256_like(package.get("status_hash")):
        add_finding(findings, "error", "trace_completeness", "detect", f"{context}.status_hash must be a sha256 digest.", path=path)


def validate_promoted_output_state(
    artifact: dict[str, Any],
    path: Path,
    findings: list[dict[str, Any]],
) -> None:
    state = artifact.get("promoted_output_state")
    if not isinstance(state, dict):
        add_finding(
            findings,
            "error",
            "trace_completeness",
            "detect",
            "promoted_output_state must be embedded as a mapping in run or gate evidence.",
            path=path,
        )
        return
    missing = sorted(PROMOTED_OUTPUT_STATE_KEYS - state.keys())
    if missing:
        add_finding(
            findings,
            "error",
            "trace_completeness",
            "detect",
            "promoted_output_state is missing required vocabulary: " + ", ".join(missing) + ".",
            path=path,
        )
    extra = sorted(set(state.keys()) - PROMOTED_OUTPUT_STATE_KEYS)
    if extra:
        add_finding(
            findings,
            "warning",
            "trace_completeness",
            "record",
            "promoted_output_state should stay within the v1 vocabulary.",
            path=path,
            evidence={"extra_keys": extra},
        )


def validate_resolved_run_artifact(path: Path, data: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    context = "resolved_run"
    require_artifact_keys(
        data,
        {
            "kind",
            "schema_version",
            "run_id",
            "package",
            "workflow",
            "run_mode",
            "route",
            "context_admission",
            "policy_resolution",
            "selected_steps",
            "selected_gates",
            "behavior",
            "output_targets",
        },
        context,
        path,
        findings,
    )
    if data.get("kind") != "resolved_run":
        add_finding(findings, "error", "trace_completeness", "detect", "Resolved-run YAML must set kind: resolved_run.", path=path)
    if data.get("schema_version") != CONTENT_AGENT_VERSION:
        add_finding(findings, "error", "trace_completeness", "detect", "resolved_run.schema_version must match content-agent v1.", path=path)
    if not isinstance(data.get("run_id"), str) or not data["run_id"]:
        add_finding(findings, "error", "trace_completeness", "detect", "resolved_run.run_id must be non-empty.", path=path)
    if data.get("run_mode") not in VALID_RUN_MODES:
        add_finding(findings, "error", "trace_completeness", "detect", "resolved_run.run_mode must be exploratory or governed_continuous.", path=path)

    validate_package_ref(require_artifact_mapping(data, "package", context, path, findings), "resolved_run.package", path, findings)
    validate_workflow_ref(require_artifact_mapping(data, "workflow", context, path, findings), "resolved_run.workflow", path, findings)

    validate_context_or_artifact_refs(
        require_artifact_list(data, "context_admission", context, path, findings),
        "resolved_run.context_admission",
        path,
        findings,
        hashes_required=True,
    )
    policy_resolution = require_artifact_mapping(data, "policy_resolution", context, path, findings)
    require_artifact_keys(
        policy_resolution,
        {"allowed_tools", "allowed_capabilities", "allowed_paths"},
        "resolved_run.policy_resolution",
        path,
        findings,
    )
    require_artifact_mapping(policy_resolution, "allowed_paths", "resolved_run.policy_resolution", path, findings)
    behavior = require_artifact_mapping(data, "behavior", context, path, findings)
    require_artifact_keys(behavior, {"budgets", "recovery"}, "resolved_run.behavior", path, findings)
    require_artifact_list(data, "selected_steps", context, path, findings)
    require_artifact_list(data, "selected_gates", context, path, findings)
    require_artifact_list(data, "output_targets", context, path, findings)


def validate_run_record_artifact(path: Path, data: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    context = "run_record"
    require_artifact_keys(
        data,
        {
            "kind",
            "schema_version",
            "run_id",
            "resolved_run_path",
            "package",
            "workflow",
            "run_mode",
            "timestamps",
            "invocation",
            "context_admission",
            "consumed_artifacts",
            "parent_artifacts",
            "produced_artifacts",
            "validation_results",
            "enforcement_outcomes",
            "gate_ids",
            "approval_decisions",
            "external_mutations",
            "terminal_status",
            "promoted_output_state",
        },
        context,
        path,
        findings,
    )
    if data.get("kind") != "run_record":
        add_finding(findings, "error", "trace_completeness", "detect", "Run-record YAML must set kind: run_record.", path=path)
    if data.get("schema_version") != CONTENT_AGENT_VERSION:
        add_finding(findings, "error", "trace_completeness", "detect", "run_record.schema_version must match content-agent v1.", path=path)
    if not isinstance(data.get("run_id"), str) or not data["run_id"]:
        add_finding(findings, "error", "trace_completeness", "detect", "run_record.run_id must be non-empty.", path=path)
    if data.get("run_mode") not in VALID_RUN_MODES:
        add_finding(findings, "error", "trace_completeness", "detect", "run_record.run_mode must be exploratory or governed_continuous.", path=path)
    if data.get("terminal_status") not in VALID_TERMINAL_STATUSES:
        add_finding(
            findings,
            "error",
            "trace_completeness",
            "detect",
            "run_record.terminal_status must be one of the Phase 2 terminal statuses.",
            path=path,
        )

    validate_artifact_repo_path(data.get("resolved_run_path"), "run_record.resolved_run_path", path, findings)
    validate_package_ref(require_artifact_mapping(data, "package", context, path, findings), "run_record.package", path, findings)
    validate_workflow_ref(require_artifact_mapping(data, "workflow", context, path, findings), "run_record.workflow", path, findings)
    timestamps = require_artifact_mapping(data, "timestamps", context, path, findings)
    require_artifact_keys(timestamps, {"started_at", "ended_at"}, "run_record.timestamps", path, findings)
    invocation = require_artifact_mapping(data, "invocation", context, path, findings)
    require_artifact_keys(invocation, {"entrypoint", "command"}, "run_record.invocation", path, findings)

    validate_context_or_artifact_refs(
        require_artifact_list(data, "context_admission", context, path, findings),
        "run_record.context_admission",
        path,
        findings,
        hashes_required=True,
    )
    validate_context_or_artifact_refs(
        require_artifact_list(data, "consumed_artifacts", context, path, findings),
        "run_record.consumed_artifacts",
        path,
        findings,
        hashes_required=True,
    )
    validate_context_or_artifact_refs(
        require_artifact_list(data, "parent_artifacts", context, path, findings),
        "run_record.parent_artifacts",
        path,
        findings,
        hashes_required=False,
    )
    validate_context_or_artifact_refs(
        require_artifact_list(data, "produced_artifacts", context, path, findings),
        "run_record.produced_artifacts",
        path,
        findings,
        hashes_required=False,
    )
    validation_results = require_artifact_list(data, "validation_results", context, path, findings)
    for index, result in enumerate(validation_results):
        if not isinstance(result, dict):
            add_finding(findings, "error", "trace_completeness", "detect", f"run_record.validation_results[{index}] must be a mapping.", path=path)
            continue
        require_artifact_keys(result, {"id", "status"}, f"run_record.validation_results[{index}]", path, findings)
    enforcement_outcomes = require_artifact_list(data, "enforcement_outcomes", context, path, findings)
    for index, outcome in enumerate(enforcement_outcomes):
        if not isinstance(outcome, dict):
            add_finding(findings, "error", "trace_completeness", "detect", f"run_record.enforcement_outcomes[{index}] must be a mapping.", path=path)
            continue
        require_artifact_keys(outcome, {"surface", "posture", "status"}, f"run_record.enforcement_outcomes[{index}]", path, findings)
    require_artifact_list(data, "gate_ids", context, path, findings)
    require_artifact_list(data, "approval_decisions", context, path, findings)
    external_mutations = require_artifact_list(data, "external_mutations", context, path, findings)
    for index, mutation in enumerate(external_mutations):
        if not isinstance(mutation, dict):
            add_finding(findings, "error", "external_mutation", "deny", f"run_record.external_mutations[{index}] must be a mapping.", path=path)
            continue
        if "status" not in mutation:
            add_finding(findings, "error", "external_mutation", "deny", f"run_record.external_mutations[{index}] must record status.", path=path)
        status = mutation.get("status")
        if status in {"attempted", "performed", "requested"} and not mutation.get("approval_reference"):
            add_finding(
                findings,
                "error",
                "external_mutation",
                "deny",
                f"run_record.external_mutations[{index}] requires an approval_reference.",
                path=path,
            )
    validate_promoted_output_state(data, path, findings)


def validate_review_gate_artifact(
    path: Path,
    data: dict[str, Any],
    gate_contracts: dict[str, Any],
    findings: list[dict[str, Any]],
) -> None:
    context = "review_gate"
    require_artifact_keys(
        data,
        {
            "kind",
            "schema_version",
            "gate_id",
            "status",
            "gate_type",
            "gate_contract",
            "package",
            "workflow",
            "run",
            "stop",
            "evidence",
            "approval",
            "resume",
            "promoted_output_state",
            "decision",
        },
        context,
        path,
        findings,
        surface="review_gates",
        posture="deny",
    )
    if data.get("kind") != "review_gate":
        add_finding(findings, "error", "review_gates", "deny", "Review-gate YAML must set kind: review_gate.", path=path)
    if data.get("schema_version") != CONTENT_AGENT_VERSION:
        add_finding(findings, "error", "review_gates", "deny", "review_gate.schema_version must match content-agent v1.", path=path)
    if data.get("status") not in VALID_GATE_ARTIFACT_STATUSES:
        add_finding(findings, "error", "review_gates", "deny", "review_gate.status must be pending or resolved.", path=path)

    gate_contract_id = data.get("gate_contract")
    gate_contract = gate_contracts.get(gate_contract_id)
    if not isinstance(gate_contract_id, str) or not gate_contract:
        add_finding(
            findings,
            "error",
            "review_gates",
            "deny",
            f"review_gate.gate_contract must reference gate_contracts.yaml, got {gate_contract_id!r}.",
            path=path,
        )
        gate_contract = {}
    expected_gate_type = gate_contract.get("gate_type")
    if expected_gate_type and data.get("gate_type") != expected_gate_type:
        add_finding(
            findings,
            "error",
            "review_gates",
            "deny",
            "review_gate.gate_type must match gate_contracts.yaml.",
            path=path,
            evidence={"expected": expected_gate_type, "actual": data.get("gate_type")},
        )

    validate_package_ref(require_artifact_mapping(data, "package", context, path, findings, "review_gates", "deny"), "review_gate.package", path, findings)
    workflow = require_artifact_mapping(data, "workflow", context, path, findings, "review_gates", "deny")
    validate_workflow_ref(workflow, "review_gate.workflow", path, findings)
    if not isinstance(workflow.get("step_id"), str) or not workflow.get("step_id"):
        add_finding(findings, "error", "review_gates", "deny", "review_gate.workflow.step_id must identify the stopped step.", path=path)

    run = require_artifact_mapping(data, "run", context, path, findings, "review_gates", "deny")
    require_artifact_keys(run, {"run_id", "resolved_run_path", "run_record_path"}, "review_gate.run", path, findings, "review_gates", "deny")
    validate_artifact_repo_path(run.get("resolved_run_path"), "review_gate.run.resolved_run_path", path, findings, surface="review_gates", posture="deny")
    validate_artifact_repo_path(run.get("run_record_path"), "review_gate.run.run_record_path", path, findings, surface="review_gates", posture="deny")

    stop = require_artifact_mapping(data, "stop", context, path, findings, "review_gates", "deny")
    require_artifact_keys(stop, {"reason", "created_at", "created_by"}, "review_gate.stop", path, findings, "review_gates", "deny")

    evidence = require_artifact_mapping(data, "evidence", context, path, findings, "review_gates", "deny")
    preview_paths = require_artifact_list(evidence, "preview_paths", "review_gate.evidence", path, findings, "review_gates", "deny")
    evidence_paths = require_artifact_list(evidence, "evidence_paths", "review_gate.evidence", path, findings, "review_gates", "deny")
    for relpath in [*preview_paths, *evidence_paths]:
        validate_artifact_repo_path(relpath, "review_gate.evidence paths", path, findings, surface="review_gates", posture="deny")
    validation_results = require_artifact_list(evidence, "validation_results", "review_gate.evidence", path, findings, "review_gates", "deny")
    for index, result in enumerate(validation_results):
        if isinstance(result, dict):
            require_artifact_keys(result, {"id", "status"}, f"review_gate.evidence.validation_results[{index}]", path, findings, "review_gates", "deny")
    enforcement_outcomes = require_artifact_list(evidence, "enforcement_outcomes", "review_gate.evidence", path, findings, "review_gates", "deny")
    for index, outcome in enumerate(enforcement_outcomes):
        if isinstance(outcome, dict):
            require_artifact_keys(outcome, {"surface", "posture", "status"}, f"review_gate.evidence.enforcement_outcomes[{index}]", path, findings, "review_gates", "deny")

    approval = require_artifact_mapping(data, "approval", context, path, findings, "review_gates", "deny")
    approval_required_keys = {
        "quality_required",
        "external_mutation_required",
        "lifecycle_movement_required",
        "promotion_required",
        "allowed_decisions",
    }
    require_artifact_keys(approval, approval_required_keys, "review_gate.approval", path, findings, "review_gates", "deny")
    for key in approval_required_keys - {"allowed_decisions"}:
        if not isinstance(approval.get(key), bool):
            add_finding(findings, "error", "review_gates", "deny", f"review_gate.approval.{key} must be boolean.", path=path)
    decisions = approval.get("allowed_decisions")
    if not isinstance(decisions, list) or not decisions or not set(decisions) <= VALID_GATE_DECISIONS:
        add_finding(findings, "error", "review_gates", "deny", "review_gate.approval.allowed_decisions must be approve/reject/defer.", path=path)
    approval_dimensions = gate_contract.get("approval_dimensions", {}) if isinstance(gate_contract, dict) else {}
    if isinstance(approval_dimensions, dict):
        dimension_map = {
            "quality": "quality_required",
            "external_mutation": "external_mutation_required",
            "lifecycle_movement": "lifecycle_movement_required",
            "promotion": "promotion_required",
        }
        for contract_key, artifact_key in dimension_map.items():
            if approval_dimensions.get(contract_key) is True and approval.get(artifact_key) is not True:
                add_finding(
                    findings,
                    "error",
                    "review_gates",
                    "deny",
                    f"review_gate.approval.{artifact_key} must preserve gate_contracts.yaml approval dimension {contract_key}.",
                    path=path,
                )
    if data.get("gate_type") == "external_mutation" and approval.get("external_mutation_required") is not True:
        add_finding(
            findings,
            "error",
            "external_mutation",
            "deny",
            "External-mutation gates must explicitly require external_mutation approval.",
            path=path,
        )

    resume = require_artifact_mapping(data, "resume", context, path, findings, "review_gates", "deny")
    require_artifact_keys(resume, {"on_approve", "on_reject", "on_defer", "command_hint"}, "review_gate.resume", path, findings, "review_gates", "deny")

    decision = data.get("decision")
    if data.get("status") == "pending" and decision is not None:
        add_finding(findings, "error", "review_gates", "deny", "Pending review gates must have decision: null.", path=path)
    if data.get("status") == "resolved":
        if not isinstance(decision, dict):
            add_finding(findings, "error", "review_gates", "deny", "Resolved review gates must include a decision record.", path=path)
        else:
            require_artifact_keys(
                decision,
                {"decided_at", "decided_by", "outcome", "quality_approved", "external_mutation_approved", "lifecycle_movement_approved", "promotion_approved", "reason"},
                "review_gate.decision",
                path,
                findings,
                "review_gates",
                "deny",
            )
            if decision.get("outcome") not in VALID_GATE_DECISIONS:
                add_finding(findings, "error", "review_gates", "deny", "review_gate.decision.outcome must be approve, reject, or defer.", path=path)
    validate_promoted_output_state(data, path, findings)


def validate_no_standalone_promoted_output_manifests(findings: list[dict[str, Any]]) -> None:
    if not REVIEWABLE_RUNS_DIR.exists():
        return
    for path in sorted([*REVIEWABLE_RUNS_DIR.rglob("*.yaml"), *REVIEWABLE_RUNS_DIR.rglob("*.yml")]):
        try:
            data = yaml.safe_load(path.read_text()) or {}
        except Exception:
            continue
        if isinstance(data, dict) and data.get("kind") == "promoted_output_state":
            add_finding(
                findings,
                "error",
                "trace_completeness",
                "deny",
                "Phase 2.3 forbids standalone promoted-output manifests; embed state in run records or gates.",
                path=path,
            )


def validate_execution_evidence_artifacts(
    root: dict[str, Any],
    findings: list[dict[str, Any]],
) -> dict[str, Any]:
    stores = {
        "resolved_runs": RESOLVED_RUNS_DIR,
        "run_records": RUN_RECORDS_DIR,
        "review_gates": REVIEW_GATES_DIR,
    }
    summary: dict[str, Any] = {
        "stores": {name: repo_relpath(path) for name, path in stores.items()},
        "counts": {"resolved_run": 0, "run_record": 0, "review_gate": 0},
        "checked_paths": [],
    }
    for name, directory in stores.items():
        if not directory.exists():
            add_finding(
                findings,
                "error",
                "trace_completeness",
                "detect",
                f"Execution evidence store is missing: {repo_relpath(directory)}.",
                path=directory,
            )

    gate_contracts = root.get("gate_contracts", {})
    for kind, directory, validator in [
        ("resolved_run", RESOLVED_RUNS_DIR, validate_resolved_run_artifact),
        ("run_record", RUN_RECORDS_DIR, validate_run_record_artifact),
    ]:
        for path in evidence_yaml_paths(directory):
            try:
                data = load_mapping(path)
            except Exception as exc:
                add_finding(findings, "error", "trace_completeness", "detect", f"Failed to load execution evidence YAML: {exc}", path=path)
                continue
            if data.get("kind") != kind:
                add_finding(
                    findings,
                    "error",
                    "trace_completeness",
                    "detect",
                    f"{repo_relpath(path)} is in the {kind} store but declares kind {data.get('kind')!r}.",
                    path=path,
                )
                continue
            validator(path, data, findings)
            summary["counts"][kind] += 1
            summary["checked_paths"].append(repo_relpath(path))

    for path in evidence_yaml_paths(REVIEW_GATES_DIR):
        try:
            data = load_mapping(path)
        except Exception as exc:
            add_finding(findings, "error", "review_gates", "deny", f"Failed to load review gate YAML: {exc}", path=path)
            continue
        if data.get("kind") != "review_gate":
            add_finding(
                findings,
                "error",
                "review_gates",
                "deny",
                f"{repo_relpath(path)} is in the review_gate store but declares kind {data.get('kind')!r}.",
                path=path,
            )
            continue
        validate_review_gate_artifact(path, data, gate_contracts if isinstance(gate_contracts, dict) else {}, findings)
        summary["counts"]["review_gate"] += 1
        summary["checked_paths"].append(repo_relpath(path))

    validate_no_standalone_promoted_output_manifests(findings)
    return summary


def validate_root_surfaces(findings: list[dict[str, Any]]) -> dict[str, Any]:
    root: dict[str, Any] = {}
    try:
        policy = load_harness_policy()
        root["harness_policy"] = policy
        for error in validate_harness_policy(policy):
            add_finding(findings, "error", "contract_shape", "deny", error, path="harness_policy.yaml")
        run_modes = policy.get("governed_execution", {}).get("run_modes", [])
        if not isinstance(run_modes, list) or not VALID_RUN_MODES <= set(run_modes):
            add_finding(
                findings,
                "error",
                "package_route_resolution",
                "deny",
                "harness_policy.yaml governed_execution.run_modes must include exploratory and governed_continuous.",
                path="harness_policy.yaml",
            )
        enforcement = policy.get("enforcement_surfaces", {})
        if not isinstance(enforcement, dict):
            add_finding(
                findings,
                "error",
                "contract_shape",
                "deny",
                "harness_policy.yaml enforcement_surfaces must be a mapping.",
                path="harness_policy.yaml",
            )
        else:
            missing = [surface for surface in REQUIRED_ENFORCEMENT_SURFACES if surface not in enforcement]
            if missing:
                add_finding(
                    findings,
                    "error",
                    "contract_shape",
                    "deny",
                    "harness_policy.yaml enforcement_surfaces is missing required surfaces.",
                    path="harness_policy.yaml",
                    evidence={"missing": missing},
                )
            for surface, posture in enforcement.items():
                if posture not in VALID_ENFORCEMENT_POSTURES:
                    add_finding(
                        findings,
                        "error",
                        "contract_shape",
                        "deny",
                        f"harness_policy.yaml enforcement surface '{surface}' has invalid posture '{posture}'.",
                        path="harness_policy.yaml",
                    )
                if surface in POLICY_SENSITIVE_ENFORCEMENT_SURFACES and posture != "deny":
                    add_finding(
                        findings,
                        "error",
                        surface,
                        str(posture),
                        f"Policy-sensitive surface '{surface}' must be deny at the policy floor.",
                        path="harness_policy.yaml",
                    )
    except Exception as exc:
        add_finding(findings, "error", "contract_shape", "deny", f"Failed to load harness_policy.yaml: {exc}")

    try:
        root["gate_contracts"] = load_gate_contracts()
    except Exception as exc:
        add_finding(findings, "error", "review_gates", "deny", f"Failed to load gate_contracts.yaml: {exc}")

    try:
        root["pipeline_profiles"] = load_pipeline_profiles()
    except Exception as exc:
        add_finding(findings, "error", "package_route_resolution", "deny", f"Failed to load pipeline_profiles.yaml: {exc}")

    try:
        root["package_scripts"] = load_package_scripts()
    except Exception as exc:
        add_finding(findings, "error", "tool_use", "deny", f"Failed to load package.json scripts: {exc}")
        root["package_scripts"] = {}

    return root


def validate_workflow_static(
    workflow_id: str,
    contract_path: Path,
    contract: dict[str, Any],
    root: dict[str, Any],
    findings: list[dict[str, Any]],
) -> None:
    enforcement = contract.get("enforcement", {})
    if not isinstance(enforcement, dict):
        return
    for surface in REQUIRED_ENFORCEMENT_SURFACES:
        posture = enforcement.get(surface)
        if posture is None:
            add_finding(
                findings,
                "error",
                surface,
                "deny",
                f"Workflow '{workflow_id}' does not declare enforcement.{surface}.",
                workflow_id=workflow_id,
                path=contract_path,
            )
        elif posture not in VALID_ENFORCEMENT_POSTURES:
            add_finding(
                findings,
                "error",
                surface,
                str(posture),
                f"Workflow '{workflow_id}' declares invalid enforcement posture for {surface}.",
                workflow_id=workflow_id,
                path=contract_path,
            )

    trace = contract.get("trace", {})
    trace_include = trace.get("include", []) if isinstance(trace, dict) else []
    missing_trace = sorted(REQUIRED_TRACE_ITEMS - set(trace_include if isinstance(trace_include, list) else []))
    if missing_trace:
        add_finding(
            findings,
            "error",
            "trace_completeness",
            str(enforcement.get("trace_completeness", "detect")),
            f"Workflow '{workflow_id}' is missing trace-readiness fields.",
            workflow_id=workflow_id,
            path=contract_path,
            evidence={"missing": missing_trace},
        )

    package_scripts = root.get("package_scripts", {})
    tools = contract.get("capabilities", {}).get("tools", [])
    declared_commands: set[str] = set()
    if isinstance(tools, list):
        for tool in tools:
            if not isinstance(tool, dict) or not isinstance(tool.get("command"), str):
                continue
            command = tool["command"]
            declared_commands.add(normalize_command(command))
            available, reason = command_availability(command, package_scripts)
            if not available and tool.get("required") is True:
                add_finding(
                    findings,
                    "error",
                    "tool_use",
                    str(enforcement.get("tool_use", "deny")),
                    f"Required tool '{tool.get('id')}' is not available: {reason}.",
                    workflow_id=workflow_id,
                    path=contract_path,
                )

    hooks = contract.get("validation", {}).get("hooks", [])
    if isinstance(hooks, list):
        for hook in hooks:
            if not isinstance(hook, dict) or not isinstance(hook.get("command"), str):
                continue
            command = hook["command"]
            available, reason = command_availability(command, package_scripts)
            if not available and hook.get("required") is True:
                add_finding(
                    findings,
                    "error",
                    "validation_hooks",
                    str(enforcement.get("validation_hooks", "deny")),
                    f"Required validation hook '{hook.get('id')}' is not available: {reason}.",
                    workflow_id=workflow_id,
                    path=contract_path,
                )
            if not command_is_covered(command, declared_commands) and not command.startswith("content-agent"):
                add_finding(
                    findings,
                    "warning",
                    "validation_hooks",
                    str(enforcement.get("validation_hooks", "deny")),
                    f"Validation hook '{hook.get('id')}' is not also declared as a capability tool.",
                    workflow_id=workflow_id,
                    path=contract_path,
                )

    steps = contract.get("steps", [])
    if isinstance(steps, list):
        for step in steps:
            if not isinstance(step, dict):
                continue
            executor = step.get("executor")
            if isinstance(executor, dict) and isinstance(executor.get("command"), str):
                command = executor["command"]
                if not command_is_covered(command, declared_commands):
                    add_finding(
                        findings,
                        "error",
                        "tool_use",
                        str(enforcement.get("tool_use", "deny")),
                        f"Scriptable step '{step.get('id')}' uses an undeclared command.",
                        workflow_id=workflow_id,
                        path=contract_path,
                        evidence={"command": command},
                    )

    policy_writes = root.get("harness_policy", {}).get("local_write_allowed", {}).get("paths", [])
    allowed_write = contract.get("allowed_paths", {}).get("write", [])
    if isinstance(policy_writes, list) and isinstance(allowed_write, list):
        for pattern in allowed_write:
            if not isinstance(pattern, str):
                continue
            if "{" in pattern:
                policy_equivalent = pattern.split("{", 1)[0]
            else:
                policy_equivalent = pattern
            if not path_covered(policy_equivalent, [item for item in policy_writes if isinstance(item, str)]):
                add_finding(
                    findings,
                    "error",
                    "path_access",
                    str(enforcement.get("path_access", "deny")),
                    "Workflow write path is outside harness_policy.yaml local_write_allowed paths.",
                    workflow_id=workflow_id,
                    path=contract_path,
                    evidence={"write_path": pattern},
                )


def validate_package_route(
    workflow_id: str,
    contract_path: Path,
    contract: dict[str, Any],
    package_key: str,
    status_data: dict[str, Any],
    findings: list[dict[str, Any]],
) -> None:
    enforcement = contract.get("enforcement", {})
    package_kind = status_data.get("kind", "leaf")
    package_classes = contract.get("package_classes", [])
    if package_kind not in package_classes:
        add_finding(
            findings,
            "error",
            "package_route_resolution",
            str(enforcement.get("package_route_resolution", "deny")),
            f"Package kind '{package_kind}' is not supported by workflow '{workflow_id}'.",
            workflow_id=workflow_id,
            path=contract_path,
            evidence={"package": package_key, "package_classes": package_classes},
        )

    if package_kind == "umbrella" and active_umbrella_route(status_data) is None and "umbrella" in package_classes:
        add_finding(
            findings,
            "info",
            "package_route_resolution",
            str(enforcement.get("package_route_resolution", "deny")),
            "Umbrella package has no active umbrella_route; settled umbrellas may have no next executable lifecycle step.",
            workflow_id=workflow_id,
            path=contract_path,
            evidence={"package": package_key},
        )


def validate_context_admission(
    workflow_id: str,
    contract_path: Path,
    contract: dict[str, Any],
    package_key: str | None,
    package_path: Path | None,
    status_data: dict[str, Any] | None,
    runtime_inputs: dict[str, str],
    mode: str,
    findings: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    enforcement = contract.get("enforcement", {})
    placeholders = build_placeholders(package_key, status_data)
    raw_read_patterns = contract.get("allowed_paths", {}).get("read", [])
    read_patterns = [
        substitute_placeholders(item, placeholders)
        for item in raw_read_patterns
        if isinstance(item, str)
    ] if isinstance(raw_read_patterns, list) else []
    context_results = []
    for dependency in contract.get("context_dependencies", []):
        if not isinstance(dependency, dict):
            continue
        result = resolve_context_dependency(dependency, package_key, package_path, status_data, runtime_inputs)
        context_results.append(result)
        required = result.get("required") is True
        if result["status"] in {"missing", "input_required"} and required:
            if package_key is None:
                continue
            add_finding(
                findings,
                missing_context_severity(mode),
                "context_admission",
                str(enforcement.get("context_admission", "deny")),
                f"Required context dependency '{result['id']}' was not admitted: {result.get('reason')}.",
                workflow_id=workflow_id,
                path=contract_path,
            )
        for relpath in result.get("paths", []):
            if not path_covered(relpath, read_patterns):
                add_finding(
                    findings,
                    "error",
                    "path_access",
                    str(enforcement.get("path_access", "deny")),
                    f"Context dependency '{result['id']}' resolved outside allowed_paths.read.",
                    workflow_id=workflow_id,
                    path=contract_path,
                    evidence={"context_path": relpath},
                )
    return context_results


def validate_gates_and_trace(
    workflow_id: str,
    contract_path: Path,
    contract: dict[str, Any],
    root: dict[str, Any],
    findings: list[dict[str, Any]],
) -> None:
    enforcement = contract.get("enforcement", {})
    gate_contracts = root.get("gate_contracts", {})
    gates = contract.get("gates", [])
    if not isinstance(gates, list):
        return

    for gate in gates:
        if not isinstance(gate, dict):
            continue
        gate_id = gate.get("id")
        contract_id = gate.get("contract")
        gate_contract = gate_contracts.get(contract_id)
        if not gate_contract:
            continue
        approval_dimensions = gate_contract.get("approval_dimensions", {})
        gate_type = gate_contract.get("gate_type") or gate.get("type")
        if gate_type == "external_mutation" and enforcement.get("external_mutation") != "deny":
            add_finding(
                findings,
                "error",
                "external_mutation",
                str(enforcement.get("external_mutation", "record")),
                f"External-mutation gate '{gate_id}' requires enforcement.external_mutation: deny.",
                workflow_id=workflow_id,
                path=contract_path,
            )
        for dimension in ("external_mutation", "lifecycle_movement", "promotion"):
            if approval_dimensions.get(dimension) is True and enforcement.get(dimension) != "deny":
                add_finding(
                    findings,
                    "error",
                    dimension,
                    str(enforcement.get(dimension, "record")),
                    f"Gate '{gate_id}' approves {dimension}, so enforcement.{dimension} must be deny.",
                    workflow_id=workflow_id,
                    path=contract_path,
                )

    trace = contract.get("trace", {})
    if isinstance(trace, dict):
        if gates and not trace.get("gate_store"):
            add_finding(
                findings,
                "error",
                "review_gates",
                str(enforcement.get("review_gates", "deny")),
                "Gated workflow must declare trace.gate_store.",
                workflow_id=workflow_id,
                path=contract_path,
            )
        resolved_run = trace.get("resolved_run", {})
        persist_when = resolved_run.get("persist_when", []) if isinstance(resolved_run, dict) else []
        if gates and "gated" not in persist_when:
            add_finding(
                findings,
                "error",
                "trace_completeness",
                str(enforcement.get("trace_completeness", "detect")),
                "Gated workflow must persist resolved runs when gated.",
                workflow_id=workflow_id,
                path=contract_path,
            )


def validate_essay_iteration_packet_drift(
    workflow_id: str,
    contract_path: Path,
    package_key: str | None,
    package_path: Path | None,
    status_data: dict[str, Any] | None,
    findings: list[dict[str, Any]],
) -> None:
    if workflow_id != "essay_iteration" or not package_key or not package_path or not status_data:
        return
    config = status_data.get("config", {})
    markdown_path = config.get("markdown_path") if isinstance(config, dict) else None
    revision = status_data.get("revision", 1)
    if not isinstance(markdown_path, str) or not isinstance(revision, int):
        return
    live_draft = package_relative_or_repo_path(markdown_path, package_path)
    manifest_path = build_packet_paths(live_draft, revision)["manifest"]
    if not manifest_path.exists():
        add_finding(
            findings,
            "warning",
            "validation_hooks",
            "detect",
            "Essay-iteration packet drift check could not run because the current revision packet is missing.",
            workflow_id=workflow_id,
            path=contract_path,
            evidence={"expected_packet": repo_relpath(manifest_path)},
        )
        return
    try:
        packet = json.loads(manifest_path.read_text())
    except Exception as exc:
        add_finding(
            findings,
            "error",
            "validation_hooks",
            "detect",
            f"Essay-iteration packet drift check could not parse packet JSON: {exc}",
            workflow_id=workflow_id,
            path=manifest_path,
        )
        return

    expected_doc = "workflows/essay-iteration/README.md"
    expected_manifest = repo_relpath(manifest_path)
    drift: dict[str, Any] = {}
    if packet.get("package") != package_key:
        drift["package"] = {"expected": package_key, "actual": packet.get("package")}
    if packet.get("workflow_doc") != expected_doc:
        drift["workflow_doc"] = {"expected": expected_doc, "actual": packet.get("workflow_doc")}
    if packet.get("packet_manifest_path") != expected_manifest:
        drift["packet_manifest_path"] = {
            "expected": expected_manifest,
            "actual": packet.get("packet_manifest_path"),
        }
    if drift:
        add_finding(
            findings,
            "error",
            "validation_hooks",
            "detect",
            "Essay-iteration packet manifest has source-linked drift.",
            workflow_id=workflow_id,
            path=manifest_path,
            evidence=drift,
        )


def build_validation_report(
    workflow_id: str | None = None,
    package_arg: str | None = None,
    mode: str = "exploratory",
    runtime_inputs: dict[str, str] | None = None,
) -> dict[str, Any]:
    if mode not in VALID_RUN_MODES:
        raise ValueError(f"mode must be one of: {', '.join(sorted(VALID_RUN_MODES))}")
    runtime_inputs = runtime_inputs or {}
    findings: list[dict[str, Any]] = []
    root = validate_root_surfaces(findings)
    execution_evidence = validate_execution_evidence_artifacts(root, findings)

    static_errors = validate_workflow_yaml_contracts()
    for error in static_errors:
        add_finding(findings, "error", "contract_shape", "deny", error)

    contracts = load_workflow_yaml_contracts()
    if workflow_id:
        if workflow_id not in contracts:
            raise KeyError(f"Unknown workflow '{workflow_id}'.")
        selected = {workflow_id: contracts[workflow_id]}
    else:
        selected = contracts

    package_key = None
    package_path = None
    status_data = None
    if package_arg:
        manifest_ref, status_data = load_status_ref(package_arg)
        package_key = manifest_ref.package_key
        package_path = manifest_ref.package_path

    workflow_reports = []
    for selected_workflow_id, loaded in selected.items():
        contract_path = loaded["path"]
        contract = loaded["data"]
        workflow_report: dict[str, Any] = {
            "workflow_id": selected_workflow_id,
            "contract_path": repo_relpath(contract_path),
            "enforcement": contract.get("enforcement", {}),
        }

        validate_workflow_static(selected_workflow_id, contract_path, contract, root, findings)
        if package_key and status_data:
            validate_package_route(selected_workflow_id, contract_path, contract, package_key, status_data, findings)
        context_results = validate_context_admission(
            selected_workflow_id,
            contract_path,
            contract,
            package_key,
            package_path,
            status_data,
            runtime_inputs,
            mode,
            findings,
        )
        validate_gates_and_trace(selected_workflow_id, contract_path, contract, root, findings)
        validate_essay_iteration_packet_drift(
            selected_workflow_id,
            contract_path,
            package_key,
            package_path,
            status_data,
            findings,
        )
        workflow_report["context_admission"] = context_results
        workflow_reports.append(workflow_report)

    return {
        "kind": "content_agent_validation_report",
        "schema_version": CONTENT_AGENT_VERSION,
        "mode": mode,
        "package": package_key,
        "success": not any(item["severity"] == "error" for item in findings),
        "findings": findings,
        "execution_evidence": execution_evidence,
        "workflows": workflow_reports,
    }


def parse_runtime_inputs(values: list[str]) -> dict[str, str]:
    inputs: dict[str, str] = {}
    for value in values:
        if "=" not in value:
            raise ValueError(f"--input expects key=value, got: {value}")
        key, raw = value.split("=", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"--input key cannot be empty: {value}")
        inputs[key] = raw
    return inputs


def severity_counts(findings: list[dict[str, Any]]) -> dict[str, int]:
    counts = {"error": 0, "warning": 0, "info": 0}
    for finding in findings:
        severity = str(finding.get("severity", "info"))
        counts[severity] = counts.get(severity, 0) + 1
    return counts


def summarize_validation_health(report: dict[str, Any]) -> dict[str, Any]:
    findings = report.get("findings", [])
    if not isinstance(findings, list):
        findings = []
    evidence = report.get("execution_evidence", {})
    counts = evidence.get("counts", {}) if isinstance(evidence, dict) else {}
    return {
        "success": report.get("success") is True,
        "mode": report.get("mode"),
        "package": report.get("package"),
        "severity_counts": severity_counts([item for item in findings if isinstance(item, dict)]),
        "finding_count": len(findings),
        "execution_evidence_counts": counts,
        "top_findings": [
            {
                "severity": item.get("severity"),
                "surface": item.get("surface"),
                "posture": item.get("posture"),
                "workflow_id": item.get("workflow_id"),
                "path": item.get("path"),
                "message": item.get("message"),
            }
            for item in findings[:5]
            if isinstance(item, dict)
        ],
    }


def gate_package_key(data: dict[str, Any]) -> str | None:
    package = data.get("package")
    if not isinstance(package, dict):
        return None
    package_path = package.get("path")
    if isinstance(package_path, str) and package_path:
        return coerce_package_key(package_path)
    status_path = package.get("status_path")
    if isinstance(status_path, str) and status_path.startswith("publications/"):
        return coerce_package_key(status_path.removesuffix("/status.yaml"))
    return None


def package_ref_matches(data: dict[str, Any], package_key: str | None) -> bool:
    if package_key is None:
        return True
    return gate_package_key(data) == package_key


def summarize_review_gate(path: Path, data: dict[str, Any]) -> dict[str, Any]:
    package = data.get("package") if isinstance(data.get("package"), dict) else {}
    workflow = data.get("workflow") if isinstance(data.get("workflow"), dict) else {}
    run = data.get("run") if isinstance(data.get("run"), dict) else {}
    stop = data.get("stop") if isinstance(data.get("stop"), dict) else {}
    decision = data.get("decision") if isinstance(data.get("decision"), dict) else None
    return {
        "path": repo_relpath(path),
        "gate_id": data.get("gate_id"),
        "status": data.get("status"),
        "gate_type": data.get("gate_type"),
        "gate_contract": data.get("gate_contract"),
        "package": package.get("path"),
        "package_key": gate_package_key(data),
        "workflow_id": workflow.get("workflow_id"),
        "step_id": workflow.get("step_id"),
        "run_id": run.get("run_id"),
        "created_at": stop.get("created_at"),
        "stop_reason": stop.get("reason"),
        "decision_outcome": decision.get("outcome") if decision else None,
        "decided_at": decision.get("decided_at") if decision else None,
        "retained_example": data.get("retained_example") is True,
    }


def load_review_gate_records(
    package_arg: str | None = None,
    *,
    include_retained: bool = False,
) -> list[dict[str, Any]]:
    package_key = coerce_package_key(package_arg) if package_arg else None
    records: list[dict[str, Any]] = []
    for path in evidence_yaml_paths(REVIEW_GATES_DIR):
        try:
            data = load_mapping(path)
        except Exception as exc:
            records.append({
                "path": repo_relpath(path),
                "status": "invalid",
                "error": str(exc),
            })
            continue
        if data.get("kind") != "review_gate":
            continue
        if not package_ref_matches(data, package_key):
            continue
        if data.get("retained_example") is True and not include_retained:
            continue
        records.append(summarize_review_gate(path, data))
    return sorted(
        records,
        key=lambda item: (
            str(item.get("created_at") or ""),
            str(item.get("gate_id") or ""),
            str(item.get("path") or ""),
        ),
        reverse=True,
    )


def summarize_run_record(path: Path, data: dict[str, Any]) -> dict[str, Any]:
    package = data.get("package") if isinstance(data.get("package"), dict) else {}
    workflow = data.get("workflow") if isinstance(data.get("workflow"), dict) else {}
    timestamps = data.get("timestamps") if isinstance(data.get("timestamps"), dict) else {}
    return {
        "path": repo_relpath(path),
        "run_id": data.get("run_id"),
        "package": package.get("path"),
        "package_key": gate_package_key(data),
        "workflow_id": workflow.get("workflow_id"),
        "run_mode": data.get("run_mode"),
        "terminal_status": data.get("terminal_status"),
        "started_at": timestamps.get("started_at"),
        "ended_at": timestamps.get("ended_at"),
        "gate_ids": data.get("gate_ids") if isinstance(data.get("gate_ids"), list) else [],
    }


def run_record_sort_key(record: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(record.get("ended_at") or record.get("started_at") or record.get("timestamp") or ""),
        str(record.get("run_id") or ""),
        str(record.get("path") or ""),
    )


def load_yaml_run_records(package_arg: str | None = None, limit: int | None = None) -> list[dict[str, Any]]:
    package_key = coerce_package_key(package_arg) if package_arg else None
    records: list[dict[str, Any]] = []
    for path in evidence_yaml_paths(RUN_RECORDS_DIR):
        try:
            data = load_mapping(path)
        except Exception as exc:
            records.append({
                "path": repo_relpath(path),
                "kind": "invalid",
                "error": str(exc),
            })
            continue
        if data.get("kind") != "run_record":
            continue
        if not package_ref_matches(data, package_key):
            continue
        records.append(summarize_run_record(path, data))
    records = sorted(records, key=run_record_sort_key, reverse=True)
    return records[:limit] if limit is not None else records


def legacy_log_package_key(data: dict[str, Any]) -> str | None:
    value = data.get("package") or data.get("package_key")
    if isinstance(value, str) and value and value != "no-package":
        return coerce_package_key(value)
    return None


def summarize_legacy_json_log(path: Path, data: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": repo_relpath(path),
        "kind": data.get("kind"),
        "schema_version": data.get("schema_version"),
        "timestamp": data.get("timestamp"),
        "run_id": data.get("run_id"),
        "package": data.get("package"),
        "package_key": legacy_log_package_key(data),
        "workflow": data.get("workflow") or data.get("workflow_id"),
        "stage": data.get("stage"),
        "gate_id": data.get("gate_id"),
        "status": data.get("status"),
        "decision": data.get("decision"),
    }


def load_legacy_json_logs(package_arg: str | None = None, limit: int | None = None) -> list[dict[str, Any]]:
    package_key = coerce_package_key(package_arg) if package_arg else None
    records: list[dict[str, Any]] = []
    if not RUN_RECORDS_DIR.exists():
        return records
    for path in sorted(RUN_RECORDS_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except Exception as exc:
            records.append({
                "path": repo_relpath(path),
                "kind": "invalid_json",
                "error": str(exc),
            })
            continue
        if not isinstance(data, dict):
            continue
        if package_key is not None and legacy_log_package_key(data) != package_key:
            continue
        records.append(summarize_legacy_json_log(path, data))
    records = sorted(records, key=run_record_sort_key, reverse=True)
    return records[:limit] if limit is not None else records


def current_stage(status_data: dict[str, Any]) -> str | None:
    stages = status_data.get("stages", {})
    if not isinstance(stages, dict):
        return None
    for stage in STAGES:
        stage_data = stages.get(stage)
        if isinstance(stage_data, dict) and stage_data.get("done") is not True:
            return stage
    for stage, stage_data in stages.items():
        if isinstance(stage_data, dict) and stage_data.get("done") is not True:
            return str(stage)
    return None


def summarize_package_status(package_arg: str) -> dict[str, Any]:
    manifest_ref, status_data = load_status_ref(package_arg)
    stages = status_data.get("stages", {})
    stage_items = []
    if isinstance(stages, dict):
        for stage in [*STAGES, *sorted(set(stages) - set(STAGES))]:
            stage_data = stages.get(stage)
            if not isinstance(stage_data, dict):
                continue
            stage_items.append({
                "stage": stage,
                "done": stage_data.get("done") is True,
                "last_updated": stage_data.get("last_updated"),
            })
    umbrella_route = active_umbrella_route(status_data)
    return {
        "package": manifest_ref.package_key,
        "path": repo_relpath(manifest_ref.package_path),
        "status_path": repo_relpath(manifest_ref.status_path),
        "kind": status_data.get("kind", "leaf"),
        "publication": status_data.get("publication"),
        "revision": status_data.get("revision", 1),
        "current_stage": current_stage(status_data),
        "umbrella_route": umbrella_route,
        "stages": stage_items,
    }


def build_root_surface_summary() -> dict[str, Any]:
    workflow_contracts = load_workflow_yaml_contracts()
    gate_contracts = load_gate_contracts()
    pipeline_profiles = load_pipeline_profiles()
    policy = load_harness_policy()
    return {
        "workflow_yaml_contracts": [
            {
                "workflow_id": workflow_id,
                "path": repo_relpath(loaded["path"]),
            }
            for workflow_id, loaded in sorted(workflow_contracts.items())
        ],
        "workflow_yaml_count": len(workflow_contracts),
        "gate_contracts": sorted(gate_contracts),
        "gate_contract_count": len(gate_contracts),
        "pipeline_profiles": sorted(pipeline_profiles),
        "pipeline_profile_count": len(pipeline_profiles),
        "harness_policy_path": "harness_policy.yaml",
        "harness_policy_sections": sorted(policy),
    }


def split_gate_statuses(gates: list[dict[str, Any]]) -> dict[str, Any]:
    pending = [gate for gate in gates if gate.get("status") == "pending"]
    resolved = [gate for gate in gates if gate.get("status") == "resolved"]
    invalid = [gate for gate in gates if gate.get("status") == "invalid"]
    return {
        "pending_count": len(pending),
        "resolved_count": len(resolved),
        "invalid_count": len(invalid),
        "pending": pending,
        "resolved": resolved,
        "invalid": invalid,
    }


def build_status_report(package_arg: str | None = None, limit: int = DEFAULT_RECENT_LIMIT) -> dict[str, Any]:
    validation_report = build_validation_report(package_arg=package_arg)
    gates = load_review_gate_records(package_arg)
    return {
        "kind": "content_agent_status",
        "schema_version": CONTENT_AGENT_VERSION,
        "package": summarize_package_status(package_arg) if package_arg else None,
        "root_surfaces": build_root_surface_summary(),
        "review_gates": split_gate_statuses(gates),
        "recent_runs": {
            "yaml_run_records": load_yaml_run_records(package_arg, limit),
            "legacy_json_logs": load_legacy_json_logs(package_arg, limit),
        },
        "validation_health": summarize_validation_health(validation_report),
    }


def build_init_report(check_only: bool = False) -> dict[str, Any]:
    directories = [
        RESOLVED_RUNS_DIR,
        RUN_RECORDS_DIR,
        REVIEW_GATES_DIR,
    ]
    directory_records = []
    for directory in directories:
        existed = directory.exists()
        if not existed and not check_only:
            directory.mkdir(parents=True, exist_ok=True)
        directory_records.append({
            "path": repo_relpath(directory),
            "existed_before": existed,
            "exists_after": directory.exists(),
            "created": not existed and directory.exists() and not check_only,
        })
    validation_report = build_validation_report()
    return {
        "kind": "content_agent_init",
        "schema_version": CONTENT_AGENT_VERSION,
        "check_only": check_only,
        "runtime_directories": directory_records,
        "root_surfaces": build_root_surface_summary(),
        "validation_health": summarize_validation_health(validation_report),
        "message": "content-agent runtime surfaces are initialized",
    }


def build_review_list_report(
    package_arg: str | None = None,
    status_filter: str = "all",
    *,
    include_retained: bool = False,
) -> dict[str, Any]:
    gates = load_review_gate_records(package_arg, include_retained=include_retained)
    if status_filter != "all":
        gates = [gate for gate in gates if gate.get("status") == status_filter]
    gate_statuses = split_gate_statuses(gates)
    return {
        "kind": "content_agent_review_list",
        "schema_version": CONTENT_AGENT_VERSION,
        "filters": {
            "package": coerce_package_key(package_arg) if package_arg else None,
            "status": status_filter,
            "include_retained": include_retained,
        },
        "counts": {
            "pending": gate_statuses["pending_count"],
            "resolved": gate_statuses["resolved_count"],
            "invalid": gate_statuses["invalid_count"],
        },
        "gates": gates,
    }


def resolve_review_gate_path(identifier: str) -> Path:
    candidate = Path(identifier).expanduser()
    if candidate.is_absolute() and candidate.exists():
        return candidate
    repo_candidate = (REPO_ROOT / candidate).resolve()
    if repo_candidate.exists():
        return repo_candidate

    matches = []
    for path in evidence_yaml_paths(REVIEW_GATES_DIR):
        try:
            data = load_mapping(path)
        except Exception:
            continue
        if data.get("kind") != "review_gate":
            continue
        if identifier in {str(data.get("gate_id")), path.name, path.stem}:
            matches.append(path)
    if not matches:
        raise FileNotFoundError(f"No review gate found for '{identifier}'.")
    if len(matches) > 1:
        raise ValueError(f"Review gate identifier is ambiguous: {identifier}")
    return matches[0]


def build_review_inspect_report(identifier: str) -> dict[str, Any]:
    path = resolve_review_gate_path(identifier)
    data = load_mapping(path)
    if data.get("kind") != "review_gate":
        raise ValueError(f"{repo_relpath(path)} is not a review_gate artifact.")
    return {
        "kind": "content_agent_review_inspect",
        "schema_version": CONTENT_AGENT_VERSION,
        "gate": summarize_review_gate(path, data),
        "artifact": data,
    }


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def filename_timestamp(timestamp: str) -> str:
    return timestamp.replace(":", "-")


def slugify(value: str | None) -> str:
    if not value:
        return "item"
    slug = re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-").lower()
    return slug or "item"


def repo_path_from_artifact_value(value: Any, context: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{context} must be a non-empty repo path.")
    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        try:
            candidate.resolve().relative_to(REPO_ROOT)
        except ValueError as exc:
            raise ValueError(f"{context} must stay inside the repository: {value}") from exc
        return candidate.resolve()
    return (REPO_ROOT / candidate).resolve()


def artifact_ref(
    artifact_id: str,
    paths: list[str],
    *,
    hashes_required: bool = False,
    precomputed_hashes: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    entry: dict[str, Any] = {
        "id": artifact_id,
        "paths": paths,
    }
    if hashes_required:
        hashes: dict[str, dict[str, Any]] = {}
        for relpath in paths:
            if precomputed_hashes and relpath in precomputed_hashes:
                hashes[relpath] = precomputed_hashes[relpath]
                continue
            hashes[relpath] = hash_path(repo_path_from_artifact_value(relpath, f"{artifact_id}.paths"))
        entry["hashes"] = hashes
    return entry


def unique_yaml_path(directory: Path, stem: str) -> Path:
    path = directory / f"{stem}.yaml"
    if not path.exists():
        return path
    for index in range(2, 1000):
        candidate = directory / f"{stem}-{index}.yaml"
        if not candidate.exists():
            return candidate
    raise FileExistsError(f"Could not find a unique path for {stem}.yaml")


def write_yaml_mapping(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = yaml.safe_dump(data, sort_keys=False, allow_unicode=False)
    temp_path = path.with_name(f".{path.name}.tmp")
    temp_path.write_text(rendered)
    temp_path.replace(path)


APPROVAL_DIMENSION_REQUIRED_KEYS = {
    "quality": "quality_required",
    "external_mutation": "external_mutation_required",
    "lifecycle_movement": "lifecycle_movement_required",
    "promotion": "promotion_required",
}


def approval_dimension_records(approval: dict[str, Any], outcome: str) -> dict[str, dict[str, bool]]:
    dimensions: dict[str, dict[str, bool]] = {}
    for dimension, required_key in APPROVAL_DIMENSION_REQUIRED_KEYS.items():
        required = approval.get(required_key) is True
        dimensions[dimension] = {
            "required": required,
            "approved": outcome == "approve" and required,
        }
    return dimensions


def build_decision_record(
    data: dict[str, Any],
    outcome: str,
    *,
    decided_at: str,
    decided_by: str,
    reason: str,
    run_record_path: str | None = None,
) -> dict[str, Any]:
    approval = data.get("approval") if isinstance(data.get("approval"), dict) else {}
    dimensions = approval_dimension_records(approval, outcome)
    decision: dict[str, Any] = {
        "decided_at": decided_at,
        "decided_by": decided_by,
        "outcome": outcome,
        "quality_approved": dimensions["quality"]["approved"],
        "external_mutation_approved": dimensions["external_mutation"]["approved"],
        "lifecycle_movement_approved": dimensions["lifecycle_movement"]["approved"],
        "promotion_approved": dimensions["promotion"]["approved"],
        "reason": reason,
        "approval_dimensions": dimensions,
        "external_mutation": {
            "approved": dimensions["external_mutation"]["approved"],
            "required": dimensions["external_mutation"]["required"],
            "distinct_from_quality_approval": True,
            "effect": "not_performed_by_content_agent_2_4b",
        },
        "state_effects": {
            "package_status": "unchanged",
            "external_mutation": "not_performed",
            "lifecycle_movement": "not_performed",
            "promotion": "not_performed",
        },
    }
    if run_record_path:
        decision["run_record_path"] = run_record_path
    return decision


def assert_review_gate_decidable(data: dict[str, Any], outcome: str) -> None:
    if data.get("kind") != "review_gate":
        raise ValueError("Target artifact is not a review_gate.")
    approval = data.get("approval") if isinstance(data.get("approval"), dict) else {}
    allowed = approval.get("allowed_decisions", [])
    if outcome not in allowed:
        raise ValueError(f"Gate does not allow decision '{outcome}'.")
    if data.get("status") != "pending":
        raise ValueError(f"Gate is not pending; current status is {data.get('status')!r}.")
    if data.get("decision") is not None:
        raise ValueError("Gate already has a decision record.")


def run_mode_for_gate(data: dict[str, Any]) -> str:
    run = data.get("run") if isinstance(data.get("run"), dict) else {}
    run_record_path = run.get("run_record_path")
    if isinstance(run_record_path, str):
        try:
            run_record = load_mapping(repo_path_from_artifact_value(run_record_path, "review_gate.run.run_record_path"))
        except Exception:
            run_record = {}
        mode = run_record.get("run_mode")
        if mode in VALID_RUN_MODES:
            return str(mode)
    return "governed_continuous"


def build_decision_run_record(
    gate_path: Path,
    gate_before_hash: dict[str, Any],
    data: dict[str, Any],
    decision: dict[str, Any],
    run_record_path: Path,
    *,
    terminal_status: str,
) -> dict[str, Any]:
    gate_relpath = repo_relpath(gate_path)
    run_record_relpath = repo_relpath(run_record_path)
    package = data.get("package") if isinstance(data.get("package"), dict) else {}
    workflow = data.get("workflow") if isinstance(data.get("workflow"), dict) else {}
    run = data.get("run") if isinstance(data.get("run"), dict) else {}
    resolved_run_relpath = run.get("resolved_run_path")
    parent_run_record_relpath = run.get("run_record_path")
    if not isinstance(resolved_run_relpath, str):
        raise ValueError("review_gate.run.resolved_run_path must be present before recording a decision.")
    if not isinstance(parent_run_record_relpath, str):
        raise ValueError("review_gate.run.run_record_path must be present before recording a decision.")

    context_admission = []
    status_path = package.get("status_path")
    if isinstance(status_path, str):
        context_admission.append(artifact_ref("package_status", [status_path], hashes_required=True))
    contract_path = workflow.get("contract_path")
    if isinstance(contract_path, str):
        context_admission.append(artifact_ref("workflow_contract", [contract_path], hashes_required=True))

    consumed_artifacts = [
        artifact_ref(
            "review_gate_before_decision",
            [gate_relpath],
            hashes_required=True,
            precomputed_hashes={gate_relpath: gate_before_hash},
        ),
        artifact_ref("parent_run_record", [parent_run_record_relpath], hashes_required=True),
        artifact_ref("resolved_run", [resolved_run_relpath], hashes_required=True),
    ]
    gate_contract = str(data.get("gate_contract") or data.get("gate_id") or "review_gate")
    gate_id = str(data.get("gate_id") or gate_contract)
    external_approved = decision.get("external_mutation_approved") is True

    return {
        "kind": "run_record",
        "schema_version": CONTENT_AGENT_VERSION,
        "run_id": run_record_path.stem,
        "resolved_run_path": resolved_run_relpath,
        "package": deepcopy(package),
        "workflow": deepcopy(workflow),
        "run_mode": run_mode_for_gate(data),
        "timestamps": {
            "started_at": decision["decided_at"],
            "ended_at": decision["decided_at"],
        },
        "invocation": {
            "entrypoint": "content-agent review",
            "command": f"./content-agent review {decision['outcome']} --gate {gate_id}",
        },
        "context_admission": context_admission,
        "consumed_artifacts": consumed_artifacts,
        "parent_artifacts": [
            {"id": "review_gate", "path": gate_relpath},
            {"id": "parent_run_record", "path": parent_run_record_relpath},
            {"id": "resolved_run", "path": resolved_run_relpath},
        ],
        "produced_artifacts": [
            {"id": "run_record", "paths": [run_record_relpath]},
            {"id": "review_gate_decision", "paths": [gate_relpath]},
        ],
        "validation_results": [
            {
                "id": "content_agent_review_decision",
                "status": "passed",
                "summary": f"Recorded {decision['outcome']} decision without lifecycle, promotion, or external mutation side effects.",
            }
        ],
        "enforcement_outcomes": [
            {
                "surface": "review_gates",
                "posture": "deny",
                "status": f"{decision['outcome']}_recorded",
            },
            {
                "surface": "external_mutation",
                "posture": "deny",
                "status": "approved_not_performed" if external_approved else "not_approved",
            },
            {
                "surface": "lifecycle_movement",
                "posture": "deny",
                "status": "approved_not_moved" if decision.get("lifecycle_movement_approved") is True else "not_approved",
            },
            {
                "surface": "promotion",
                "posture": "deny",
                "status": "approved_not_promoted" if decision.get("promotion_approved") is True else "not_approved",
            },
            {
                "surface": "trace_completeness",
                "posture": "detect",
                "status": "recorded",
            },
        ],
        "gate_ids": [gate_contract, gate_id],
        "approval_decisions": [deepcopy(decision)],
        "external_mutations": [
            {
                "target": "none",
                "status": "not_attempted",
                "approval_reference": f"{gate_id}#decision" if external_approved else None,
            }
        ],
        "terminal_status": terminal_status,
        "promoted_output_state": deepcopy(data.get("promoted_output_state", {})),
    }


def build_decision_run_record_path(data: dict[str, Any], outcome: str, decided_at: str) -> Path:
    package_key = gate_package_key(data) or "no-package"
    gate_id = str(data.get("gate_id") or data.get("gate_contract") or "review-gate")
    stem = (
        f"run-{filename_timestamp(decided_at)}-"
        f"{slugify(package_key)}-review-{outcome}-{slugify(gate_id)}"
    )
    return unique_yaml_path(RUN_RECORDS_DIR, stem)


def build_review_decision_report(
    identifier: str,
    outcome: str,
    *,
    reason: str | None = None,
    decided_by: str | None = None,
) -> dict[str, Any]:
    path = resolve_review_gate_path(identifier)
    data = load_mapping(path)
    assert_review_gate_decidable(data, outcome)
    decided_at = utc_timestamp()
    actor = decided_by or f"content-agent review {outcome}"
    decision_reason = reason or f"{outcome} recorded by content-agent review {outcome}."

    if outcome == "defer":
        decision = build_decision_record(
            data,
            outcome,
            decided_at=decided_at,
            decided_by=actor,
            reason=decision_reason,
        )
        return {
            "kind": "content_agent_review_decision",
            "schema_version": CONTENT_AGENT_VERSION,
            "mutating": False,
            "gate": summarize_review_gate(path, data),
            "status_before": data.get("status"),
            "status_after": data.get("status"),
            "decision": decision,
            "run_record": None,
            "message": "defer is non-mutating; gate remains pending",
        }

    terminal_status = "completed" if outcome == "approve" else "rejected"
    run_record_path = build_decision_run_record_path(data, outcome, decided_at)
    run_record_relpath = repo_relpath(run_record_path)
    decision = build_decision_record(
        data,
        outcome,
        decided_at=decided_at,
        decided_by=actor,
        reason=decision_reason,
        run_record_path=run_record_relpath,
    )
    gate_before_hash = hash_path(path)
    updated_data = deepcopy(data)
    updated_data["status"] = "resolved"
    updated_data["decision"] = decision
    run_record = build_decision_run_record(
        path,
        gate_before_hash,
        data,
        decision,
        run_record_path,
        terminal_status=terminal_status,
    )

    write_yaml_mapping(run_record_path, run_record)
    write_yaml_mapping(path, updated_data)

    return {
        "kind": "content_agent_review_decision",
        "schema_version": CONTENT_AGENT_VERSION,
        "mutating": True,
        "gate": summarize_review_gate(path, updated_data),
        "status_before": data.get("status"),
        "status_after": updated_data.get("status"),
        "decision": decision,
        "run_record": summarize_run_record(run_record_path, run_record),
        "message": f"{outcome} decision recorded",
    }


def prefixed_sha256(path: Path) -> str:
    return "sha256:" + hash_path(path)["sha256"]


def rendered_repo_relpath(value: str, placeholders: dict[str, Any], package_path: Path) -> str:
    rendered = substitute_placeholders(value, placeholders)
    candidate = package_relative_or_repo_path(rendered, package_path)
    try:
        return repo_relpath(candidate)
    except ValueError:
        return rendered


def render_patterns(values: Any, placeholders: dict[str, Any]) -> list[str]:
    if not isinstance(values, list):
        return []
    return [
        substitute_placeholders(item, placeholders)
        for item in values
        if isinstance(item, str)
    ]


def render_contract_command(command: str, placeholders: dict[str, Any]) -> str:
    rendered = substitute_placeholders(command, placeholders)
    package_key = placeholders.get("package")
    if package_key is not None:
        rendered = rendered.replace("{package_key}", str(package_key))
    return rendered


def workflow_ref_payload(
    workflow_id: str,
    contract_path: Path,
    contract: dict[str, Any],
    *,
    step_id: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "workflow_id": workflow_id,
        "workflow_version": contract.get("version", CONTENT_AGENT_VERSION),
        "workflow_hash": prefixed_sha256(contract_path),
        "contract_path": repo_relpath(contract_path),
    }
    if step_id:
        payload["step_id"] = step_id
    return payload


def package_ref_payload(manifest_ref: Any) -> dict[str, Any]:
    return {
        "path": repo_relpath(manifest_ref.package_path),
        "status_path": repo_relpath(manifest_ref.status_path),
        "status_hash": prefixed_sha256(manifest_ref.status_path),
    }


def resolve_pipeline_profile_name(package_arg: str) -> str | None:
    try:
        next_payload = build_next_action(package_arg)
    except Exception:
        return None
    profile = next_payload.get("pipeline_profile")
    return str(profile) if profile else None


def build_run_id(workflow_id: str, package_key: str, timestamp: str, supplied_run_id: str | None = None) -> str:
    if supplied_run_id:
        if not re.fullmatch(r"[A-Za-z0-9_.:-]+", supplied_run_id):
            raise ValueError("run id may only contain letters, digits, underscores, dots, colons, and hyphens.")
        return supplied_run_id
    return f"run-{filename_timestamp(timestamp)}-{slugify(package_key)}-{slugify(workflow_id)}"


def planned_gate_path(run_id: str, gate_id: str) -> str:
    return f"reviewable-runs/gates/gate-{slugify(run_id)}-{slugify(gate_id)}.yaml"


def build_policy_resolution(contract: dict[str, Any], placeholders: dict[str, Any]) -> dict[str, Any]:
    tools = contract.get("capabilities", {}).get("tools", [])
    allowed_tools = []
    if isinstance(tools, list):
        for tool in tools:
            if not isinstance(tool, dict):
                continue
            command = tool.get("command")
            if not isinstance(command, str):
                continue
            allowed_tools.append({
                "id": tool.get("id"),
                "command": render_contract_command(command, placeholders),
                "required": tool.get("required") is True,
            })
    allowed_paths = contract.get("allowed_paths", {})
    if not isinstance(allowed_paths, dict):
        allowed_paths = {}
    return {
        "allowed_tools": allowed_tools,
        "allowed_capabilities": [
            "contract_validation",
            "context_admission",
            "scriptable_step_execution",
            "gate_stop",
            "run_record_writing",
        ],
        "allowed_paths": {
            "read": render_patterns(allowed_paths.get("read"), placeholders),
            "write": render_patterns(allowed_paths.get("write"), placeholders),
        },
    }


def selected_steps_from_contract(contract: dict[str, Any]) -> list[dict[str, Any]]:
    steps = []
    for step in contract.get("steps", []):
        if not isinstance(step, dict):
            continue
        item: dict[str, Any] = {
            "id": step.get("id"),
            "mode": step.get("mode"),
        }
        gate = step.get("gate")
        if isinstance(gate, dict) and gate.get("id"):
            item["gate_id"] = gate.get("id")
        if isinstance(step.get("executor"), dict) and step["executor"].get("command"):
            item["executor"] = "command"
        steps.append(item)
    return steps


def selected_gates_from_contract(contract: dict[str, Any], gate_contracts: dict[str, Any]) -> list[dict[str, Any]]:
    gates = []
    for gate in contract.get("gates", []):
        if not isinstance(gate, dict):
            continue
        contract_id = gate.get("contract")
        gate_contract = gate_contracts.get(contract_id, {}) if isinstance(gate_contracts, dict) else {}
        gates.append({
            "id": gate.get("id"),
            "contract": contract_id,
            "type": gate_contract.get("gate_type") or gate.get("type"),
            "required": gate.get("required"),
            "status": "declared",
        })
    return gates


def output_targets_from_contract(
    contract: dict[str, Any],
    placeholders: dict[str, Any],
    package_path: Path,
    run_id: str,
) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = [
        {
            "id": "resolved_run",
            "path": f"reviewable-runs/resolved-runs/{run_id}.yaml",
        },
        {
            "id": "run_record",
            "path": f"reviewable-runs/logs/{run_id}.yaml",
        },
    ]
    for output in contract.get("outputs", []):
        if not isinstance(output, dict):
            continue
        template = output.get("path_template")
        if not isinstance(template, str):
            continue
        targets.append({
            "id": output.get("id"),
            "path": rendered_repo_relpath(template, placeholders, package_path),
            "required": output.get("required"),
            "format": output.get("format"),
        })
    for gate in contract.get("gates", []):
        if not isinstance(gate, dict) or not gate.get("id"):
            continue
        targets.append({
            "id": f"review_gate:{gate['id']}",
            "path": planned_gate_path(run_id, str(gate["id"])),
            "required": gate.get("required"),
        })
    return targets


def resolved_run_persistence_reasons(contract: dict[str, Any], run_mode: str) -> list[str]:
    reasons: list[str] = []
    trace = contract.get("trace", {}) if isinstance(contract.get("trace"), dict) else {}
    resolved_run = trace.get("resolved_run", {}) if isinstance(trace.get("resolved_run"), dict) else {}
    persist_when = resolved_run.get("persist_when", [])
    persist_set = set(item for item in persist_when if isinstance(item, str))
    if run_mode == "governed_continuous" and "governed" in persist_set:
        reasons.append("governed")
    if run_mode == "governed_continuous" and "continuous" in persist_set:
        reasons.append("continuous")
    if contract.get("gates") and "gated" in persist_set:
        reasons.append("gated")
    recovery = contract.get("behavior", {}).get("recovery", {}) if isinstance(contract.get("behavior"), dict) else {}
    if isinstance(recovery, dict) and recovery.get("resume_from") == "resolved_run" and "resumable" in persist_set:
        reasons.append("resumable")
    if trace.get("run_record") == "required" and "audit_relevant" in persist_set:
        reasons.append("audit_relevant")
    return sorted(set(reasons))


def assert_validation_success(report: dict[str, Any], context: str) -> None:
    if report.get("success") is True:
        return
    errors = [
        str(item.get("message"))
        for item in report.get("findings", [])
        if isinstance(item, dict) and item.get("severity") == "error"
    ]
    detail = "; ".join(errors[:3]) if errors else "validation failed"
    raise ValueError(f"{context}: {detail}")


def build_resolved_run_payload(
    workflow_id: str,
    package_arg: str,
    *,
    run_mode: str,
    runtime_inputs: dict[str, str] | None = None,
    supplied_run_id: str | None = None,
) -> tuple[dict[str, Any], Path, list[str]]:
    runtime_inputs = runtime_inputs or {}
    contracts = load_workflow_yaml_contracts()
    if workflow_id not in contracts:
        raise KeyError(f"Unknown workflow '{workflow_id}'.")
    loaded = contracts[workflow_id]
    contract_path = loaded["path"]
    contract = loaded["data"]
    manifest_ref, status_data = load_status_ref(package_arg)
    package_key = manifest_ref.package_key
    placeholders = build_runtime_placeholders(package_key, status_data, runtime_inputs)
    timestamp = utc_timestamp()
    run_id = build_run_id(workflow_id, package_key, timestamp, supplied_run_id)
    placeholders["run_id"] = run_id
    run_path = RESOLVED_RUNS_DIR / f"{run_id}.yaml"
    if run_path.exists():
        raise FileExistsError(f"Resolved run already exists: {repo_relpath(run_path)}")

    validation_report = build_validation_report(
        workflow_id=workflow_id,
        package_arg=package_key,
        mode=run_mode,
        runtime_inputs=runtime_inputs,
    )
    assert_validation_success(validation_report, "cannot create resolved run")

    gate_contracts = load_gate_contracts()
    policy = load_harness_policy()
    route = {
        "package_kind": status_data.get("kind", "leaf"),
        "pipeline_profile": resolve_pipeline_profile_name(package_key),
        "current_stage": current_stage(status_data),
        "workflow_stage": workflow_id if contract.get("workflow_kind") == "stage" else None,
        "resolved_from": [
            repo_relpath(manifest_ref.status_path),
            repo_relpath(contract_path),
            "harness_policy.yaml",
            "gate_contracts.yaml",
            "pipeline_profiles.yaml",
        ],
    }
    payload = {
        "kind": "resolved_run",
        "schema_version": CONTENT_AGENT_VERSION,
        "run_id": run_id,
        "package": package_ref_payload(manifest_ref),
        "workflow": workflow_ref_payload(workflow_id, contract_path, contract),
        "run_mode": run_mode,
        "runtime_inputs": deepcopy(runtime_inputs),
        "route": route,
        "context_admission": validate_context_admission(
            workflow_id,
            contract_path,
            contract,
            package_key,
            manifest_ref.package_path,
            status_data,
            runtime_inputs,
            run_mode,
            [],
        ),
        "policy_resolution": build_policy_resolution(contract, placeholders),
        "selected_steps": selected_steps_from_contract(contract),
        "selected_gates": selected_gates_from_contract(gate_contracts=gate_contracts, contract=contract),
        "behavior": {
            "budgets": deepcopy(contract.get("behavior", {}).get("budgets", {}))
            if isinstance(contract.get("behavior"), dict)
            else {},
            "recovery": deepcopy(contract.get("behavior", {}).get("recovery", {}))
            if isinstance(contract.get("behavior"), dict)
            else {},
            "policy_run_modes": policy.get("governed_execution", {}).get("run_modes", []),
        },
        "output_targets": output_targets_from_contract(contract, placeholders, manifest_ref.package_path, run_id),
    }
    return payload, run_path, resolved_run_persistence_reasons(contract, run_mode)


def build_run_resolve_report(
    workflow_id: str,
    package_arg: str,
    *,
    run_mode: str,
    runtime_inputs: dict[str, str] | None = None,
    supplied_run_id: str | None = None,
) -> dict[str, Any]:
    payload, run_path, persistence_reasons = build_resolved_run_payload(
        workflow_id,
        package_arg,
        run_mode=run_mode,
        runtime_inputs=runtime_inputs,
        supplied_run_id=supplied_run_id,
    )
    persisted = bool(persistence_reasons)
    if persisted:
        write_yaml_mapping(run_path, payload)
        validation_report = build_validation_report(
            workflow_id=workflow_id,
            package_arg=payload["package"]["path"],
            mode=run_mode,
            runtime_inputs=runtime_inputs,
        )
        assert_validation_success(validation_report, "resolved run validation failed after write")
    return {
        "kind": "content_agent_run_resolution",
        "schema_version": CONTENT_AGENT_VERSION,
        "workflow_id": workflow_id,
        "package": gate_package_key(payload),
        "run_id": payload["run_id"],
        "run_mode": run_mode,
        "persisted": persisted,
        "persistence_reasons": persistence_reasons,
        "resolved_run_path": repo_relpath(run_path) if persisted else None,
        "resolved_run": payload,
        "message": "resolved run persisted" if persisted else "resolved run is transient",
    }


def resolve_step_start_index(steps: list[Any], start_at: str | None) -> int:
    if not start_at:
        return 0
    for index, step in enumerate(steps):
        if isinstance(step, dict) and step.get("id") == start_at:
            return index
    raise ValueError(f"Unknown workflow step: {start_at}")


def rendered_step_command(step: dict[str, Any], placeholders: dict[str, Any]) -> str | None:
    executor = step.get("executor")
    if not isinstance(executor, dict):
        return None
    command = executor.get("command")
    if not isinstance(command, str) or not command:
        return None
    return render_contract_command(command, placeholders)


def declared_rendered_commands(contract: dict[str, Any], placeholders: dict[str, Any]) -> set[str]:
    commands = set()
    tools = contract.get("capabilities", {}).get("tools", [])
    if not isinstance(tools, list):
        return commands
    for tool in tools:
        if not isinstance(tool, dict) or not isinstance(tool.get("command"), str):
            continue
        commands.add(normalize_command(render_contract_command(tool["command"], placeholders)))
    return commands


def output_excerpt(stdout: str, stderr: str, limit: int = 6000) -> str:
    combined = stdout + stderr
    if len(combined) <= limit:
        return combined
    return combined[-limit:]


def run_scriptable_command(command: str) -> dict[str, Any]:
    proc = subprocess.run(
        command,
        shell=True,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    return {
        "command": command,
        "returncode": proc.returncode,
        "status": "passed" if proc.returncode == 0 else "failed",
        "output_excerpt": output_excerpt(proc.stdout, proc.stderr),
        "output_truncated": len(proc.stdout + proc.stderr) > 6000,
    }


def gate_entry_for_step(contract: dict[str, Any], step: dict[str, Any]) -> dict[str, Any] | None:
    gate_ref = step.get("gate")
    gate_id = gate_ref.get("id") if isinstance(gate_ref, dict) else None
    if not gate_id:
        return None
    for gate in contract.get("gates", []):
        if isinstance(gate, dict) and gate.get("id") == gate_id:
            return gate
    return {"id": gate_id}


def output_target_paths_by_id(resolved_run: dict[str, Any]) -> dict[str, str]:
    paths: dict[str, str] = {}
    for target in resolved_run.get("output_targets", []):
        if not isinstance(target, dict):
            continue
        target_id = target.get("id")
        target_path = target.get("path")
        if isinstance(target_id, str) and isinstance(target_path, str):
            paths[target_id] = target_path
    return paths


def existing_output_artifact_refs(
    resolved_run: dict[str, Any],
    *,
    only_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for target in resolved_run.get("output_targets", []):
        if not isinstance(target, dict):
            continue
        target_id = target.get("id")
        target_path = target.get("path")
        if not isinstance(target_id, str) or not isinstance(target_path, str):
            continue
        if target_id in {"resolved_run", "run_record"} or target_id.startswith("review_gate:"):
            continue
        if only_ids is not None and target_id not in only_ids:
            continue
        try:
            candidate = repo_path_from_artifact_value(target_path, f"output_targets.{target_id}.path")
        except ValueError:
            continue
        if candidate.exists():
            refs.append({"id": target_id, "paths": [target_path]})
    return refs


def executed_step_output_ids(resolved_run: dict[str, Any], command_results: list[dict[str, Any]]) -> set[str]:
    passed_step_ids = {
        str(result.get("step_id"))
        for result in command_results
        if result.get("status") == "passed" and result.get("step_id")
    }
    if not passed_step_ids:
        return set()
    contract_path = repo_path_from_artifact_value(
        resolved_run["workflow"]["contract_path"],
        "resolved_run.workflow.contract_path",
    )
    contract = load_mapping(contract_path)
    output_ids: set[str] = set()
    for step in contract.get("steps", []):
        if not isinstance(step, dict) or step.get("id") not in passed_step_ids:
            continue
        produces = step.get("produces", [])
        if not isinstance(produces, list):
            continue
        output_ids.update(item for item in produces if isinstance(item, str))
    return output_ids


def unique_paths(paths: list[str]) -> list[str]:
    seen: set[str] = set()
    unique: list[str] = []
    for path in paths:
        if path in seen:
            continue
        seen.add(path)
        unique.append(path)
    return unique


def gate_preview_paths(gate_entry: dict[str, Any], resolved_run: dict[str, Any]) -> list[str]:
    paths_by_id = output_target_paths_by_id(resolved_run)
    paths = []
    artifacts = gate_entry.get("artifacts", [])
    if not isinstance(artifacts, list):
        return paths
    for artifact_id in artifacts:
        if not isinstance(artifact_id, str):
            continue
        clean_id = artifact_id.split()[0]
        relpath = paths_by_id.get(clean_id)
        if not relpath:
            continue
        if (REPO_ROOT / relpath).exists():
            paths.append(relpath)
    return paths


def default_promoted_output_state(validation_state: str = "passed") -> dict[str, str]:
    return {
        "authority_order": "workflow_contract_first",
        "claim_state": "unchanged",
        "contradiction_state": "none_known",
        "validation_state": validation_state,
        "trace_state": "minimum_complete",
    }


def validation_results_from_execution(command_results: list[dict[str, Any]], preflight_status: str = "passed") -> list[dict[str, Any]]:
    results = [
        {
            "id": "content_agent_validate",
            "status": preflight_status,
            "command": "./content-agent validate",
        }
    ]
    for result in command_results:
        item = {
            "id": f"scriptable_step:{result.get('step_id')}",
            "status": result.get("status"),
            "command": result.get("command"),
        }
        if result.get("returncode") is not None:
            item["returncode"] = result.get("returncode")
        results.append(item)
    return results


def enforcement_outcomes_for_execution(terminal_status: str, gate_written: bool) -> list[dict[str, Any]]:
    return [
        {
            "surface": "contract_shape",
            "posture": "deny",
            "status": "passed",
        },
        {
            "surface": "context_admission",
            "posture": "deny",
            "status": "passed",
        },
        {
            "surface": "tool_use",
            "posture": "deny",
            "status": "passed" if terminal_status != "failed" else "failed",
        },
        {
            "surface": "path_access",
            "posture": "deny",
            "status": "passed",
        },
        {
            "surface": "review_gates",
            "posture": "deny",
            "status": "gate_recorded" if gate_written else "not_reached",
        },
        {
            "surface": "external_mutation",
            "posture": "deny",
            "status": "not_attempted",
        },
        {
            "surface": "lifecycle_movement",
            "posture": "deny",
            "status": "not_attempted",
        },
        {
            "surface": "promotion",
            "posture": "deny",
            "status": "not_attempted",
        },
        {
            "surface": "trace_completeness",
            "posture": "detect",
            "status": "recorded",
        },
    ]


def approval_requirements_from_gate_contract(gate_contract: dict[str, Any]) -> dict[str, Any]:
    dimensions = gate_contract.get("approval_dimensions", {}) if isinstance(gate_contract, dict) else {}
    return {
        "quality_required": dimensions.get("quality") is True,
        "external_mutation_required": dimensions.get("external_mutation") is True,
        "lifecycle_movement_required": dimensions.get("lifecycle_movement") is True,
        "promotion_required": dimensions.get("promotion") is True,
        "allowed_decisions": ["approve", "reject", "defer"],
    }


def build_review_gate_from_run(
    resolved_run: dict[str, Any],
    resolved_run_path: Path,
    run_record_path: Path,
    contract: dict[str, Any],
    step: dict[str, Any],
    gate_entry: dict[str, Any],
    validation_results: list[dict[str, Any]],
    enforcement_outcomes: list[dict[str, Any]],
    timestamp: str,
) -> tuple[dict[str, Any], Path]:
    gate_contracts = load_gate_contracts()
    contract_id = gate_entry.get("contract") or gate_entry.get("id")
    gate_contract = gate_contracts.get(contract_id, {}) if isinstance(contract_id, str) else {}
    gate_id = f"{contract_id}-{filename_timestamp(timestamp)}"
    planned_path = output_target_paths_by_id(resolved_run).get(f"review_gate:{gate_entry.get('id')}")
    gate_path = (REPO_ROOT / planned_path).resolve() if planned_path else REVIEW_GATES_DIR / f"gate-{slugify(resolved_run['run_id'])}-{slugify(str(gate_entry.get('id')))}.yaml"
    if gate_path.exists():
        gate_path = unique_yaml_path(REVIEW_GATES_DIR, f"gate-{slugify(resolved_run['run_id'])}-{slugify(str(gate_entry.get('id')))}")
    gate_type = gate_contract.get("gate_type") or gate_entry.get("type")
    preview_paths = gate_preview_paths(gate_entry, resolved_run)
    evidence_paths = unique_paths([
        repo_relpath(resolved_run_path),
        repo_relpath(run_record_path),
        *preview_paths,
    ])
    artifact = {
        "kind": "review_gate",
        "schema_version": CONTENT_AGENT_VERSION,
        "gate_id": gate_id,
        "status": "pending",
        "gate_type": gate_type,
        "gate_contract": contract_id,
        "package": deepcopy(resolved_run["package"]),
        "workflow": {
            **deepcopy(resolved_run["workflow"]),
            "step_id": step.get("id"),
        },
        "run": {
            "run_id": resolved_run["run_id"],
            "resolved_run_path": repo_relpath(resolved_run_path),
            "run_record_path": repo_relpath(run_record_path),
        },
        "stop": {
            "reason": f"Reached review gate '{gate_entry.get('id')}' before governed progress could continue.",
            "created_at": timestamp,
            "created_by": "content-agent run",
        },
        "evidence": {
            "preview_paths": preview_paths,
            "evidence_paths": evidence_paths,
            "validation_results": validation_results,
            "enforcement_outcomes": enforcement_outcomes,
        },
        "approval": approval_requirements_from_gate_contract(gate_contract),
        "resume": {
            "on_approve": "content-agent resume --gate " + gate_id,
            "on_reject": "route_to_correction_or_stop",
            "on_defer": "keep_pending",
            "command_hint": "content-agent resume --gate " + gate_id,
        },
        "promoted_output_state": default_promoted_output_state("blocked"),
        "decision": None,
    }
    return artifact, gate_path


def context_artifact_refs(resolved_run: dict[str, Any]) -> list[dict[str, Any]]:
    refs = []
    for entry in resolved_run.get("context_admission", []):
        if not isinstance(entry, dict):
            continue
        paths = entry.get("paths", [])
        if not isinstance(paths, list) or not paths:
            continue
        refs.append(artifact_ref(
            f"context:{entry.get('id')}",
            [path for path in paths if isinstance(path, str)],
            hashes_required=True,
            precomputed_hashes=entry.get("hashes") if isinstance(entry.get("hashes"), dict) else None,
        ))
    return refs


def build_execution_run_record(
    resolved_run: dict[str, Any],
    resolved_run_path: Path,
    run_record_path: Path,
    *,
    terminal_status: str,
    started_at: str,
    ended_at: str,
    command_results: list[dict[str, Any]],
    gate_artifact_path: Path | None,
    gate_artifact: dict[str, Any] | None,
    stop_reason: str,
) -> dict[str, Any]:
    resolved_run_relpath = repo_relpath(resolved_run_path)
    run_record_relpath = repo_relpath(run_record_path)
    validation_state = "passed" if terminal_status in {"completed", "gated", "deferred"} else "failed"
    validation_results = validation_results_from_execution(command_results)
    gate_ids = []
    if gate_artifact:
        gate_ids = [
            str(gate_artifact.get("gate_contract")),
            str(gate_artifact.get("gate_id")),
        ]
    produced_artifacts = [
        {"id": "resolved_run", "paths": [resolved_run_relpath]},
        {"id": "run_record", "paths": [run_record_relpath]},
    ]
    produced_artifacts.extend(
        existing_output_artifact_refs(
            resolved_run,
            only_ids=executed_step_output_ids(resolved_run, command_results),
        )
    )
    if gate_artifact_path:
        produced_artifacts.append({"id": "review_gate", "paths": [repo_relpath(gate_artifact_path)]})
    runtime_inputs = resolved_run.get("runtime_inputs")
    if not isinstance(runtime_inputs, dict):
        runtime_inputs = {}
    invocation_parts = [
        "./content-agent",
        "run",
        "--workflow",
        str(resolved_run["workflow"]["workflow_id"]),
        "--package",
        str(gate_package_key(resolved_run) or resolved_run["package"]["path"]),
    ]
    if resolved_run["run_mode"] != "governed_continuous":
        invocation_parts.extend(["--mode", str(resolved_run["run_mode"])])
    for key in sorted(runtime_inputs):
        invocation_parts.extend(["--input", f"{key}={runtime_inputs[key]}"])
    execution_options = resolved_run.get("execution_options")
    if not isinstance(execution_options, dict):
        execution_options = {}
    if execution_options.get("start_at"):
        invocation_parts.extend(["--start-at", str(execution_options["start_at"])])
    if execution_options.get("max_scriptable_steps") is not None:
        invocation_parts.extend(["--max-scriptable-steps", str(execution_options["max_scriptable_steps"])])
    return {
        "kind": "run_record",
        "schema_version": CONTENT_AGENT_VERSION,
        "run_id": resolved_run["run_id"],
        "resolved_run_path": resolved_run_relpath,
        "package": deepcopy(resolved_run["package"]),
        "workflow": deepcopy(resolved_run["workflow"]),
        "run_mode": resolved_run["run_mode"],
        "timestamps": {
            "started_at": started_at,
            "ended_at": ended_at,
        },
        "invocation": {
            "entrypoint": "content-agent run",
            "command": " ".join(shlex.quote(part) for part in invocation_parts),
        },
        "context_admission": deepcopy(resolved_run.get("context_admission", [])),
        "consumed_artifacts": [
            artifact_ref("resolved_run", [resolved_run_relpath], hashes_required=True),
            *context_artifact_refs(resolved_run),
        ],
        "parent_artifacts": [
            {"id": "resolved_run", "path": resolved_run_relpath},
            {"id": "package_status", "path": resolved_run["package"]["status_path"]},
        ],
        "produced_artifacts": produced_artifacts,
        "validation_results": validation_results,
        "enforcement_outcomes": enforcement_outcomes_for_execution(terminal_status, gate_artifact is not None),
        "gate_ids": gate_ids,
        "approval_decisions": [],
        "external_mutations": [
            {
                "target": "none",
                "status": "not_attempted",
                "approval_reference": None,
            }
        ],
        "terminal_status": terminal_status,
        "promoted_output_state": default_promoted_output_state(validation_state),
        "execution": {
            "stop_reason": stop_reason,
            "scriptable_steps": command_results,
        },
    }


def execute_resolved_run(
    resolved_run: dict[str, Any],
    resolved_run_path: Path,
    *,
    start_at: str | None = None,
    max_scriptable_steps: int | None = None,
) -> dict[str, Any]:
    workflow_id = resolved_run["workflow"]["workflow_id"]
    contract_path = repo_path_from_artifact_value(resolved_run["workflow"]["contract_path"], "resolved_run.workflow.contract_path")
    contract = load_mapping(contract_path)
    package_key = gate_package_key(resolved_run)
    if not package_key:
        raise ValueError("Resolved run package path does not map to a package key.")
    manifest_ref, status_data = load_status_ref(package_key)
    runtime_inputs = resolved_run.get("runtime_inputs")
    if not isinstance(runtime_inputs, dict):
        runtime_inputs = {}
    placeholders = build_runtime_placeholders(package_key, status_data, runtime_inputs)
    declared_commands = declared_rendered_commands(contract, placeholders)
    steps = contract.get("steps", [])
    if not isinstance(steps, list):
        raise ValueError("workflow steps must be a list.")

    started_at = utc_timestamp()
    command_results: list[dict[str, Any]] = []
    scriptable_count = 0
    terminal_status = "completed"
    stop_reason = "workflow completed"
    gate_artifact = None
    gate_artifact_path = None
    run_record_path = RUN_RECORDS_DIR / f"{resolved_run['run_id']}.yaml"
    if run_record_path.exists():
        raise FileExistsError(f"Run record already exists: {repo_relpath(run_record_path)}")

    start_index = resolve_step_start_index(steps, start_at)
    for step in steps[start_index:]:
        if not isinstance(step, dict):
            continue
        step_id = str(step.get("id") or "unknown")
        mode = step.get("mode")
        if mode == "review_gated" or gate_entry_for_step(contract, step):
            terminal_status = "gated"
            stop_reason = f"stopped at review gate step: {step_id}"
            validation_results = validation_results_from_execution(command_results)
            enforcement_outcomes = enforcement_outcomes_for_execution("gated", True)
            gate_artifact, gate_artifact_path = build_review_gate_from_run(
                resolved_run,
                resolved_run_path,
                run_record_path,
                contract,
                step,
                gate_entry_for_step(contract, step) or {"id": step_id},
                validation_results,
                enforcement_outcomes,
                utc_timestamp(),
            )
            break
        if mode != "scriptable":
            terminal_status = "deferred"
            stop_reason = f"deferred before non-scriptable step: {step_id}"
            break
        if max_scriptable_steps is not None and scriptable_count >= max_scriptable_steps:
            terminal_status = "deferred"
            stop_reason = f"scriptable step limit reached before: {step_id}"
            break
        command = rendered_step_command(step, placeholders)
        if not command:
            terminal_status = "deferred"
            stop_reason = f"scriptable step has no runnable command: {step_id}"
            break
        if not command_is_covered(command, declared_commands):
            raise ValueError(f"Scriptable step '{step_id}' uses a command not declared in capabilities.tools.")
        available, reason = command_availability(command, load_package_scripts())
        if not available:
            raise ValueError(f"Scriptable step '{step_id}' command is unavailable: {reason}")
        result = run_scriptable_command(command)
        result["step_id"] = step_id
        command_results.append(result)
        scriptable_count += 1
        if result["status"] != "passed":
            terminal_status = "failed"
            stop_reason = f"scriptable step failed: {step_id}"
            break

    ended_at = utc_timestamp()
    run_record = build_execution_run_record(
        resolved_run,
        resolved_run_path,
        run_record_path,
        terminal_status=terminal_status,
        started_at=started_at,
        ended_at=ended_at,
        command_results=command_results,
        gate_artifact_path=gate_artifact_path,
        gate_artifact=gate_artifact,
        stop_reason=stop_reason,
    )
    if gate_artifact and gate_artifact_path:
        write_yaml_mapping(gate_artifact_path, gate_artifact)
    write_yaml_mapping(run_record_path, run_record)

    validation_report = build_validation_report(
        workflow_id=workflow_id,
        package_arg=package_key,
        mode=resolved_run["run_mode"],
        runtime_inputs=runtime_inputs,
    )
    assert_validation_success(validation_report, "run evidence validation failed after write")
    return {
        "kind": "content_agent_run",
        "schema_version": CONTENT_AGENT_VERSION,
        "workflow_id": workflow_id,
        "package": package_key,
        "run_id": resolved_run["run_id"],
        "terminal_status": terminal_status,
        "stop_reason": stop_reason,
        "resolved_run_path": repo_relpath(resolved_run_path),
        "run_record_path": repo_relpath(run_record_path),
        "review_gate_path": repo_relpath(gate_artifact_path) if gate_artifact_path else None,
        "review_gate_id": gate_artifact.get("gate_id") if gate_artifact else None,
        "scriptable_steps_executed": scriptable_count,
        "command_results": command_results,
    }


def build_run_execution_report(
    workflow_id: str,
    package_arg: str,
    *,
    run_mode: str,
    runtime_inputs: dict[str, str] | None = None,
    supplied_run_id: str | None = None,
    start_at: str | None = None,
    max_scriptable_steps: int | None = None,
) -> dict[str, Any]:
    runtime_inputs = runtime_inputs or {}
    resolved_run, resolved_run_path, persistence_reasons = build_resolved_run_payload(
        workflow_id,
        package_arg,
        run_mode=run_mode,
        runtime_inputs=runtime_inputs,
        supplied_run_id=supplied_run_id,
    )
    if start_at is not None or max_scriptable_steps is not None:
        resolved_run["execution_options"] = {
            "start_at": start_at,
            "max_scriptable_steps": max_scriptable_steps,
        }
    if not persistence_reasons:
        raise ValueError("content-agent run currently requires a persisted resolved_run.")
    write_yaml_mapping(resolved_run_path, resolved_run)
    validation_report = build_validation_report(
        workflow_id=workflow_id,
        package_arg=package_arg,
        mode=run_mode,
        runtime_inputs=runtime_inputs,
    )
    assert_validation_success(validation_report, "resolved run validation failed before execution")
    return execute_resolved_run(
        resolved_run,
        resolved_run_path,
        start_at=start_at,
        max_scriptable_steps=max_scriptable_steps,
    )


def resolve_resolved_run_path(identifier: str) -> Path:
    candidate = Path(identifier).expanduser()
    if candidate.is_absolute() and candidate.exists():
        return candidate.resolve()
    repo_candidate = (REPO_ROOT / candidate).resolve()
    if repo_candidate.exists():
        return repo_candidate
    matches = []
    for path in evidence_yaml_paths(RESOLVED_RUNS_DIR):
        try:
            data = load_mapping(path)
        except Exception:
            continue
        if data.get("kind") != "resolved_run":
            continue
        if identifier in {str(data.get("run_id")), path.name, path.stem}:
            matches.append(path)
    if not matches:
        raise FileNotFoundError(f"No resolved run found for '{identifier}'.")
    if len(matches) > 1:
        raise ValueError(f"Resolved run identifier is ambiguous: {identifier}")
    return matches[0]


def assert_gate_resume_allowed(gate: dict[str, Any]) -> None:
    if gate.get("status") != "resolved":
        raise ValueError(f"Cannot resume gate with status {gate.get('status')!r}; approve the gate first.")
    decision = gate.get("decision")
    if not isinstance(decision, dict):
        raise ValueError("Cannot resume gate without a decision record.")
    if decision.get("outcome") != "approve":
        raise ValueError(f"Cannot resume from decision outcome {decision.get('outcome')!r}.")
    approval = gate.get("approval") if isinstance(gate.get("approval"), dict) else {}
    checks = [
        ("quality_required", "quality_approved"),
        ("external_mutation_required", "external_mutation_approved"),
        ("lifecycle_movement_required", "lifecycle_movement_approved"),
        ("promotion_required", "promotion_approved"),
    ]
    missing = [
        approved_key
        for required_key, approved_key in checks
        if approval.get(required_key) is True and decision.get(approved_key) is not True
    ]
    if missing:
        raise ValueError("Cannot resume; approval dimensions are insufficient: " + ", ".join(missing))


def resume_run_record_path(source_id: str, package_key: str, timestamp: str) -> Path:
    stem = f"run-{filename_timestamp(timestamp)}-{slugify(package_key)}-resume-{slugify(source_id)}"
    return unique_yaml_path(RUN_RECORDS_DIR, stem)


def build_resume_run_record(
    resolved_run: dict[str, Any],
    resolved_run_path: Path,
    run_record_path: Path,
    *,
    timestamp: str,
    gate_path: Path | None = None,
    gate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved_run_relpath = repo_relpath(resolved_run_path)
    run_record_relpath = repo_relpath(run_record_path)
    consumed = [
        artifact_ref("resolved_run", [resolved_run_relpath], hashes_required=True),
        *context_artifact_refs(resolved_run),
    ]
    parent_artifacts = [
        {"id": "resolved_run", "path": resolved_run_relpath},
        {"id": "package_status", "path": resolved_run["package"]["status_path"]},
    ]
    gate_ids: list[str] = []
    approval_decisions: list[dict[str, Any]] = []
    if gate_path and gate:
        gate_relpath = repo_relpath(gate_path)
        consumed.append(artifact_ref("approved_review_gate", [gate_relpath], hashes_required=True))
        parent_artifacts.append({"id": "approved_review_gate", "path": gate_relpath})
        gate_ids = [str(gate.get("gate_contract")), str(gate.get("gate_id"))]
        if isinstance(gate.get("decision"), dict):
            approval_decisions.append(deepcopy(gate["decision"]))
    return {
        "kind": "run_record",
        "schema_version": CONTENT_AGENT_VERSION,
        "run_id": run_record_path.stem,
        "resolved_run_path": resolved_run_relpath,
        "package": deepcopy(resolved_run["package"]),
        "workflow": deepcopy(resolved_run["workflow"]),
        "run_mode": resolved_run["run_mode"],
        "timestamps": {
            "started_at": timestamp,
            "ended_at": timestamp,
        },
        "invocation": {
            "entrypoint": "content-agent resume",
            "command": "./content-agent resume",
        },
        "context_admission": deepcopy(resolved_run.get("context_admission", [])),
        "consumed_artifacts": consumed,
        "parent_artifacts": parent_artifacts,
        "produced_artifacts": [
            {"id": "run_record", "paths": [run_record_relpath]},
        ],
        "validation_results": [
            {
                "id": "content_agent_resume_preflight",
                "status": "passed",
                "summary": "Resume preflight accepted file-backed state without lifecycle, promotion, or external mutation side effects.",
            }
        ],
        "enforcement_outcomes": [
            {
                "surface": "review_gates",
                "posture": "deny",
                "status": "approved" if gate else "not_applicable",
            },
            {
                "surface": "external_mutation",
                "posture": "deny",
                "status": "not_attempted",
            },
            {
                "surface": "lifecycle_movement",
                "posture": "deny",
                "status": "not_moved",
            },
            {
                "surface": "promotion",
                "posture": "deny",
                "status": "not_promoted",
            },
            {
                "surface": "trace_completeness",
                "posture": "detect",
                "status": "recorded",
            },
        ],
        "gate_ids": gate_ids,
        "approval_decisions": approval_decisions,
        "external_mutations": [
            {
                "target": "none",
                "status": "not_attempted",
                "approval_reference": f"{gate.get('gate_id')}#decision" if gate else None,
            }
        ],
        "terminal_status": "deferred",
        "promoted_output_state": default_promoted_output_state("passed"),
        "resume": {
            "source": "review_gate" if gate else "resolved_run",
            "source_path": repo_relpath(gate_path) if gate_path else resolved_run_relpath,
            "effect": "resume_authorized_without_automatic_lifecycle_or_promotion",
        },
    }


def build_resume_report(gate_identifier: str | None = None, resolved_run_identifier: str | None = None) -> dict[str, Any]:
    if bool(gate_identifier) == bool(resolved_run_identifier):
        raise ValueError("resume requires exactly one of --gate or --resolved-run.")
    gate_path = None
    gate = None
    if gate_identifier:
        gate_path = resolve_review_gate_path(gate_identifier)
        gate = load_mapping(gate_path)
        if gate.get("kind") != "review_gate":
            raise ValueError(f"{repo_relpath(gate_path)} is not a review_gate artifact.")
        assert_gate_resume_allowed(gate)
        run_ref = gate.get("run") if isinstance(gate.get("run"), dict) else {}
        resolved_run_value = run_ref.get("resolved_run_path")
        if not isinstance(resolved_run_value, str):
            raise ValueError("Approved gate is missing run.resolved_run_path.")
        resolved_run_path = repo_path_from_artifact_value(resolved_run_value, "review_gate.run.resolved_run_path")
    else:
        resolved_run_path = resolve_resolved_run_path(str(resolved_run_identifier))

    resolved_run = load_mapping(resolved_run_path)
    if resolved_run.get("kind") != "resolved_run":
        raise ValueError(f"{repo_relpath(resolved_run_path)} is not a resolved_run artifact.")
    package_key = gate_package_key(resolved_run)
    workflow_id = resolved_run.get("workflow", {}).get("workflow_id") if isinstance(resolved_run.get("workflow"), dict) else None
    if not package_key or not isinstance(workflow_id, str):
        raise ValueError("Resolved run is missing package or workflow identity.")
    runtime_inputs = resolved_run.get("runtime_inputs")
    if not isinstance(runtime_inputs, dict):
        runtime_inputs = {}
    validation_report = build_validation_report(
        workflow_id=workflow_id,
        package_arg=package_key,
        mode=resolved_run.get("run_mode", "governed_continuous"),
        runtime_inputs=runtime_inputs,
    )
    assert_validation_success(validation_report, "resume validation failed")
    timestamp = utc_timestamp()
    source_id = str(gate.get("gate_id") if gate else resolved_run.get("run_id"))
    run_record_path = resume_run_record_path(source_id, package_key, timestamp)
    run_record = build_resume_run_record(
        resolved_run,
        resolved_run_path,
        run_record_path,
        timestamp=timestamp,
        gate_path=gate_path,
        gate=gate,
    )
    write_yaml_mapping(run_record_path, run_record)
    post_report = build_validation_report(
        workflow_id=workflow_id,
        package_arg=package_key,
        mode=resolved_run.get("run_mode", "governed_continuous"),
        runtime_inputs=runtime_inputs,
    )
    assert_validation_success(post_report, "resume evidence validation failed after write")
    return {
        "kind": "content_agent_resume",
        "schema_version": CONTENT_AGENT_VERSION,
        "source": "review_gate" if gate else "resolved_run",
        "source_path": repo_relpath(gate_path) if gate_path else repo_relpath(resolved_run_path),
        "package": package_key,
        "workflow_id": workflow_id,
        "resolved_run_path": repo_relpath(resolved_run_path),
        "run_record_path": repo_relpath(run_record_path),
        "terminal_status": "deferred",
        "message": "resume authorized and recorded",
    }


def build_next_report(package_arg: str) -> dict[str, Any]:
    payload = build_next_action(package_arg)
    blockers = [gate for gate in load_review_gate_records(package_arg) if gate.get("status") == "pending"]
    payload["kind"] = "content_agent_next"
    payload["schema_version"] = CONTENT_AGENT_VERSION
    payload["pending_review_gate_blockers"] = blockers
    payload["has_pending_review_gate_blockers"] = bool(blockers)
    payload["gate_blocking_policy"] = "pending review gates block governed progress"
    if blockers:
        blocking_issues = payload.setdefault("blocking_issues", [])
        for gate in blockers:
            issue = (
                "Pending review gate blocks governed progress: "
                f"{gate.get('gate_id')} ({gate.get('path')})"
            )
            if issue not in blocking_issues:
                blocking_issues.append(issue)
        payload["can_execute"] = False
        if payload.get("effective_can_execute") is not None:
            payload["effective_can_execute"] = False
        suggested = payload.setdefault("suggested_commands", [])
        for gate in blockers:
            gate_id = gate.get("gate_id")
            if gate_id:
                command = f"content-agent review inspect --gate {gate_id}"
                if command not in suggested:
                    suggested.append(command)
    return payload


def resolve_packet_path(packet_arg: str | None) -> Path | None:
    if not packet_arg:
        return None
    candidate = Path(packet_arg).expanduser()
    if not candidate.is_absolute():
        candidate = (REPO_ROOT / candidate).resolve()
    return candidate


def build_gate_check_report(
    gate_id: str,
    *,
    package_arg: str | None = None,
    packet_arg: str | None = None,
) -> dict[str, Any]:
    packet_path = resolve_packet_path(packet_arg)
    result = evaluate_gate(gate_id, package_arg=package_arg, packet_path=packet_path)
    log_path = log_gate_check(result, package_arg, packet_path)
    return {
        "kind": "content_agent_gate_check",
        "schema_version": CONTENT_AGENT_VERSION,
        "success": not result["blocking"],
        **result,
        "log_path": log_path,
    }


def print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, indent=2, default=str))


def print_text_report(report: dict[str, Any]) -> None:
    status = "passed" if report["success"] else "failed"
    print(f"content-agent validate {status}.")
    print(f"mode: {report['mode']}")
    if report.get("package"):
        print(f"package: {report['package']}")
    print("workflows: " + ", ".join(item["workflow_id"] for item in report["workflows"]))
    evidence = report.get("execution_evidence", {})
    counts = evidence.get("counts", {}) if isinstance(evidence, dict) else {}
    if counts:
        print(
            "execution evidence: "
            + ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
        )
    if not report["findings"]:
        print("findings: none")
        return
    print("findings:")
    for finding in report["findings"]:
        prefix = finding["severity"].upper()
        workflow = f" {finding['workflow_id']}:" if finding.get("workflow_id") else ""
        path = f" ({finding['path']})" if finding.get("path") else ""
        print(
            f"  - [{prefix}] {finding['surface']}[{finding['posture']}]{workflow} "
            f"{finding['message']}{path}"
        )


def print_text_status(report: dict[str, Any]) -> None:
    print("content-agent status")
    package = report.get("package")
    if package:
        print(f"package: {package['package']}")
        print(f"kind: {package['kind']}")
        print(f"revision: {package['revision']}")
        print(f"current_stage: {package.get('current_stage')}")
        if package.get("umbrella_route"):
            route = package["umbrella_route"]
            print(f"umbrella_route: {route.get('active_workflow')} ({route.get('active_route')})")
    else:
        print("package: not supplied")

    root = report.get("root_surfaces", {})
    print(
        "root surfaces: "
        f"workflow_yaml={root.get('workflow_yaml_count', 0)}, "
        f"gate_contracts={root.get('gate_contract_count', 0)}, "
        f"pipeline_profiles={root.get('pipeline_profile_count', 0)}"
    )

    gates = report.get("review_gates", {})
    print(
        "review gates: "
        f"pending={gates.get('pending_count', 0)}, "
        f"resolved={gates.get('resolved_count', 0)}, "
        f"invalid={gates.get('invalid_count', 0)}"
    )
    if gates.get("pending"):
        print("pending gate blockers:")
        for gate in gates["pending"]:
            print(
                "  - "
                f"{gate.get('gate_id')} "
                f"({gate.get('gate_contract')}, {gate.get('workflow_id')}) "
                f"{gate.get('path')}"
            )

    runs = report.get("recent_runs", {})
    yaml_runs = runs.get("yaml_run_records", [])
    legacy_logs = runs.get("legacy_json_logs", [])
    print(f"recent YAML run records: {len(yaml_runs)}")
    for record in yaml_runs:
        print(
            "  - "
            f"{record.get('run_id')} "
            f"{record.get('workflow_id')} "
            f"{record.get('terminal_status')} "
            f"{record.get('path')}"
        )
    print(f"recent legacy JSON logs: {len(legacy_logs)}")
    for record in legacy_logs:
        label = record.get("run_id") or record.get("timestamp") or record.get("path")
        print(
            "  - "
            f"{label} "
            f"{record.get('kind')} "
            f"{record.get('status')} "
            f"{record.get('path')}"
        )

    health = report.get("validation_health", {})
    counts = health.get("severity_counts", {})
    state = "passed" if health.get("success") else "failed"
    print(
        "validation: "
        f"{state} "
        f"(errors={counts.get('error', 0)}, "
        f"warnings={counts.get('warning', 0)}, "
        f"info={counts.get('info', 0)})"
    )
    if health.get("top_findings"):
        print("validation findings:")
        for finding in health["top_findings"]:
            path = f" ({finding.get('path')})" if finding.get("path") else ""
            print(
                "  - "
                f"[{str(finding.get('severity')).upper()}] "
                f"{finding.get('surface')}: {finding.get('message')}{path}"
            )


def print_text_init(report: dict[str, Any]) -> None:
    print("content-agent init")
    print(f"check_only: {str(report.get('check_only') is True).lower()}")
    print("runtime_directories:")
    for record in report.get("runtime_directories", []):
        print(
            "  - "
            f"{record.get('path')}: exists={str(record.get('exists_after') is True).lower()}, "
            f"created={str(record.get('created') is True).lower()}"
        )
    health = report.get("validation_health", {})
    counts = health.get("severity_counts", {})
    state = "passed" if health.get("success") else "failed"
    print(
        "validation: "
        f"{state} "
        f"(errors={counts.get('error', 0)}, "
        f"warnings={counts.get('warning', 0)}, "
        f"info={counts.get('info', 0)})"
    )
    if report.get("message"):
        print(f"message: {report.get('message')}")


def print_text_review_list(report: dict[str, Any]) -> None:
    filters = report.get("filters", {})
    print("content-agent review list")
    print(f"package: {filters.get('package') or 'all'}")
    print(f"status: {filters.get('status')}")
    print(f"include_retained: {filters.get('include_retained')}")
    gates = report.get("gates", [])
    if not gates:
        print("gates: none")
        return
    print("gates:")
    for gate in gates:
        print(
            "  - "
            f"{gate.get('gate_id')} "
            f"[{gate.get('status')}] "
            f"{gate.get('gate_contract')} "
            f"{gate.get('package_key')} "
            f"{'retained ' if gate.get('retained_example') else ''}"
            f"{gate.get('path')}"
        )


def print_text_review_inspect(report: dict[str, Any]) -> None:
    gate = report["gate"]
    artifact = report["artifact"]
    print(f"content-agent review inspect: {gate.get('gate_id')}")
    print(f"path: {gate.get('path')}")
    print(f"status: {gate.get('status')}")
    print(f"gate_contract: {gate.get('gate_contract')}")
    print(f"gate_type: {gate.get('gate_type')}")
    print(f"package: {gate.get('package')}")
    print(f"workflow: {gate.get('workflow_id')} / {gate.get('step_id')}")
    print(f"run_id: {gate.get('run_id')}")
    if gate.get("stop_reason"):
        print(f"stop_reason: {gate.get('stop_reason')}")
    evidence = artifact.get("evidence") if isinstance(artifact.get("evidence"), dict) else {}
    preview_paths = evidence.get("preview_paths", [])
    evidence_paths = evidence.get("evidence_paths", [])
    if preview_paths:
        print("preview_paths:")
        for relpath in preview_paths:
            print(f"  - {relpath}")
    if evidence_paths:
        print("evidence_paths:")
        for relpath in evidence_paths:
            print(f"  - {relpath}")
    validation_results = evidence.get("validation_results", [])
    if validation_results:
        print("validation_results:")
        for result in validation_results:
            if not isinstance(result, dict):
                continue
            summary = f": {result.get('summary')}" if result.get("summary") else ""
            print(f"  - {result.get('id')}: {result.get('status')}{summary}")
    approval = artifact.get("approval") if isinstance(artifact.get("approval"), dict) else {}
    if approval:
        dimensions = [
            key
            for key in (
                "quality_required",
                "external_mutation_required",
                "lifecycle_movement_required",
                "promotion_required",
            )
            if approval.get(key) is True
        ]
        print("approval_required: " + (", ".join(dimensions) if dimensions else "none"))
        print("allowed_decisions: " + ", ".join(str(item) for item in approval.get("allowed_decisions", [])))
    decision = artifact.get("decision")
    if isinstance(decision, dict):
        print(f"decision: {decision.get('outcome')} by {decision.get('decided_by')} at {decision.get('decided_at')}")
    else:
        print("decision: pending")
    resume = artifact.get("resume") if isinstance(artifact.get("resume"), dict) else {}
    if resume.get("command_hint"):
        print(f"command_hint: {resume.get('command_hint')}")


def print_text_review_decision(report: dict[str, Any]) -> None:
    gate = report["gate"]
    decision = report["decision"]
    print(f"content-agent review {decision.get('outcome')}: {gate.get('gate_id')}")
    print(f"path: {gate.get('path')}")
    print(f"mutating: {str(report.get('mutating') is True).lower()}")
    print(f"status: {report.get('status_before')} -> {report.get('status_after')}")
    print(f"decision: {decision.get('outcome')} by {decision.get('decided_by')} at {decision.get('decided_at')}")
    print(f"reason: {decision.get('reason')}")
    print("approval_dimensions:")
    for dimension in ("quality", "external_mutation", "lifecycle_movement", "promotion"):
        record = decision.get("approval_dimensions", {}).get(dimension, {})
        print(
            "  - "
            f"{dimension}: required={str(record.get('required') is True).lower()}, "
            f"approved={str(record.get('approved') is True).lower()}"
        )
    external = decision.get("external_mutation", {})
    print(
        "external_mutation_effect: "
        f"approved={str(external.get('approved') is True).lower()}, "
        f"effect={external.get('effect')}"
    )
    effects = decision.get("state_effects", {})
    print(
        "state_effects: "
        f"package_status={effects.get('package_status')}, "
        f"lifecycle_movement={effects.get('lifecycle_movement')}, "
        f"promotion={effects.get('promotion')}"
    )
    run_record = report.get("run_record")
    if isinstance(run_record, dict):
        print(f"run_record: {run_record.get('path')}")
    else:
        print("run_record: none")
    if report.get("message"):
        print(f"message: {report.get('message')}")


def print_text_run_resolution(report: dict[str, Any]) -> None:
    print(f"content-agent run: {report.get('workflow_id')}")
    print(f"package: {report.get('package')}")
    print(f"run_id: {report.get('run_id')}")
    print(f"run_mode: {report.get('run_mode')}")
    print(f"persisted: {str(report.get('persisted') is True).lower()}")
    if report.get("resolved_run_path"):
        print(f"resolved_run: {report.get('resolved_run_path')}")
    reasons = report.get("persistence_reasons", [])
    print("persistence_reasons: " + (", ".join(reasons) if reasons else "none"))
    selected_steps = report.get("resolved_run", {}).get("selected_steps", [])
    selected_gates = report.get("resolved_run", {}).get("selected_gates", [])
    print(f"selected_steps: {len(selected_steps)}")
    print(f"selected_gates: {len(selected_gates)}")
    if report.get("message"):
        print(f"message: {report.get('message')}")


def print_text_run_execution(report: dict[str, Any]) -> None:
    print(f"content-agent run: {report.get('workflow_id')}")
    print(f"package: {report.get('package')}")
    print(f"run_id: {report.get('run_id')}")
    print(f"terminal_status: {report.get('terminal_status')}")
    print(f"stop_reason: {report.get('stop_reason')}")
    print(f"resolved_run: {report.get('resolved_run_path')}")
    print(f"run_record: {report.get('run_record_path')}")
    if report.get("review_gate_path"):
        print(f"review_gate: {report.get('review_gate_id')} ({report.get('review_gate_path')})")
    else:
        print("review_gate: none")
    print(f"scriptable_steps_executed: {report.get('scriptable_steps_executed')}")


def print_text_resume(report: dict[str, Any]) -> None:
    print(f"content-agent resume: {report.get('source')}")
    print(f"source: {report.get('source_path')}")
    print(f"package: {report.get('package')}")
    print(f"workflow: {report.get('workflow_id')}")
    print(f"resolved_run: {report.get('resolved_run_path')}")
    print(f"run_record: {report.get('run_record_path')}")
    print(f"terminal_status: {report.get('terminal_status')}")
    if report.get("message"):
        print(f"message: {report.get('message')}")


def print_text_gate_check(report: dict[str, Any]) -> None:
    print(f"content-agent gate check: {report['gate_id']}")
    print(f"status: {report['status']}")
    print(f"decision: {report['decision']}")
    print(f"blocking: {report['blocking']}")
    print(f"recommended_workflow: {report['recommended_workflow']}")
    print(f"recommended_validator: {report['recommended_validator']}")
    print(f"proof_mode: {report['proof_mode']}")
    print(f"log: {report['log_path']}")
    if report.get("missing_artifacts"):
        print("missing_artifacts:")
        for item in report["missing_artifacts"]:
            print(f"  - {item}")
    if report.get("details"):
        print("details:")
        for key, value in report["details"].items():
            if value in (None, "", []):
                continue
            print(f"  - {key}: {value}")


def print_text_next(report: dict[str, Any]) -> None:
    print(f"content-agent next: {report.get('package')}")
    if report.get("has_pending_review_gate_blockers"):
        print("blocked_by_pending_review_gates: true")
        for gate in report.get("pending_review_gate_blockers", []):
            print(f"  - {gate.get('gate_id')} ({gate.get('path')})")
    else:
        print("blocked_by_pending_review_gates: false")
    print(f"all_stages_complete: {report.get('all_stages_complete')}")
    print(f"next_stage: {report.get('next_stage')}")
    if report.get("effective_workflow"):
        print(f"effective_workflow: {report.get('effective_workflow')}")
        print(f"effective_kind: {report.get('effective_workflow_kind')}")
        print(f"effective_next_action: {report.get('effective_next_action')}")
        print(f"effective_can_execute: {report.get('effective_can_execute')}")
        print(f"effective_requires_approval: {report.get('effective_requires_approval')}")
        print(f"effective_approval_gate: {report.get('effective_approval_gate')}")
    else:
        print(f"can_execute: {report.get('can_execute')}")
        print(f"requires_approval: {report.get('requires_approval')}")
        print(f"approval_gate: {report.get('approval_gate')}")
    if report.get("blocking_issues"):
        print("blocking_issues:")
        for issue in report["blocking_issues"]:
            print(f"  - {issue}")
    if report.get("suggested_commands"):
        print("suggested_commands:")
        for command in report["suggested_commands"]:
            print(f"  - {command}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic Phase 2 content-agent facade.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Initialize or check content-agent runtime surfaces.")
    init.add_argument("--check-only", action="store_true", help="Report setup state without creating directories.")
    init.add_argument("--format", choices=["text", "json"], default="text")

    status = subparsers.add_parser("status", help="Report package, gate, run, and validation state.")
    status.add_argument("--package", help="Package path or key under publications/.")
    status.add_argument("--limit", type=int, default=DEFAULT_RECENT_LIMIT, help="Recent run/log records to show.")
    status.add_argument("--format", choices=["text", "json"], default="text")

    next_cmd = subparsers.add_parser("next", help="Resolve the next read-only eligible package action.")
    next_cmd.add_argument("--package", required=True, help="Package path or key under publications/.")
    next_cmd.add_argument("--format", choices=["text", "json"], default="text")

    run = subparsers.add_parser("run", help="Create or execute a governed workflow run.")
    run.add_argument("--workflow", required=True, help="Workflow id from workflows/*/workflow.yaml.")
    run.add_argument("--package", required=True, help="Package path or key under publications/.")
    run.add_argument(
        "--mode",
        choices=sorted(VALID_RUN_MODES),
        default="governed_continuous",
        help="Run mode for context admission and persistence policy.",
    )
    run.add_argument("--run-id", help="Optional deterministic run id for tests or handoffs.")
    run.add_argument(
        "--resolve-only",
        action="store_true",
        help="Persist the resolved_run and stop before script execution.",
    )
    run.add_argument(
        "--input",
        action="append",
        default=[],
        help="Runtime input as key=value; may be repeated.",
    )
    run.add_argument("--start-at", help="Start execution at a named workflow step.")
    run.add_argument("--max-scriptable-steps", type=int, help="Maximum scriptable steps to execute before deferring.")
    run.add_argument("--format", choices=["text", "json"], default="text")

    resume = subparsers.add_parser("resume", help="Resume from an approved gate or durable resolved run.")
    resume.add_argument("--gate", help="Approved review gate id, path, or filename.")
    resume.add_argument("--resolved-run", help="Resolved run id, path, or filename.")
    resume.add_argument("--format", choices=["text", "json"], default="text")

    gate = subparsers.add_parser("gate", help="Evaluate first-class workflow gates.")
    gate_subparsers = gate.add_subparsers(dest="gate_command", required=True)
    gate_check = gate_subparsers.add_parser("check", help="Evaluate a gate contract without mutating package state.")
    gate_check.add_argument("--gate", required=True, help="Gate id from gate_contracts.yaml.")
    gate_check.add_argument("--package", help="Package path or key under publications/.")
    gate_check.add_argument("--packet", help="Packet path for packet-scoped gates.")
    gate_check.add_argument("--format", choices=["text", "json"], default="text")

    review = subparsers.add_parser("review", help="Inspect file-backed review gates.")
    review_subparsers = review.add_subparsers(dest="review_command", required=True)
    review_list = review_subparsers.add_parser("list", help="List pending and resolved review gates.")
    review_list.add_argument("--package", help="Package path or key under publications/.")
    review_list.add_argument("--status", choices=["pending", "resolved", "all"], default="all")
    review_list.add_argument(
        "--include-retained",
        action="store_true",
        help="Include retained proof examples that are ignored by active gate blockers.",
    )
    review_list.add_argument("--format", choices=["text", "json"], default="text")

    review_inspect = review_subparsers.add_parser("inspect", help="Inspect a single review gate artifact.")
    review_inspect.add_argument("gate_arg", nargs="?", help="Gate id, artifact path, or artifact filename.")
    review_inspect.add_argument("--gate", dest="gate", help="Gate id, artifact path, or artifact filename.")
    review_inspect.add_argument("--format", choices=["text", "json"], default="text")

    for decision_command in ("approve", "reject", "defer"):
        decision_parser = review_subparsers.add_parser(
            decision_command,
            help=f"Record a {decision_command} decision for a pending review gate.",
        )
        decision_parser.add_argument("gate_arg", nargs="?", help="Gate id, artifact path, or artifact filename.")
        decision_parser.add_argument("--gate", dest="gate", help="Gate id, artifact path, or artifact filename.")
        decision_parser.add_argument("--reason", help="Human-readable reason to preserve in the decision record.")
        decision_parser.add_argument(
            "--decided-by",
            default=None,
            help="Actor label to preserve in the decision record.",
        )
        decision_parser.add_argument("--format", choices=["text", "json"], default="text")

    validate = subparsers.add_parser("validate", help="Report contract enforcement readiness without promotion.")
    validate.add_argument("--workflow", help="Workflow id to validate. Defaults to all workflow.yaml contracts.")
    validate.add_argument("--package", help="Package path or key under publications/.")
    validate.add_argument(
        "--mode",
        choices=sorted(VALID_RUN_MODES),
        default="exploratory",
        help="Run mode posture for missing runtime context.",
    )
    validate.add_argument("--input", action="append", default=[], help="Runtime input as key=value.")
    validate.add_argument("--format", choices=["text", "json"], default="text")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        try:
            report = build_init_report(check_only=args.check_only)
        except Exception as exc:
            if args.format == "json":
                print_json({"success": False, "error": str(exc)})
            else:
                print(f"content-agent init failed: {exc}")
            sys.exit(1)
        if args.format == "json":
            print_json(report)
        else:
            print_text_init(report)
        return

    if args.command == "status":
        try:
            report = build_status_report(package_arg=args.package, limit=args.limit)
        except Exception as exc:
            if args.format == "json":
                print_json({"success": False, "error": str(exc)})
            else:
                print(f"content-agent status failed: {exc}")
            sys.exit(1)
        if args.format == "json":
            print_json(report)
        else:
            print_text_status(report)
        return

    if args.command == "review":
        if args.review_command == "list":
            try:
                report = build_review_list_report(
                    package_arg=args.package,
                    status_filter=args.status,
                    include_retained=args.include_retained,
                )
            except Exception as exc:
                if args.format == "json":
                    print_json({"success": False, "error": str(exc)})
                else:
                    print(f"content-agent review list failed: {exc}")
                sys.exit(1)
            if args.format == "json":
                print_json(report)
            else:
                print_text_review_list(report)
            return

        if args.review_command == "inspect":
            identifier = args.gate or args.gate_arg
            if not identifier:
                if args.format == "json":
                    print_json({"success": False, "error": "review inspect requires --gate or a gate argument"})
                else:
                    print("content-agent review inspect failed: review inspect requires --gate or a gate argument")
                sys.exit(1)
            try:
                report = build_review_inspect_report(identifier)
            except Exception as exc:
                if args.format == "json":
                    print_json({"success": False, "error": str(exc)})
                else:
                    print(f"content-agent review inspect failed: {exc}")
                sys.exit(1)
            if args.format == "json":
                print_json(report)
            else:
                print_text_review_inspect(report)
            return

        if args.review_command in {"approve", "reject", "defer"}:
            identifier = args.gate or args.gate_arg
            if not identifier:
                message = f"review {args.review_command} requires --gate or a gate argument"
                if args.format == "json":
                    print_json({"success": False, "error": message})
                else:
                    print(f"content-agent review {args.review_command} failed: {message}")
                sys.exit(1)
            try:
                report = build_review_decision_report(
                    identifier,
                    args.review_command,
                    reason=args.reason,
                    decided_by=args.decided_by,
                )
            except Exception as exc:
                if args.format == "json":
                    print_json({"success": False, "error": str(exc)})
                else:
                    print(f"content-agent review {args.review_command} failed: {exc}")
                sys.exit(1)
            if args.format == "json":
                print_json(report)
            else:
                print_text_review_decision(report)
            return

    if args.command == "run":
        try:
            runtime_inputs = parse_runtime_inputs(args.input)
            if args.resolve_only:
                report = build_run_resolve_report(
                    args.workflow,
                    args.package,
                    run_mode=args.mode,
                    runtime_inputs=runtime_inputs,
                    supplied_run_id=args.run_id,
                )
            else:
                report = build_run_execution_report(
                    args.workflow,
                    args.package,
                    run_mode=args.mode,
                    runtime_inputs=runtime_inputs,
                    supplied_run_id=args.run_id,
                    start_at=args.start_at,
                    max_scriptable_steps=args.max_scriptable_steps,
                )
        except Exception as exc:
            if args.format == "json":
                print_json({"success": False, "error": str(exc)})
            else:
                print(f"content-agent run failed: {exc}")
            sys.exit(1)
        if args.format == "json":
            print_json(report)
        else:
            if report.get("kind") == "content_agent_run_resolution":
                print_text_run_resolution(report)
            else:
                print_text_run_execution(report)
        return

    if args.command == "resume":
        try:
            report = build_resume_report(
                gate_identifier=args.gate,
                resolved_run_identifier=args.resolved_run,
            )
        except Exception as exc:
            if args.format == "json":
                print_json({"success": False, "error": str(exc)})
            else:
                print(f"content-agent resume failed: {exc}")
            sys.exit(1)
        if args.format == "json":
            print_json(report)
        else:
            print_text_resume(report)
        return

    if args.command == "gate":
        if args.gate_command == "check":
            try:
                report = build_gate_check_report(
                    args.gate,
                    package_arg=args.package,
                    packet_arg=args.packet,
                )
            except Exception as exc:
                if args.format == "json":
                    print_json({"success": False, "error": str(exc)})
                else:
                    print(f"content-agent gate check failed: {exc}")
                sys.exit(1)
            if args.format == "json":
                print_json(report)
            else:
                print_text_gate_check(report)
            if report["blocking"]:
                sys.exit(1)
            return

    if args.command == "next":
        try:
            report = build_next_report(args.package)
        except Exception as exc:
            if args.format == "json":
                print_json({"success": False, "error": str(exc)})
            else:
                print(f"content-agent next failed: {exc}")
            sys.exit(1)
        if args.format == "json":
            print_json(report)
        else:
            print_text_next(report)
        return

    if args.command == "validate":
        try:
            report = build_validation_report(
                workflow_id=args.workflow,
                package_arg=args.package,
                mode=args.mode,
                runtime_inputs=parse_runtime_inputs(args.input),
            )
        except Exception as exc:
            if args.format == "json":
                print(json.dumps({"success": False, "error": str(exc)}, indent=2))
            else:
                print(f"content-agent validate failed: {exc}")
            sys.exit(1)

        if args.format == "json":
            print_json(report)
        else:
            print_text_report(report)
        if not report["success"]:
            sys.exit(1)
        return

    parser.error(f"unsupported command: {args.command}")


if __name__ == "__main__":
    main()
