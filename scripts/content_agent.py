#!/usr/bin/env python3
"""Deterministic Phase 2 content-agent facade.

Only `validate` is implemented in Phase 2.2. It reads file-backed workflow
contracts and reports enforcement readiness without mutating package state.
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
