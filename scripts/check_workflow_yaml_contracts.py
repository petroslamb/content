#!/usr/bin/env python3
"""Validate authored Phase 2 workflow.yaml contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

from lifecycle import REPO_ROOT, WORKFLOWS_DIR, load_gate_contracts, split_frontmatter


REQUIRED_TOP_LEVEL_FIELDS = [
    "workflow_id",
    "version",
    "stability",
    "workflow_kind",
    "workflow_group",
    "summary",
    "package_classes",
    "inputs",
    "context_dependencies",
    "capabilities",
    "allowed_paths",
    "outputs",
    "behavior",
    "enforcement",
    "validation",
    "gates",
    "trace",
    "steps",
]

VALID_STABILITY = {"canonical", "experimental"}
VALID_WORKFLOW_KIND = {"stage", "module", "overlay"}
VALID_PACKAGE_CLASSES = {"leaf", "umbrella"}
VALID_STEP_MODES = {
    "scriptable",
    "codex_session",
    "review_gated",
    "external_mutation_gated",
}
VALID_ENFORCEMENT_POSTURES = {"deny", "detect", "record"}
VALID_GATE_DECISIONS = {"approve", "reject", "defer"}

RUNTIME_REFERENCES = {
    "gate_artifact_paths",
    "lifecycle_guardrail_report",
    "replacement_north_star_gate",
    "run_record",
    "validation_results",
}

IDENTITY_DRIFT_FIELDS = [
    "workflow_id",
    "workflow_kind",
    "stability",
    "workflow_group",
]

DRIFT_STOPWORDS = {
    "a",
    "an",
    "and",
    "any",
    "are",
    "as",
    "be",
    "been",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "into",
    "is",
    "it",
    "its",
    "of",
    "or",
    "the",
    "to",
    "up",
    "when",
    "with",
}

TOKEN_RE = re.compile(r"[a-z0-9_]+")

INVALID_FIXTURES = [
    {
        "path": REPO_ROOT / "scripts" / "fixtures" / "workflow-yaml" / "invalid_missing_fields.yaml",
        "expected_errors": [
            "missing required fields",
            "version must be a positive integer",
            "stability must be one of",
        ],
    },
]


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


def read_readme_frontmatter(readme_path: Path, errors: list[str]) -> dict[str, Any]:
    if not readme_path.exists():
        errors.append(f"{repo_relpath(readme_path.parent / 'workflow.yaml')}: adjacent README.md is missing.")
        return {}
    try:
        frontmatter_text, _ = split_frontmatter(readme_path.read_text())
    except ValueError as exc:
        errors.append(f"{repo_relpath(readme_path)}: {exc}")
        return {}
    data = yaml.safe_load(frontmatter_text) or {}
    if not isinstance(data, dict):
        errors.append(f"{repo_relpath(readme_path)}: frontmatter must be a mapping.")
        return {}
    return data


def require_mapping(contract_path: Path, data: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        errors.append(f"{repo_relpath(contract_path)}: field '{key}' must be a mapping.")
        return {}
    return value


def require_list(contract_path: Path, data: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = data.get(key)
    if not isinstance(value, list):
        errors.append(f"{repo_relpath(contract_path)}: field '{key}' must be a list.")
        return []
    return value


def require_ids(
    contract_path: Path,
    items: list[Any],
    field_name: str,
    errors: list[str],
) -> set[str]:
    ids: set[str] = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{repo_relpath(contract_path)}: {field_name}[{index}] must be a mapping.")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            errors.append(f"{repo_relpath(contract_path)}: {field_name}[{index}] must define a non-empty id.")
            continue
        if item_id in ids:
            errors.append(f"{repo_relpath(contract_path)}: duplicate id '{item_id}' in {field_name}.")
        ids.add(item_id)
    return ids


def command_strings(contract: dict[str, Any]) -> set[str]:
    commands: set[str] = set()
    tools = contract.get("capabilities", {}).get("tools", [])
    if isinstance(tools, list):
        for tool in tools:
            if isinstance(tool, dict) and isinstance(tool.get("command"), str):
                commands.add(normalize_command(tool["command"]))

    hooks = contract.get("validation", {}).get("hooks", [])
    if isinstance(hooks, list):
        for hook in hooks:
            if isinstance(hook, dict) and isinstance(hook.get("command"), str):
                commands.add(normalize_command(hook["command"]))

    steps = contract.get("steps", [])
    if isinstance(steps, list):
        for step in steps:
            if not isinstance(step, dict):
                continue
            executor = step.get("executor")
            if isinstance(executor, dict) and isinstance(executor.get("command"), str):
                commands.add(normalize_command(executor["command"]))
    return commands


def normalize_command(command: str) -> str:
    return " ".join(command.replace("{package_key}", "{package}").split())


def drift_tokens(value: object) -> set[str]:
    if value is None:
        return set()
    text = str(value).replace("-", "_").lower()
    tokens = {
        token
        for token in TOKEN_RE.findall(text)
        if len(token) >= 3 and token not in DRIFT_STOPWORDS
    }
    return tokens


def contract_tokens(contract: dict[str, Any]) -> set[str]:
    return drift_tokens(json.dumps(contract, sort_keys=True))


def token_covered(source_value: object, target_tokens: set[str]) -> bool:
    tokens = drift_tokens(source_value)
    if not tokens:
        return True
    if tokens & target_tokens:
        return True

    # Frontmatter is intentionally prose-heavy. Also accept compact phrase coverage
    # where a contract uses identifiers such as `release_readiness`.
    compact = "_".join(sorted(tokens))
    return compact in target_tokens


def path_exists_from_repo(path: str) -> bool:
    if "{" in path or path.endswith("/"):
        return (REPO_ROOT / path.rstrip("/")).exists()
    return (REPO_ROOT / path).exists()


def path_covered(path_pattern: str, allowed_patterns: list[str]) -> bool:
    if path_pattern.startswith("{live_draft_dir}/"):
        return "publications/{package}/" in allowed_patterns

    if path_pattern.startswith("publications/{package}/"):
        return any(
            allowed == "publications/{package}/"
            or path_pattern.startswith(allowed)
            for allowed in allowed_patterns
        )

    if path_pattern.startswith("reviewable-runs/"):
        return any(path_pattern.startswith(allowed) or allowed == "reviewable-runs/" for allowed in allowed_patterns)

    if "{" in path_pattern:
        return True

    return any(path_pattern.startswith(allowed) for allowed in allowed_patterns)


def validate_readme_drift(contract_path: Path, contract: dict[str, Any], errors: list[str]) -> None:
    readme_path = contract_path.parent / "README.md"
    metadata = read_readme_frontmatter(readme_path, errors)
    if not metadata:
        return
    searchable_contract_tokens = contract_tokens(contract)

    for field in IDENTITY_DRIFT_FIELDS:
        if field not in metadata:
            continue
        if metadata[field] != contract.get(field):
            errors.append(
                f"{repo_relpath(contract_path)}: README frontmatter field '{field}' is "
                f"'{metadata[field]}', expected '{contract.get(field)}'."
            )

    if contract.get("workflow_kind") == "stage":
        stage_binding = metadata.get("stage_binding")
        if stage_binding is not None and stage_binding != contract.get("workflow_id"):
            errors.append(
                f"{repo_relpath(contract_path)}: README stage_binding '{stage_binding}' "
                f"must match workflow_id '{contract.get('workflow_id')}'."
            )

    default_skill = metadata.get("default_skill")
    if default_skill is not None:
        skills = contract.get("capabilities", {}).get("skills", [])
        if not isinstance(skills, list) or default_skill not in skills:
            errors.append(
                f"{repo_relpath(contract_path)}: README default_skill '{default_skill}' "
                "is not listed in workflow.yaml capabilities.skills."
            )

    declared_commands = command_strings(contract)
    for key in ["launch_templates", "validator_commands"]:
        values = metadata.get(key, [])
        if not isinstance(values, list):
            errors.append(f"{repo_relpath(readme_path)}: frontmatter field '{key}' must be a list.")
            continue
        missing = [
            command
            for command in values
            if normalize_command(str(command)) not in declared_commands
        ]
        if missing:
            errors.append(
                f"{repo_relpath(contract_path)}: README {key} not covered by workflow.yaml commands: "
                + "; ".join(missing)
            )

    packet_templates = metadata.get("packet_templates", [])
    if not isinstance(packet_templates, list):
        errors.append(f"{repo_relpath(readme_path)}: frontmatter field 'packet_templates' must be a list.")
        return
    for template in packet_templates:
        if not isinstance(template, str) or not path_exists_from_repo(template):
            errors.append(f"{repo_relpath(readme_path)}: packet template does not exist: {template}")

    context_dependencies = contract.get("context_dependencies", [])
    context_tokens = drift_tokens(json.dumps(context_dependencies, sort_keys=True))
    required_context = metadata.get("required_context", [])
    if not isinstance(required_context, list):
        errors.append(f"{repo_relpath(readme_path)}: frontmatter field 'required_context' must be a list.")
    else:
        missing_context = [
            item
            for item in required_context
            if not token_covered(item, context_tokens | searchable_contract_tokens)
        ]
        if missing_context:
            errors.append(
                f"{repo_relpath(contract_path)}: README required_context not covered by workflow.yaml context: "
                + "; ".join(str(item) for item in missing_context)
            )

    outputs = contract.get("outputs", [])
    output_tokens = drift_tokens(json.dumps(outputs, sort_keys=True))
    expected_outputs = metadata.get("expected_outputs", [])
    if not isinstance(expected_outputs, list):
        errors.append(f"{repo_relpath(readme_path)}: frontmatter field 'expected_outputs' must be a list.")
    else:
        missing_outputs = [
            item
            for item in expected_outputs
            if not token_covered(item, output_tokens | searchable_contract_tokens)
        ]
        if missing_outputs:
            errors.append(
                f"{repo_relpath(contract_path)}: README expected_outputs not covered by workflow.yaml outputs: "
                + "; ".join(str(item) for item in missing_outputs)
            )

    approval_gate = metadata.get("approval_gate")
    gates = contract.get("gates", [])
    gate_tokens = drift_tokens(json.dumps(gates, sort_keys=True))
    if isinstance(approval_gate, str) and approval_gate not in {"", "none"}:
        approval_tokens = drift_tokens(approval_gate)
        if "publish" in approval_tokens or "publication" in approval_tokens:
            if "release_readiness" not in gate_tokens and "live_publish_approval" not in gate_tokens:
                errors.append(
                    f"{repo_relpath(contract_path)}: README approval_gate '{approval_gate}' "
                    "requires a release_readiness or live_publish_approval gate in workflow.yaml."
                )
        elif not gates:
            errors.append(
                f"{repo_relpath(contract_path)}: README approval_gate '{approval_gate}' "
                "requires at least one workflow.yaml gate."
            )


def validate_contract(path: Path, gate_contract_ids: set[str]) -> list[str]:
    errors: list[str] = []
    contract = load_mapping(path)

    missing = [field for field in REQUIRED_TOP_LEVEL_FIELDS if field not in contract]
    if missing:
        errors.append(f"{repo_relpath(path)}: missing required fields: {', '.join(missing)}")

    workflow_id = contract.get("workflow_id")
    if not isinstance(workflow_id, str) or not workflow_id.strip():
        errors.append(f"{repo_relpath(path)}: workflow_id must be a non-empty string.")

    version = contract.get("version")
    if not isinstance(version, int) or version < 1:
        errors.append(f"{repo_relpath(path)}: version must be a positive integer.")

    stability = contract.get("stability")
    if stability not in VALID_STABILITY:
        errors.append(f"{repo_relpath(path)}: stability must be one of {sorted(VALID_STABILITY)}.")

    workflow_kind = contract.get("workflow_kind")
    if workflow_kind not in VALID_WORKFLOW_KIND:
        errors.append(f"{repo_relpath(path)}: workflow_kind must be one of {sorted(VALID_WORKFLOW_KIND)}.")

    if not isinstance(contract.get("workflow_group"), str) or not contract.get("workflow_group"):
        errors.append(f"{repo_relpath(path)}: workflow_group must be a non-empty string.")
    if not isinstance(contract.get("summary"), str) or not contract.get("summary"):
        errors.append(f"{repo_relpath(path)}: summary must be a non-empty string.")

    package_classes = require_list(path, contract, "package_classes", errors)
    invalid_package_classes = sorted(
        item for item in package_classes if not isinstance(item, str) or item not in VALID_PACKAGE_CLASSES
    )
    if invalid_package_classes:
        errors.append(
            f"{repo_relpath(path)}: package_classes contains unsupported values: "
            + ", ".join(str(item) for item in invalid_package_classes)
        )

    require_mapping(path, contract, "inputs", errors)
    behavior = require_mapping(path, contract, "behavior", errors)
    validation = require_mapping(path, contract, "validation", errors)
    trace = require_mapping(path, contract, "trace", errors)
    capabilities = require_mapping(path, contract, "capabilities", errors)
    allowed_paths = require_mapping(path, contract, "allowed_paths", errors)

    context_dependencies = require_list(path, contract, "context_dependencies", errors)
    outputs = require_list(path, contract, "outputs", errors)
    gates = require_list(path, contract, "gates", errors)
    steps = require_list(path, contract, "steps", errors)

    context_ids = require_ids(path, context_dependencies, "context_dependencies", errors)
    output_ids = require_ids(path, outputs, "outputs", errors)
    gate_ids = require_ids(path, gates, "gates", errors)
    step_ids = require_ids(path, steps, "steps", errors)

    tools = capabilities.get("tools", [])
    if not isinstance(tools, list):
        errors.append(f"{repo_relpath(path)}: capabilities.tools must be a list.")
        tools = []
    require_ids(path, tools, "capabilities.tools", errors)
    for tool in tools:
        if isinstance(tool, dict) and not isinstance(tool.get("command"), str):
            errors.append(f"{repo_relpath(path)}: capabilities.tools entry '{tool.get('id')}' must define command.")

    skills = capabilities.get("skills", [])
    if not isinstance(skills, list):
        errors.append(f"{repo_relpath(path)}: capabilities.skills must be a list.")

    hooks = validation.get("hooks", [])
    if hooks is None:
        hooks = []
    if not isinstance(hooks, list):
        errors.append(f"{repo_relpath(path)}: validation.hooks must be a list.")
        hooks = []
    hook_ids = require_ids(path, hooks, "validation.hooks", errors)
    for hook in hooks:
        if isinstance(hook, dict) and not isinstance(hook.get("command"), str):
            errors.append(f"{repo_relpath(path)}: validation hook '{hook.get('id')}' must define command.")

    for dependency in context_dependencies:
        if not isinstance(dependency, dict):
            continue
        if not isinstance(dependency.get("required"), bool):
            errors.append(f"{repo_relpath(path)}: context dependency '{dependency.get('id')}' must define required as boolean.")
        if not isinstance(dependency.get("purpose"), str) or not dependency.get("purpose"):
            errors.append(f"{repo_relpath(path)}: context dependency '{dependency.get('id')}' must define purpose.")
        if not isinstance(dependency.get("record_hash"), bool):
            errors.append(f"{repo_relpath(path)}: context dependency '{dependency.get('id')}' must define record_hash as boolean.")

    read_paths = allowed_paths.get("read", [])
    write_paths = allowed_paths.get("write", [])
    if not isinstance(read_paths, list) or not all(isinstance(item, str) for item in read_paths):
        errors.append(f"{repo_relpath(path)}: allowed_paths.read must be a list of strings.")
        read_paths = []
    if not isinstance(write_paths, list) or not all(isinstance(item, str) for item in write_paths):
        errors.append(f"{repo_relpath(path)}: allowed_paths.write must be a list of strings.")
        write_paths = []

    for output in outputs:
        if not isinstance(output, dict):
            continue
        output_path = output.get("path_template") or output.get("path")
        is_external = output.get("external") is True
        external_target = output.get("external_target")
        if is_external and not isinstance(external_target, str):
            errors.append(f"{repo_relpath(path)}: external output '{output.get('id')}' must define external_target.")
        if not output_path and is_external:
            pass
        elif not isinstance(output_path, str) or not output_path:
            errors.append(f"{repo_relpath(path)}: output '{output.get('id')}' must define path or path_template.")
        elif not path_covered(output_path, write_paths):
            errors.append(
                f"{repo_relpath(path)}: output '{output.get('id')}' path '{output_path}' "
                "is not covered by allowed_paths.write."
            )
        gated_by = output.get("gated_by")
        if gated_by is not None and gated_by not in gate_ids:
            errors.append(f"{repo_relpath(path)}: output '{output.get('id')}' references unknown gate '{gated_by}'.")

    for store_key in ["run_record_store", "gate_store"]:
        store_path = trace.get(store_key)
        if isinstance(store_path, str) and not path_covered(store_path, write_paths):
            errors.append(f"{repo_relpath(path)}: trace.{store_key} '{store_path}' is not covered by allowed_paths.write.")

    resolved_run = trace.get("resolved_run")
    if isinstance(resolved_run, dict):
        store_path = resolved_run.get("store")
        if isinstance(store_path, str) and not path_covered(store_path, write_paths):
            errors.append(
                f"{repo_relpath(path)}: trace.resolved_run.store '{store_path}' is not covered by allowed_paths.write."
            )
    elif resolved_run is not None:
        errors.append(f"{repo_relpath(path)}: trace.resolved_run must be a mapping when present.")

    enforcement = require_mapping(path, contract, "enforcement", errors)
    for key, value in enforcement.items():
        if value not in VALID_ENFORCEMENT_POSTURES:
            errors.append(f"{repo_relpath(path)}: enforcement.{key} must be one of {sorted(VALID_ENFORCEMENT_POSTURES)}.")

    for section in ["preconditions", "invariants"]:
        items = behavior.get(section, [])
        if not isinstance(items, list):
            errors.append(f"{repo_relpath(path)}: behavior.{section} must be a list.")
            continue
        require_ids(path, items, f"behavior.{section}", errors)

    if not isinstance(behavior.get("budgets"), dict):
        errors.append(f"{repo_relpath(path)}: behavior.budgets must be a mapping.")
    if not isinstance(behavior.get("recovery"), dict):
        errors.append(f"{repo_relpath(path)}: behavior.recovery must be a mapping.")

    for gate in gates:
        if not isinstance(gate, dict):
            continue
        gate_contract = gate.get("contract")
        if gate_contract not in gate_contract_ids:
            errors.append(f"{repo_relpath(path)}: gate '{gate.get('id')}' references unknown contract '{gate_contract}'.")
        decisions = gate.get("decisions", [])
        if not isinstance(decisions, list) or not decisions:
            errors.append(f"{repo_relpath(path)}: gate '{gate.get('id')}' must define decisions as a non-empty list.")
        else:
            invalid_decisions = [item for item in decisions if item not in VALID_GATE_DECISIONS]
            if invalid_decisions:
                errors.append(
                    f"{repo_relpath(path)}: gate '{gate.get('id')}' has invalid decisions: "
                    + ", ".join(str(item) for item in invalid_decisions)
                )

    known_consumes = context_ids | output_ids | RUNTIME_REFERENCES
    known_produces = output_ids | RUNTIME_REFERENCES
    for step in steps:
        if not isinstance(step, dict):
            continue
        step_id = step.get("id")
        if step.get("mode") not in VALID_STEP_MODES:
            errors.append(f"{repo_relpath(path)}: step '{step_id}' mode must be one of {sorted(VALID_STEP_MODES)}.")
        if not isinstance(step.get("title"), str) or not step.get("title"):
            errors.append(f"{repo_relpath(path)}: step '{step_id}' must define title.")

        if step.get("mode") == "scriptable":
            executor = step.get("executor")
            if not isinstance(executor, dict) or not (executor.get("command") or executor.get("named")):
                errors.append(f"{repo_relpath(path)}: scriptable step '{step_id}' must define executor.command or executor.named.")
        elif not isinstance(step.get("action"), str) or not step.get("action"):
            errors.append(f"{repo_relpath(path)}: non-scriptable step '{step_id}' must define action.")

        for key, known in [("consumes", known_consumes), ("produces", known_produces)]:
            values = step.get(key, [])
            if not isinstance(values, list):
                errors.append(f"{repo_relpath(path)}: step '{step_id}' field '{key}' must be a list.")
                continue
            unknown = [value for value in values if value not in known]
            if unknown:
                errors.append(
                    f"{repo_relpath(path)}: step '{step_id}' {key} unknown references: "
                    + ", ".join(str(value) for value in unknown)
                )

        step_validation = step.get("validation", {})
        if isinstance(step_validation, dict):
            for hook in step_validation.get("hooks", []):
                if hook not in hook_ids:
                    errors.append(f"{repo_relpath(path)}: step '{step_id}' references unknown validation hook '{hook}'.")
        elif step_validation is not None:
            errors.append(f"{repo_relpath(path)}: step '{step_id}' validation must be a mapping.")

        gate_ref = step.get("gate")
        if isinstance(gate_ref, dict):
            gate_id = gate_ref.get("id")
            if gate_id not in gate_ids:
                errors.append(f"{repo_relpath(path)}: step '{step_id}' references unknown gate '{gate_id}'.")
        elif gate_ref is not None:
            errors.append(f"{repo_relpath(path)}: step '{step_id}' gate must be a mapping.")

        trace_req = step.get("trace", {}).get("required") if isinstance(step.get("trace"), dict) else None
        if trace_req is not True:
            errors.append(f"{repo_relpath(path)}: step '{step_id}' must declare trace.required: true.")

    validate_readme_drift(path, contract, errors)
    return errors


def validate_workflow_yaml_contracts() -> list[str]:
    errors: list[str] = []
    gate_contract_ids = set(load_gate_contracts().keys())
    seen_workflow_ids: dict[str, Path] = {}

    for path in workflow_yaml_paths():
        try:
            contract = load_mapping(path)
            workflow_id = contract.get("workflow_id")
            if isinstance(workflow_id, str):
                if workflow_id in seen_workflow_ids:
                    errors.append(
                        f"{repo_relpath(path)}: duplicate workflow_id '{workflow_id}' also used by "
                        f"{repo_relpath(seen_workflow_ids[workflow_id])}."
                    )
                else:
                    seen_workflow_ids[workflow_id] = path
            errors.extend(validate_contract(path, gate_contract_ids))
        except Exception as exc:
            errors.append(f"{repo_relpath(path)}: {exc}")

    errors.extend(validate_invalid_fixtures(gate_contract_ids))
    return errors


def validate_invalid_fixtures(gate_contract_ids: set[str]) -> list[str]:
    errors: list[str] = []
    for fixture in INVALID_FIXTURES:
        path = fixture["path"]
        if not path.exists():
            errors.append(f"Invalid workflow.yaml fixture is missing: {repo_relpath(path)}")
            continue
        try:
            fixture_errors = validate_contract(path, gate_contract_ids)
        except Exception as exc:
            fixture_errors = [str(exc)]

        if not fixture_errors:
            errors.append(f"Invalid workflow.yaml fixture unexpectedly passed: {repo_relpath(path)}")
            continue

        joined = "\n".join(fixture_errors)
        missing_expected = [
            expected
            for expected in fixture["expected_errors"]
            if expected not in joined
        ]
        if missing_expected:
            errors.append(
                f"Invalid workflow.yaml fixture {repo_relpath(path)} did not emit expected errors: "
                + "; ".join(missing_expected)
            )
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate authored workflow.yaml contracts.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    paths = [repo_relpath(path) for path in workflow_yaml_paths()]
    errors = validate_workflow_yaml_contracts()
    payload = {
        "success": not errors,
        "errors": errors,
        "validated_files": paths,
    }

    if args.format == "json":
        print(json.dumps(payload, indent=2))
        if errors:
            sys.exit(1)
        return

    if errors:
        print("Workflow YAML validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)

    if paths:
        print("Workflow YAML validation passed.")
    else:
        print("Workflow YAML validation passed; no workflow.yaml contracts found.")


if __name__ == "__main__":
    main()
