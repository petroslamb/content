#!/usr/bin/env python3
"""Validate Phase 2.8a experimental workflow operating state."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

from lifecycle import REPO_ROOT, WORKFLOWS_DIR, split_frontmatter


CURRENT_GOVERNED_EXPERIMENT_DIRS = {
    "expert-feedback-outreach",
    "paper-development",
    "post-ceiling-pivot",
    "reddit-discussion-lab",
    "youtube-cinematic-pilot",
    "youtube-cinematic-rollout",
    "youtube-insight-authority",
}

LIFECYCLE_HEADING = "## Phase 2.8 Lifecycle State"
LIFECYCLE_FIELDS = [
    "State",
    "Governed contract",
    "Proof runs",
    "Promotion status",
    "Promotion blockers",
]

ALLOWED_STATES = {
    "documented",
    "contracted",
    "active_experiment",
    "proof_backed",
    "promotion_candidate",
    "retired",
}
ALLOWED_CONTRACT_STATUS = {"present", "absent", "readme_only"}
ALLOWED_PROMOTION_STATUS = {"not_candidate", "promotion_candidate", "retired"}
NON_CLEAN_TERMINAL_STATUSES = {"deferred", "failed", "failure", "error", "cancelled", "canceled"}

REQUIRED_FRONTMATTER_FIELDS = ["expected_outputs", "done_when", "approval_gate"]
REQUIRED_GOVERNED_SECTIONS = ["outputs", "steps"]
REQUIRED_VALIDATION_LISTS = ["static_checks", "context_checks"]

CODE_SPAN_RE = re.compile(r"`([^`]+)`")
FIELD_RE = re.compile(r"^- (?P<field>[^:]+): (?P<value>.+)$")


def repo_relpath(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text()) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{repo_relpath(path)} must contain a YAML mapping.")
    return data


def experimental_readmes(errors: list[str]) -> list[tuple[Path, dict[str, Any], str]]:
    readmes: list[tuple[Path, dict[str, Any], str]] = []
    for readme_path in sorted(WORKFLOWS_DIR.glob("*/README.md")):
        if readme_path.parent.name == "skills":
            continue
        text = readme_path.read_text()
        if not text.startswith("---"):
            continue
        try:
            frontmatter_text, body = split_frontmatter(text)
            metadata = yaml.safe_load(frontmatter_text) or {}
        except Exception as exc:
            errors.append(f"{repo_relpath(readme_path)}: {exc}")
            continue
        if not isinstance(metadata, dict):
            errors.append(f"{repo_relpath(readme_path)}: frontmatter must be a mapping.")
            continue
        if metadata.get("stability") == "experimental":
            readmes.append((readme_path, metadata, body))
    return readmes


def extract_lifecycle_block(readme_path: Path, body: str, errors: list[str]) -> dict[str, str]:
    lines = body.splitlines()
    start_index = None
    for index, line in enumerate(lines):
        if line.strip() == LIFECYCLE_HEADING:
            start_index = index + 1
            break
    if start_index is None:
        errors.append(f"{repo_relpath(readme_path)}: missing {LIFECYCLE_HEADING}.")
        return {}

    block_lines: list[str] = []
    for line in lines[start_index:]:
        if line.startswith("## "):
            break
        if line.strip():
            block_lines.append(line.rstrip())

    fields: dict[str, str] = {}
    seen_order: list[str] = []
    for line in block_lines:
        match = FIELD_RE.match(line)
        if not match:
            errors.append(
                f"{repo_relpath(readme_path)}: lifecycle block line must use '- Field: value': {line}"
            )
            continue
        field = match.group("field").strip()
        value = match.group("value").strip()
        fields[field] = value
        seen_order.append(field)

    missing = [field for field in LIFECYCLE_FIELDS if field not in fields]
    extra = [field for field in fields if field not in LIFECYCLE_FIELDS]
    if missing:
        errors.append(f"{repo_relpath(readme_path)}: lifecycle block is missing fields: {', '.join(missing)}.")
    if extra:
        errors.append(f"{repo_relpath(readme_path)}: lifecycle block has unknown fields: {', '.join(extra)}.")
    if seen_order and seen_order != LIFECYCLE_FIELDS:
        errors.append(
            f"{repo_relpath(readme_path)}: lifecycle fields must appear in order: "
            + ", ".join(LIFECYCLE_FIELDS)
        )
    return fields


def first_code_span(value: str) -> str | None:
    match = CODE_SPAN_RE.search(value)
    if not match:
        return None
    return match.group(1).strip()


def require_frontmatter(readme_path: Path, metadata: dict[str, Any], errors: list[str]) -> None:
    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in metadata:
            errors.append(f"{repo_relpath(readme_path)}: frontmatter missing required field '{field}'.")

    for field in ["expected_outputs", "done_when"]:
        value = metadata.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"{repo_relpath(readme_path)}: frontmatter field '{field}' must be a non-empty list.")

    approval_gate = metadata.get("approval_gate")
    if not isinstance(approval_gate, str) or not approval_gate.strip():
        errors.append(f"{repo_relpath(readme_path)}: frontmatter field 'approval_gate' must be a non-empty string.")


def validate_lifecycle_values(readme_path: Path, fields: dict[str, str], errors: list[str]) -> dict[str, str]:
    parsed: dict[str, str] = {}
    checks = [
        ("State", ALLOWED_STATES),
        ("Governed contract", ALLOWED_CONTRACT_STATUS),
        ("Promotion status", ALLOWED_PROMOTION_STATUS),
    ]
    for field, allowed in checks:
        value = fields.get(field)
        if not value:
            continue
        code_value = first_code_span(value)
        if code_value is None:
            errors.append(f"{repo_relpath(readme_path)}: lifecycle field '{field}' must start with a backticked status token.")
            continue
        parsed[field] = code_value
        if code_value not in allowed:
            errors.append(
                f"{repo_relpath(readme_path)}: lifecycle field '{field}' has unsupported status "
                f"'{code_value}', expected one of {sorted(allowed)}."
            )

    proof_runs = fields.get("Proof runs", "")
    proof_status = first_code_span(proof_runs)
    if proof_status is None:
        errors.append(f"{repo_relpath(readme_path)}: lifecycle field 'Proof runs' must record a backticked proof status.")
    else:
        parsed["Proof runs"] = proof_status

    blockers = fields.get("Promotion blockers", "")
    if not blockers or blockers.strip().lower() in {"none", "`none`"}:
        errors.append(f"{repo_relpath(readme_path)}: lifecycle field 'Promotion blockers' must record the remaining promotion proof or approval boundary.")

    return parsed


def validate_governed_contract(
    readme_path: Path,
    metadata: dict[str, Any],
    lifecycle_values: dict[str, str],
    errors: list[str],
) -> str | None:
    workflow_dir = readme_path.parent
    contract_path = workflow_dir / "workflow.yaml"
    workflow_id = metadata.get("workflow_id")
    state = lifecycle_values.get("State")
    governed_status = lifecycle_values.get("Governed contract")

    if not contract_path.exists():
        if workflow_dir.name in CURRENT_GOVERNED_EXPERIMENT_DIRS:
            errors.append(f"{repo_relpath(readme_path)}: current experimental workflow must have adjacent workflow.yaml.")
        if state != "documented":
            errors.append(
                f"{repo_relpath(readme_path)}: README-only experimental workflows must use State: `documented`."
            )
        if governed_status not in {"absent", "readme_only"}:
            errors.append(
                f"{repo_relpath(readme_path)}: README-only experimental workflows must record Governed contract: `absent` or `readme_only`."
            )
        return None

    if governed_status != "present":
        errors.append(f"{repo_relpath(readme_path)}: governed experimental workflow must record Governed contract: `present`.")
    if state == "documented":
        errors.append(f"{repo_relpath(readme_path)}: workflow.yaml is present, so lifecycle State cannot remain `documented`.")

    try:
        contract = load_yaml_mapping(contract_path)
    except Exception as exc:
        errors.append(str(exc))
        return None

    if contract.get("workflow_id") != workflow_id:
        errors.append(
            f"{repo_relpath(contract_path)}: workflow_id '{contract.get('workflow_id')}' does not match README '{workflow_id}'."
        )
    if contract.get("stability") != "experimental":
        errors.append(f"{repo_relpath(contract_path)}: governed experiment must keep stability: experimental.")

    for section in REQUIRED_GOVERNED_SECTIONS:
        value = contract.get(section)
        if not isinstance(value, list) or not value:
            errors.append(f"{repo_relpath(contract_path)}: governed experiment must define non-empty {section}.")

    validation = contract.get("validation")
    if not isinstance(validation, dict):
        errors.append(f"{repo_relpath(contract_path)}: governed experiment must define validation mapping.")
    else:
        for key in REQUIRED_VALIDATION_LISTS:
            value = validation.get(key)
            if not isinstance(value, list) or not value:
                errors.append(f"{repo_relpath(contract_path)}: governed experiment must define validation.{key}.")

    trace = contract.get("trace")
    if not isinstance(trace, dict):
        errors.append(f"{repo_relpath(contract_path)}: governed experiment must define trace mapping.")
    else:
        if trace.get("run_record") != "required":
            errors.append(f"{repo_relpath(contract_path)}: governed experiment must define trace.run_record: required.")
        if not isinstance(trace.get("run_record_store"), str) or not trace.get("run_record_store"):
            errors.append(f"{repo_relpath(contract_path)}: governed experiment must define trace.run_record_store.")
        resolved_run = trace.get("resolved_run")
        if not isinstance(resolved_run, dict):
            errors.append(f"{repo_relpath(contract_path)}: governed experiment must define trace.resolved_run mapping.")
        else:
            if not isinstance(resolved_run.get("store"), str) or not resolved_run.get("store"):
                errors.append(f"{repo_relpath(contract_path)}: governed experiment must define trace.resolved_run.store.")
            persist_when = resolved_run.get("persist_when")
            if not isinstance(persist_when, list) or not persist_when:
                errors.append(f"{repo_relpath(contract_path)}: governed experiment must define trace.resolved_run.persist_when.")

    if not isinstance(workflow_id, str) or not workflow_id:
        errors.append(f"{repo_relpath(readme_path)}: frontmatter workflow_id must be a non-empty string.")
        return None
    return workflow_id


def run_content_agent_validate(workflow_id: str, errors: list[str]) -> None:
    command = ["./content-agent", "validate", "--workflow", workflow_id, "--format", "json"]
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        timeout=90,
        check=False,
    )
    command_text = " ".join(command)
    if result.returncode != 0:
        snippet = (result.stderr or result.stdout).strip().splitlines()[:5]
        errors.append(f"{command_text}: failed with exit code {result.returncode}: {' | '.join(snippet)}")
        return
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        errors.append(f"{command_text}: did not emit JSON: {exc}")
        return
    if payload.get("success") is not True:
        findings = payload.get("findings", [])
        summary = "; ".join(str(item.get("message", item)) for item in findings[:5] if isinstance(item, dict))
        errors.append(f"{command_text}: validation report did not succeed. {summary}")


def nested_status_values(value: Any) -> list[str]:
    statuses: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "status" and isinstance(item, str):
                statuses.append(item.lower())
            else:
                statuses.extend(nested_status_values(item))
    elif isinstance(value, list):
        for item in value:
            statuses.extend(nested_status_values(item))
    return statuses


def load_run_record(run_id: str) -> dict[str, Any] | None:
    for suffix in [".yaml", ".json"]:
        path = REPO_ROOT / "reviewable-runs" / "logs" / f"{run_id}{suffix}"
        if not path.exists():
            continue
        if suffix == ".json":
            data = json.loads(path.read_text())
        else:
            data = yaml.safe_load(path.read_text()) or {}
        if isinstance(data, dict):
            return data
    return None


def clean_real_package_proof(run_id: str, workflow_id: str, errors: list[str], readme_path: Path) -> str | None:
    record = load_run_record(run_id)
    if record is None:
        errors.append(f"{repo_relpath(readme_path)}: promotion proof run id '{run_id}' has no retained run record.")
        return None

    record_workflow = record.get("workflow", {}).get("workflow_id")
    if record_workflow != workflow_id:
        errors.append(
            f"{repo_relpath(readme_path)}: proof run '{run_id}' is for workflow '{record_workflow}', expected '{workflow_id}'."
        )
        return None

    package_path = record.get("package", {}).get("path")
    if not isinstance(package_path, str) or not package_path.startswith("publications/"):
        errors.append(f"{repo_relpath(readme_path)}: proof run '{run_id}' must target a real publications/ package.")
        return None

    terminal_status = str(record.get("terminal_status", "")).lower()
    if terminal_status in NON_CLEAN_TERMINAL_STATUSES or "fail" in terminal_status:
        errors.append(f"{repo_relpath(readme_path)}: proof run '{run_id}' is not clean; terminal_status is '{terminal_status}'.")
        return None

    statuses = nested_status_values(record.get("validation_results", []))
    if any(status in {"failed", "failure", "error"} or "fail" in status for status in statuses):
        errors.append(f"{repo_relpath(readme_path)}: proof run '{run_id}' has failed validation status.")
        return None
    if not any(status in {"passed", "success", "succeeded"} for status in statuses):
        errors.append(f"{repo_relpath(readme_path)}: proof run '{run_id}' must include successful validation evidence.")
        return None
    return package_path


def validate_promotion_claim(
    readme_path: Path,
    fields: dict[str, str],
    lifecycle_values: dict[str, str],
    workflow_id: str | None,
    errors: list[str],
) -> None:
    combined = "\n".join(fields.values())
    claims_candidate = (
        lifecycle_values.get("State") == "promotion_candidate"
        or lifecycle_values.get("Promotion status") == "promotion_candidate"
    )
    if not claims_candidate:
        return
    if workflow_id is None:
        errors.append(f"{repo_relpath(readme_path)}: promotion_candidate requires a governed workflow_id.")
        return

    run_ids = [
        token
        for token in CODE_SPAN_RE.findall(combined)
        if token
        not in ALLOWED_STATES
        | ALLOWED_CONTRACT_STATUS
        | ALLOWED_PROMOTION_STATUS
        | {"none_recorded", "deferred_only", "one_clean", "two_clean", "mixed"}
        and "/" not in token
    ]
    unique_run_ids = sorted(set(run_ids))
    if len(unique_run_ids) < 2:
        errors.append(f"{repo_relpath(readme_path)}: promotion_candidate requires at least two proof run ids.")
        return

    clean_package_paths = []
    for run_id in unique_run_ids:
        package_path = clean_real_package_proof(run_id, workflow_id, errors, readme_path)
        if package_path is not None:
            clean_package_paths.append(package_path)

    if len(clean_package_paths) < 2:
        errors.append(f"{repo_relpath(readme_path)}: promotion_candidate requires at least two clean real-package proofs.")
    if len(set(clean_package_paths)) < 2:
        errors.append(f"{repo_relpath(readme_path)}: promotion_candidate proofs must cover at least two distinct package contexts.")

    lowered = combined.lower()
    has_explicit_approval = "approval" in lowered and any(
        marker in lowered for marker in ["approved", "accepted", "explicit approval", "human approval"]
    )
    if not has_explicit_approval:
        errors.append(f"{repo_relpath(readme_path)}: promotion_candidate requires explicit approval text.")


def validate_experimental_workflows() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    validated_files: list[str] = []

    for readme_path, metadata, body in experimental_readmes(errors):
        validated_files.append(repo_relpath(readme_path))
        require_frontmatter(readme_path, metadata, errors)
        fields = extract_lifecycle_block(readme_path, body, errors)
        lifecycle_values = validate_lifecycle_values(readme_path, fields, errors) if fields else {}
        workflow_id = validate_governed_contract(readme_path, metadata, lifecycle_values, errors)
        validate_promotion_claim(readme_path, fields, lifecycle_values, workflow_id, errors)
        if workflow_id is not None:
            validated_files.append(repo_relpath(readme_path.parent / "workflow.yaml"))
            run_content_agent_validate(workflow_id, errors)

    return errors, sorted(set(validated_files))


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Phase 2.8a experimental workflow operating state.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    errors, validated_files = validate_experimental_workflows()
    payload = {
        "success": not errors,
        "errors": errors,
        "validated_files": validated_files,
        "current_governed_experiments": sorted(CURRENT_GOVERNED_EXPERIMENT_DIRS),
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
        if errors:
            sys.exit(1)
        return

    if errors:
        print("Experimental workflow validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    print("Experimental workflow validation passed.")


if __name__ == "__main__":
    main()
