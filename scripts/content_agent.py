#!/usr/bin/env python3
"""Deterministic Phase 2 content-agent facade.

Only `validate` is implemented through Phase 2.3. It reads file-backed
workflow contracts and execution evidence, then reports enforcement and trace
readiness without mutating package state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shlex
import shutil
import sys
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
from harness import load_harness_policy, load_package_scripts, validate_harness_policy
from lifecycle import (
    PUBLICATIONS_DIR,
    REPO_ROOT,
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
    manifest_path = live_draft.with_name(f"{live_draft.stem}-essay-iteration-packet-r{revision}.json")
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Deterministic Phase 2 content-agent facade.")
    subparsers = parser.add_subparsers(dest="command", required=True)

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
            print(json.dumps(report, indent=2))
        else:
            print_text_report(report)
        if not report["success"]:
            sys.exit(1)
        return

    parser.error(f"unsupported command: {args.command}")


if __name__ == "__main__":
    main()
