#!/usr/bin/env python3
"""Read-only local cockpit over Phase 2 content-agent readers."""

from __future__ import annotations

import argparse
import html
import json
import mimetypes
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

import content_agent
from research_exit_support import build_research_exit_gate_path


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_ARTIFACT_MAX_BYTES = 2_000_000
MAX_RECENT_LIMIT = 50
TEXT_MIME_TYPES = {
    "application/json",
    "application/x-yaml",
    "application/yaml",
    "text/markdown",
}
TEXT_SUFFIXES = {
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".txt",
    ".yaml",
    ".yml",
}
VALID_GATE_DECISIONS = {"approve", "reject", "defer"}
MAX_ACTION_BODY_BYTES = 64_000
COCKPIT_LOGS_DIR = content_agent.REPO_ROOT / "reviewable-runs" / "logs"
DEFAULT_RESEARCH_QUESTIONS = {
    "literate-workflow-programming/specification-surface-source-of-truth": (
        "How do controlled, typed, linted, validated, and trace-linked specification surfaces "
        "become the governed source-of-truth artifact in AI-assisted software work, and why is "
        "this different from treating natural language prompts as code?"
    ),
}


@dataclass(frozen=True)
class CockpitConfig:
    host: str
    port: int
    package_arg: str | None
    limit: int
    artifact_max_bytes: int


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def unique_json_path(directory: Path, stem: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    candidate = directory / f"{stem}.json"
    if not candidate.exists():
        return candidate
    index = 2
    while True:
        candidate = directory / f"{stem}-{index}.json"
        if not candidate.exists():
            return candidate
        index += 1


def clamp_limit(value: str | None, default: int) -> int:
    if not value:
        return default
    try:
        parsed = int(value)
    except ValueError:
        return default
    return max(1, min(parsed, MAX_RECENT_LIMIT))


def first_query_value(query: dict[str, list[str]], key: str) -> str | None:
    values = query.get(key)
    if not values:
        return None
    value = values[0].strip()
    return value or None


def cockpit_status_payload(package_arg: str | None, limit: int) -> dict[str, object]:
    return {
        "kind": "content_cockpit_status",
        "schema_version": 1,
        "generated_at": utc_now(),
        "readers": [
            "content_agent.build_status_report",
        ],
        "status": content_agent.build_status_report(package_arg=package_arg, limit=limit),
    }


def cockpit_gate_list_payload(package_arg: str | None, status_filter: str) -> dict[str, object]:
    return {
        "kind": "content_cockpit_gate_list",
        "schema_version": 1,
        "generated_at": utc_now(),
        "readers": [
            "content_agent.build_review_list_report",
        ],
        "review_gates": content_agent.build_review_list_report(
            package_arg=package_arg,
            status_filter=status_filter,
        ),
    }


def cockpit_gate_payload(identifier: str) -> dict[str, object]:
    return {
        "kind": "content_cockpit_gate",
        "schema_version": 1,
        "generated_at": utc_now(),
        "readers": [
            "content_agent.build_review_inspect_report",
        ],
        "review_gate": content_agent.build_review_inspect_report(identifier),
    }


def cockpit_next_payload(package_arg: str) -> dict[str, object]:
    next_report = content_agent.build_next_report(package_arg)
    next_report["cockpit_wizard"] = cockpit_wizard_state(package_arg, next_report)
    next_report["cockpit_view_model"] = build_cockpit_view_model(package_arg, next_report)
    return {
        "kind": "content_cockpit_next",
        "schema_version": 1,
        "generated_at": utc_now(),
        "readers": [
            "content_agent.build_next_report",
        ],
        "next": next_report,
    }


def latest_launch_pack(package_key: str, stage: str) -> dict[str, object] | None:
    if not COCKPIT_LOGS_DIR.exists():
        return None
    for path in sorted(COCKPIT_LOGS_DIR.glob("*_launch-pack.json"), reverse=True):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if payload.get("kind") != "harness_launch_pack":
            continue
        if payload.get("package") != package_key or payload.get("stage") != stage:
            continue
        return {
            "status": "completed",
            "path": content_agent.repo_relpath(path),
            "run_id": payload.get("run_id") or path.stem,
            "timestamp": payload.get("timestamp"),
            "task_brief": payload.get("task_brief"),
        }
    return None


def cockpit_wizard_state(package_arg: str, next_report: dict[str, object]) -> dict[str, object]:
    package_key = content_agent.coerce_package_key(package_arg)
    stage = str(next_report.get("next_stage") or next_report.get("effective_workflow") or "")
    gate_statuses = next_report.get("gate_statuses")
    research_exit = gate_statuses.get("research_exit") if isinstance(gate_statuses, dict) else None
    if not isinstance(research_exit, dict) or research_exit.get("blocking") is not True:
        return {"schema_version": 1, "steps": []}
    launch_pack = latest_launch_pack(package_key, stage) if stage else None
    prompt = (
        "Create the research-exit gate artifact and claim-boundary surface for "
        f"{package_key}. Use the generated launch pack and the package evidence/brief as context."
    )
    return {
        "schema_version": 1,
        "steps": [
            {
                "id": "research_question",
                "label": "Research question admitted",
                "status": "completed",
            },
            {
                "id": "launch_pack",
                "label": "Guided launch pack generated",
                "status": "completed" if launch_pack else "available",
                "artifact": launch_pack,
            },
            {
                "id": "codex_research_exit_packet",
                "label": "Codex prepares research-exit packet",
                "status": "next" if launch_pack else "waiting",
                "prompt": prompt,
            },
        ],
        "next_instruction": prompt if launch_pack else "Generate a launch pack or ask Codex to prepare the research-exit packet directly.",
        "launch_pack": launch_pack,
    }


def build_cockpit_view_model(package_arg: str, next_report: dict[str, object]) -> dict[str, object]:
    """Build a cockpit-specific adapter model without changing workflow/status schemas."""
    wizard = next_report.get("cockpit_wizard")
    if not isinstance(wizard, dict):
        wizard = cockpit_wizard_state(package_arg, next_report)
    gate_statuses = next_report.get("gate_statuses")
    blocking_issues = next_report.get("blocking_issues")
    required_context = next_report.get("required_context")
    return {
        "schema_version": 1,
        "default_tab": "workflow-map",
        "tabs": ["workflow-map", "wizard", "gates", "diagnostics"],
        "wizard": {
            "steps": wizard.get("steps", []),
            "next_instruction": wizard.get("next_instruction"),
            "safe_actions": [],
            "disabled_reasons": blocking_issues if isinstance(blocking_issues, list) else [],
        },
        "gates": {
            "gate_statuses": gate_statuses if isinstance(gate_statuses, dict) else {},
        },
        "diagnostics": {
            "required_context": required_context if isinstance(required_context, list) else [],
            "launch_pack": wizard.get("launch_pack"),
        },
        "workflow_map": build_workflow_map_view_model(package_arg, next_report),
    }


WORKFLOW_LIFECYCLE_ORDER = {
    "topic_discovery": 10,
    "research": 20,
    "paper_intake": 30,
    "evidence_authorization": 40,
    "essay_iteration": 50,
    "article_polish": 60,
    "release_gate": 70,
    "substack_publishing": 80,
    "distribution": 90,
    "post_ceiling_pivot": 100,
    "substack_archive_sync": 900,
}


def workflow_lifecycle_sort_key(item: tuple[str, dict[str, object]]) -> tuple[int, str]:
    workflow_id, contract = item
    data = contract.get("data") if isinstance(contract, dict) else {}
    group = data.get("workflow_group") if isinstance(data, dict) else ""
    kind = data.get("workflow_kind") if isinstance(data, dict) else ""
    normalized = workflow_id.replace("-", "_")
    if normalized in WORKFLOW_LIFECYCLE_ORDER:
        return (WORKFLOW_LIFECYCLE_ORDER[normalized], workflow_id)
    if kind == "stage":
        return (300, workflow_id)
    if group == "evidence":
        return (400, workflow_id)
    if group == "editorial":
        return (500, workflow_id)
    if group == "publication":
        return (600, workflow_id)
    return (800, workflow_id)


def listify(value: object) -> list[object]:
    if isinstance(value, list):
        return value
    if value in (None, ""):
        return []
    return [value]


def stringify_list(value: object) -> list[str]:
    return [str(item) for item in listify(value)]


def step_gate_id(step: dict[str, object]) -> str | None:
    gate = step.get("gate")
    if isinstance(gate, dict):
        gate_id = gate.get("id")
        return str(gate_id) if gate_id else None
    if isinstance(gate, str):
        return gate
    return None


def step_validation_hooks(step: dict[str, object]) -> list[str]:
    validation = step.get("validation")
    if not isinstance(validation, dict):
        return []
    return stringify_list(validation.get("hooks"))


def current_workflow_id(next_report: dict[str, object]) -> str:
    return str(
        next_report.get("effective_workflow")
        or next_report.get("active_overlay")
        or next_report.get("umbrella_route_workflow")
        or next_report.get("next_stage")
        or ""
    )


def blocked_gate_ids(next_report: dict[str, object]) -> set[str]:
    gates = next_report.get("gate_statuses")
    if not isinstance(gates, dict):
        return set()
    return {
        str(gate_id)
        for gate_id, gate in gates.items()
        if isinstance(gate, dict) and gate.get("blocking") is True
    }


def derive_workflow_step_state(
    workflow_id: str,
    step: dict[str, object],
    next_report: dict[str, object],
    active_workflow: str,
    blocked_gates: set[str],
) -> tuple[str, str, bool]:
    gate_id = step_gate_id(step)
    mode = str(step.get("mode") or "")
    gates = next_report.get("gate_statuses")
    gate_status = gates.get(gate_id) if isinstance(gates, dict) and gate_id else None
    if isinstance(gate_status, dict) and gate_status.get("blocking") is not True:
        status_text = str(gate_status.get("status") or gate_status.get("decision") or "")
        if status_text in {"pass", "passed", "ready", "completed", "ready_for_essay_iteration"}:
            return ("completed", f"Gate '{gate_id}' has a non-blocking passing status.", False)
    if gate_id and gate_id in blocked_gates:
        return ("blocked", f"Gate '{gate_id}' is currently blocking this package.", True)
    if workflow_id == active_workflow and gate_id and blocked_gates:
        return ("future", "This step is gated after the current blocker is resolved.", False)
    if workflow_id == active_workflow and not blocked_gates:
        return ("available", "This step belongs to the active workflow route.", True)
    if workflow_id in stringify_list(next_report.get("recommended_workflows")):
        return ("future", "This workflow is recommended after the current package blocker is resolved.", False)
    return ("inferred", "Shown from workflow.yaml; no package-local completion proof is attached.", False)


def workflow_step_instruction(package_key: str, workflow_id: str, step: dict[str, object], state: str) -> str:
    title = str(step.get("title") or step.get("id") or "workflow step")
    action = str(step.get("action") or "")
    gate_id = step_gate_id(step)
    if gate_id == "research_exit" and state == "blocked":
        return (
            "Create the research-exit gate artifact and claim-boundary surface for "
            f"{package_key}. Use the package evidence, brief, status, and any launch pack as context."
        )
    if action:
        return f"Perform workflow step '{title}' for {package_key}: {action}"
    return f"Perform workflow step '{title}' for {package_key}."


def workflow_step_actions(
    package_key: str,
    workflow_id: str,
    step: dict[str, object],
    state: str,
    is_current: bool,
    missing_artifacts: list[str],
) -> dict[str, list[dict[str, str]]]:
    mode = str(step.get("mode") or "unknown")
    gate_id = step_gate_id(step)
    instruction = workflow_step_instruction(package_key, workflow_id, step, state)
    enabled: list[dict[str, str]] = [{"id": "diagnostics", "label": "Open Diagnostics", "target": "diagnostics"}]
    if is_current:
        enabled.insert(0, {"id": "wizard", "label": "Open in Wizard", "target": "wizard"})
    if gate_id or mode == "review_gated":
        enabled.append({"id": "gates", "label": "Open Gates", "target": "gates"})
    if mode in {"codex_session", "external_mutation_gated", "review_gated"} or state in {"blocked", "current"}:
        enabled.append({"id": "copy_instruction", "label": "Copy Codex instruction", "instruction": instruction})
    if gate_id == "research_exit" and any("research-exit" in item or "claim-boundary" in item for item in missing_artifacts):
        enabled.append({
            "id": "prepare_template",
            "label": "Prepare research-exit templates",
            "workflow": workflow_id,
            "step": str(step.get("id") or ""),
        })
    disabled = [
        {
            "id": "reopen_step",
            "label": "Reopen step",
            "reason": "Not operational in cockpit v1; reopening needs explicit workflow-specific state semantics.",
        },
        {
            "id": "rerun_step",
            "label": "Rerun step",
            "reason": "Not operational in cockpit v1; rerun requires a workflow-specific runner binding.",
        },
        {
            "id": "execute_step",
            "label": "Execute step",
            "reason": (
                "Codex-session and external-mutation steps are intentionally manual."
                if mode in {"codex_session", "external_mutation_gated"}
                else "This scriptable step is not yet exposed as a safe cockpit action."
            ),
        },
    ]
    return {"enabled": enabled, "disabled": disabled}


def workflow_step_view(
    package_key: str,
    workflow_id: str,
    step: dict[str, object],
    next_report: dict[str, object],
    active_workflow: str,
    blocked_gates: set[str],
) -> dict[str, object]:
    state, state_reason, is_current = derive_workflow_step_state(
        workflow_id,
        step,
        next_report,
        active_workflow,
        blocked_gates,
    )
    mode = str(step.get("mode") or "unknown")
    executor = step.get("executor")
    command = executor.get("command") if isinstance(executor, dict) else None
    gate_id = step_gate_id(step)
    gates = next_report.get("gate_statuses")
    gate_status = gates.get(gate_id) if isinstance(gates, dict) and gate_id else None
    missing_artifacts = stringify_list(gate_status.get("missing_artifacts")) if isinstance(gate_status, dict) else []
    return {
        "id": str(step.get("id") or "unnamed_step"),
        "title": str(step.get("title") or step.get("id") or "Unnamed step"),
        "mode": mode,
        "action": str(step.get("action") or ""),
        "consumes": stringify_list(step.get("consumes")),
        "produces": stringify_list(step.get("produces")),
        "validation_hooks": step_validation_hooks(step),
        "gate_id": gate_id,
        "missing_artifacts": missing_artifacts,
        "executor_command": str(command) if command else None,
        "state": state,
        "state_reason": state_reason,
        "is_current": is_current,
        "instruction": workflow_step_instruction(package_key, workflow_id, step, state),
        "actions": workflow_step_actions(package_key, workflow_id, step, state, is_current, missing_artifacts),
    }


def workflow_section_view(
    workflow_id: str,
    contract: dict[str, object],
    package_key: str,
    next_report: dict[str, object],
    active_workflow: str,
    blocked_gates: set[str],
) -> dict[str, object]:
    data = contract.get("data") if isinstance(contract, dict) else {}
    path = contract.get("path") if isinstance(contract, dict) else None
    if not isinstance(data, dict):
        data = {}
    steps = [step for step in data.get("steps", []) if isinstance(step, dict)]
    return {
        "id": workflow_id,
        "summary": str(data.get("summary") or ""),
        "workflow_kind": str(data.get("workflow_kind") or ""),
        "workflow_group": str(data.get("workflow_group") or ""),
        "stability": str(data.get("stability") or ""),
        "path": content_agent.repo_relpath(path) if path else "",
        "is_active": workflow_id == active_workflow,
        "steps": [
            workflow_step_view(package_key, workflow_id, step, next_report, active_workflow, blocked_gates)
            for step in steps
        ],
    }


def build_workflow_map_view_model(
    package_arg: str,
    next_report: dict[str, object],
    status_report: dict[str, object] | None = None,
    mode: str = "active_route",
) -> dict[str, object]:
    del status_report, mode
    package_key = content_agent.coerce_package_key(package_arg)
    contracts = content_agent.load_workflow_yaml_contracts()
    active_workflow = current_workflow_id(next_report)
    blocked_gates = blocked_gate_ids(next_report)

    active_ids: list[str] = []

    def push(workflow_id: object) -> None:
        if not workflow_id:
            return
        key = str(workflow_id)
        if key in contracts and key not in active_ids:
            active_ids.append(key)

    push(active_workflow)
    for workflow_id in stringify_list(next_report.get("recommended_workflows")):
        push(workflow_id)
    gates = next_report.get("gate_statuses")
    if isinstance(gates, dict):
        for gate in gates.values():
            if isinstance(gate, dict):
                push(gate.get("recommended_workflow"))
    if not active_ids:
        for fallback in ("research", "essay_iteration", "article_polish"):
            push(fallback)

    active_workflows = [
        workflow_section_view(workflow_id, contracts[workflow_id], package_key, next_report, active_workflow, blocked_gates)
        for workflow_id in active_ids
    ]
    all_workflows = [
        workflow_section_view(workflow_id, contract, package_key, next_report, active_workflow, blocked_gates)
        for workflow_id, contract in sorted(contracts.items(), key=workflow_lifecycle_sort_key)
    ]
    return {
        "schema_version": 1,
        "default_mode": "active_route",
        "default_filter": "all",
        "active_workflow": active_workflow,
        "blocked_gate_ids": sorted(blocked_gates),
        "modes": {
            "active_route": {
                "label": "Active route",
                "description": "Current package route plus recommended support workflows.",
                "workflows": active_workflows,
            },
            "all_workflows": {
                "label": "All workflows",
                "description": "Catalog view of all workflow.yaml contracts.",
                "workflows": all_workflows,
            },
        },
    }


def cockpit_package_list_payload() -> dict[str, object]:
    packages: list[dict[str, str]] = []
    publications_root = content_agent.REPO_ROOT / "publications"
    if publications_root.exists():
        for status_path in sorted(publications_root.rglob("status.yaml")):
            rel_package = status_path.parent.relative_to(publications_root).as_posix()
            packages.append({
                "key": rel_package,
                "path": content_agent.repo_relpath(status_path.parent),
                "status_path": content_agent.repo_relpath(status_path),
            })
    return {
        "kind": "content_cockpit_packages",
        "schema_version": 1,
        "generated_at": utc_now(),
        "packages": packages,
    }


def parse_json_bytes(raw: bytes) -> object:
    if not raw.strip():
        return None
    return json.loads(raw.decode("utf-8"))


def run_content_agent(args: list[str]) -> dict[str, object]:
    return run_repo_command([str(content_agent.REPO_ROOT / "content-agent"), *args])


def run_repo_command(command: list[str]) -> dict[str, object]:
    proc = subprocess.run(
        command,
        cwd=content_agent.REPO_ROOT,
        capture_output=True,
        text=True,
    )
    stdout_payload: object | None
    try:
        stdout_payload = json.loads(proc.stdout) if proc.stdout.strip() else None
    except json.JSONDecodeError:
        stdout_payload = proc.stdout
    payload: dict[str, object] = {
        "kind": "content_cockpit_content_agent_command",
        "schema_version": 1,
        "generated_at": utc_now(),
        "command": shlex.join(command),
        "returncode": proc.returncode,
        "success": proc.returncode == 0,
        "stdout": stdout_payload,
    }
    if proc.stderr.strip():
        payload["stderr"] = proc.stderr
    return payload


def editorial_report_action_payload(package_arg: str) -> dict[str, object]:
    if not package_arg.strip():
        raise ValueError("package is required")
    return run_repo_command(
        [
            str(content_agent.REPO_ROOT / ".venv/bin/python"),
            str(content_agent.REPO_ROOT / "scripts/generate_editorial_report.py"),
            "--package",
            package_arg.strip(),
            "--stdout",
        ]
    )


def validation_action_payload(package_arg: str | None) -> dict[str, object]:
    args = ["validate"]
    if package_arg:
        args.extend(["--package", package_arg])
    args.extend(["--format", "json"])
    return run_content_agent(args)


def next_execute_action_payload(package_arg: str, approved: bool) -> dict[str, object]:
    package_key = content_agent.coerce_package_key(package_arg.strip())
    if not package_key:
        raise ValueError("package is required")
    if not approved:
        raise ValueError("local execution approval is required")
    next_report = content_agent.build_next_report(package_key)
    gate_statuses = next_report.get("gate_statuses")
    research_exit = gate_statuses.get("research_exit") if isinstance(gate_statuses, dict) else {}
    blockers = next_report.get("blocking_issues") if isinstance(next_report.get("blocking_issues"), list) else []
    research_exit_blocked = (
        isinstance(research_exit, dict)
        and research_exit.get("blocking") is True
    ) or any("research_exit" in str(item) for item in blockers)
    if not research_exit_blocked:
        raise ValueError("no cockpit executor is available for the current next step")
    stage = str(next_report.get("next_stage") or "research")
    command_result = run_repo_command(
        [
            "npm",
            "run",
            "stage:resolve",
            "--",
            "--package",
            package_key,
            "--stage",
            stage,
            "--emit-launch-pack",
            "--format",
            "json",
        ]
    )
    return {
        "kind": "content_cockpit_next_execute_result",
        "schema_version": 1,
        "generated_at": utc_now(),
        "success": command_result.get("success") is True,
        "mutating": True,
        "package": package_key,
        "stage": stage,
        "action": "emit_research_stage_launch_pack",
        "message": "Generated a guided research-stage launch pack. This is a handoff artifact and does not clear the research_exit gate." if command_result.get("success") is True else "Launch-pack generation failed.",
        "next_snapshot": next_report,
        "command_result": command_result,
    }


def research_question_action_payload(package_arg: str, research_question: str) -> dict[str, object]:
    package_key = content_agent.coerce_package_key(package_arg.strip())
    if not package_key:
        raise ValueError("package is required")
    question = research_question.strip()
    if not question:
        raise ValueError("research question is required")
    status_path = content_agent.REPO_ROOT / "publications" / package_key / "status.yaml"
    if not status_path.exists():
        raise ValueError(f"status.yaml not found for package: {package_key}")
    text = status_path.read_text(encoding="utf-8")
    quoted_question = json.dumps(question)
    lines = text.splitlines()
    updated_lines: list[str] = []
    saw_config = False
    in_config = False
    inserted = False
    config_indent = ""
    for line in lines:
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]
        if stripped == "config:":
            saw_config = True
            in_config = True
            config_indent = indent
            updated_lines.append(line)
            continue
        if in_config and stripped and not line.startswith(f"{config_indent} "):
            if not inserted:
                updated_lines.append(f"{config_indent}  research_question: {quoted_question}")
                inserted = True
            in_config = False
        if in_config and stripped.startswith("research_question:"):
            updated_lines.append(f"{indent}research_question: {quoted_question}")
            inserted = True
        else:
            updated_lines.append(line)
    if in_config and not inserted:
        updated_lines.append(f"{config_indent}  research_question: {quoted_question}")
        inserted = True
    if not saw_config:
        raise ValueError("status.yaml does not expose config")
    status_path.write_text("\n".join(updated_lines) + "\n", encoding="utf-8")
    return {
        "kind": "content_cockpit_research_question_result",
        "schema_version": 1,
        "generated_at": utc_now(),
        "success": True,
        "mutating": True,
        "package": package_key,
        "status_path": content_agent.repo_relpath(status_path),
        "research_question": question,
        "message": "Research question saved to package status.yaml.",
    }


def research_exit_gate_template(package_key: str, package_path: Path, revision: int, boundary_relpath: str) -> str:
    return f"""---
kind: research_exit_gate
package: {json.dumps(package_key)}
revision: {revision}
governing_brief_path: ""
evidence_surface_path: ""
claim_boundary_status: required_but_missing
claim_boundary_paths:
  - {json.dumps(boundary_relpath)}
research_exit_verdict: pending
dominant_blocker_slug: template-fill-required
follow_on_research_triggers: []
---

# Research Exit Gate

## Governing Blueprint

TODO: Name the governing brief, handoff, or blueprint surface that constrains the essay attempt.

## Evidence Surface

TODO: Summarize the evidence inventory that supports this leaf and name the source index or paper stack.

## Claim Boundaries

TODO: Link the claim-boundary ledger and summarize the allowed, forbidden, and caveated claims.

## Drafting Boundary

TODO: State the draftable object, what must stay out of scope, and what follow-on research remains.

## Verdict

TODO: Choose `ready_for_essay_iteration` or `not_ready` and explain the decision.

## Required Follow-Through

TODO: List the next governed workflow or gate.
"""


def claim_boundary_template(package_key: str) -> str:
    return f"""# Claim-Boundary Ledger

Package: `{package_key}`

## Authorized Core Claim

TODO: State the strongest claim the current evidence permits.

## Forbidden Claims

TODO: List claims the draft must not make.

## Caveats And Source Burden

TODO: Name caveats, weak evidence, and claims that require direct source support.

## Follow-On Research Triggers

TODO: List conditions that should send the package back to research.
"""


def prepare_workflow_template_action_payload(package_arg: str, workflow_id: str, step_id: str) -> dict[str, object]:
    package_key = content_agent.coerce_package_key(package_arg.strip())
    if not package_key:
        raise ValueError("package is required")
    if workflow_id != "research" or step_id != "settle_research_exit_gate":
        raise ValueError("no deterministic cockpit template is available for this workflow step")
    package_path = content_agent.REPO_ROOT / "publications" / package_key
    status_path = package_path / "status.yaml"
    if not status_path.exists():
        raise ValueError(f"status.yaml not found for package: {package_key}")
    status_data = content_agent.load_mapping(status_path)
    revision = status_data.get("revision", 1)
    if not isinstance(revision, int):
        revision = 1
    gate_path = build_research_exit_gate_path(package_path, revision)
    boundary_path = package_path / f"{package_path.name}-claim-boundary-ledger.md"
    boundary_relpath = content_agent.repo_relpath(boundary_path)
    created: list[str] = []
    skipped: list[str] = []
    if not boundary_path.exists():
        boundary_path.write_text(claim_boundary_template(package_key), encoding="utf-8")
        created.append(boundary_relpath)
    else:
        skipped.append(boundary_relpath)
    gate_relpath = content_agent.repo_relpath(gate_path)
    if not gate_path.exists():
        gate_path.write_text(research_exit_gate_template(package_key, package_path, revision, boundary_relpath), encoding="utf-8")
        created.append(gate_relpath)
    else:
        skipped.append(gate_relpath)
    return {
        "kind": "content_cockpit_workflow_template_result",
        "schema_version": 1,
        "generated_at": utc_now(),
        "success": True,
        "mutating": True,
        "package": package_key,
        "workflow": workflow_id,
        "step": step_id,
        "created_paths": created,
        "skipped_existing_paths": skipped,
        "message": "Prepared deterministic research-exit template artifacts." if created else "Research-exit template artifacts already exist.",
    }


def current_next_gate_decision_action_payload(
    package_arg: str,
    outcome: str,
    *,
    reason: str,
    decided_by: str,
) -> dict[str, object]:
    if outcome not in VALID_GATE_DECISIONS:
        raise ValueError("decision must be approve, reject, or defer")
    if not package_arg.strip():
        raise ValueError("package is required")
    if not reason.strip():
        raise ValueError("decision reason is required")

    next_report = content_agent.build_next_report(package_arg.strip())
    requires_approval = bool(next_report.get("requires_approval") is True or next_report.get("effective_requires_approval") is True)
    if not requires_approval:
        raise ValueError("current next action does not require approval")

    approval_gate = (
        next_report.get("effective_approval_gate")
        or next_report.get("approval_gate")
        or next_report.get("gate")
        or "approval_required"
    )
    workflow = (
        next_report.get("effective_workflow")
        or next_report.get("active_overlay")
        or next_report.get("umbrella_route_workflow")
        or next_report.get("next_stage")
        or "unknown_workflow"
    )
    action = (
        next_report.get("effective_next_action")
        or next_report.get("next_overlay_action")
        or next_report.get("next_packet_action")
        or next_report.get("umbrella_route_next_action")
        or "unknown_action"
    )
    package_key = content_agent.coerce_package_key(package_arg.strip())
    manifest_ref, _status_data = content_agent.load_status_ref(package_key)
    stage = next_report.get("next_stage")
    workflow_doc = (
        next_report.get("effective_workflow_doc")
        or next_report.get("workflow_doc")
        or next_report.get("workflow")
        or "unknown"
    )
    timestamp = utc_now()
    stem = (
        f"{timestamp.replace(':', '-').replace('Z', '')}_"
        f"{content_agent.slugify(package_key)}_"
        f"{content_agent.slugify(str(approval_gate))}_cockpit-next-approval"
    )
    log_path = unique_json_path(COCKPIT_LOGS_DIR, stem)
    log_relpath = content_agent.repo_relpath(log_path)
    payload: dict[str, object] = {
        "kind": "content_cockpit_next_approval",
        "schema_version": 2,
        "timestamp": timestamp,
        "run_id": log_path.stem,
        "package": package_key,
        "package_key": package_key,
        "workflow": workflow,
        "stage": stage,
        "action": f"record-{outcome}-decision",
        "success": True,
        "gate_id": approval_gate,
        "status": "recorded",
        "decision": outcome,
        "decided_by": decided_by.strip() or "content-cockpit",
        "reason": reason.strip(),
        "next_action": action,
        "boundary": {
            "type": "approval decision",
            "reason": "Content cockpit recorded an operator decision for a local approval boundary.",
            "external_side_effect": False,
            "approval_gate": approval_gate,
            "approval_required": True,
            "approval_status": outcome,
        },
        "task": {
            "objective": f"Record {outcome} decision for current next-action approval boundary.",
            "stop_condition": "Approval decision written to reviewable-runs/logs/.",
            "non_goals": [
                "Do not move lifecycle state from this approval record alone.",
                "Do not publish or mutate external systems from this approval record.",
            ],
        },
        "execution": {
            "commands": [],
            "output_excerpt": f"{outcome} decision recorded for {approval_gate}.",
            "output_truncated": False,
            "state_before": {"approval_recorded": False},
            "state_after": {
                "approval_recorded": True,
                "approval_status": outcome,
            },
        },
        "evidence": {
            "workflow_doc": workflow_doc,
            "status_path": content_agent.repo_relpath(manifest_ref.status_path),
            "next_snapshot": next_report,
        },
        "verification": {
            "checks": [
                {
                    "name": "approval_log_written",
                    "result": "pass",
                    "notes": log_relpath,
                }
            ],
            "residual_risk": "This record captures operator approval only. A separate lifecycle or gate log must record any state movement.",
        },
        "failure_or_risk": {
            "actual_failure": None,
            "possible_failures": [
                "Approval recorded with insufficient rationale.",
                "Approval record mistaken for lifecycle movement.",
                "Approval record mistaken for external publication or promotion.",
            ],
        },
        "workflow_doc": workflow_doc,
        "status_path": content_agent.repo_relpath(manifest_ref.status_path),
        "effects": {
            "approval_recorded": True,
            "lifecycle_movement_approved": outcome == "approve",
            "lifecycle_movement_performed": False,
            "promotion_performed": False,
            "external_mutation_performed": False,
        },
        "next_snapshot": next_report,
    }
    log_path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    return {
        "kind": "content_cockpit_next_approval_result",
        "schema_version": 1,
        "generated_at": utc_now(),
        "success": True,
        "mutating": True,
        "message": f"{outcome} decision recorded for current approval boundary; no lifecycle state was moved.",
        "approval_log_path": log_relpath,
        "approval": payload,
    }


def gate_decision_action_payload(
    gate_identifier: str,
    outcome: str,
    *,
    reason: str,
    decided_by: str,
) -> dict[str, object]:
    if outcome not in VALID_GATE_DECISIONS:
        raise ValueError("decision must be approve, reject, or defer")
    if not reason.strip():
        raise ValueError("decision reason is required")
    args = [
        "review",
        outcome,
        "--gate",
        gate_identifier,
        "--reason",
        reason.strip(),
        "--decided-by",
        decided_by.strip() or "content-cockpit",
        "--format",
        "json",
    ]
    return run_content_agent(args)


def repo_artifact_path(value: str) -> Path:
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = content_agent.REPO_ROOT / candidate
    resolved = candidate.resolve()
    try:
        relpath = resolved.relative_to(content_agent.REPO_ROOT)
    except ValueError as exc:
        raise ValueError("artifact path must stay inside the repository") from exc
    for part in relpath.parts:
        if part.startswith(".") and part != ".github":
            raise ValueError("artifact path cannot reference local hidden files")
    return resolved


def is_text_artifact(path: Path, mime_type: str | None) -> bool:
    if path.suffix.lower() in TEXT_SUFFIXES:
        return True
    if mime_type in TEXT_MIME_TYPES:
        return True
    return bool(mime_type and mime_type.startswith("text/"))


def json_bytes(payload: object) -> bytes:
    return json.dumps(payload, indent=2, default=str).encode("utf-8")


def page_shell(title: str, body: str, config: CockpitConfig) -> bytes:
    initial = {
        "package": config.package_arg,
        "limit": config.limit,
    }
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f8fa;
      --surface: #ffffff;
      --line: #d8dde6;
      --muted: #5b6575;
      --text: #18202f;
      --accent: #176b87;
      --warn: #a15c00;
      --bad: #a12626;
      --good: #0f7a4f;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font: 14px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
    }}
    header {{
      padding: 8px 24px 7px;
      border-bottom: 1px solid var(--line);
      background: var(--surface);
    }}
    h1 {{
      margin: 0 0 6px;
      font-size: 17px;
      line-height: 1.1;
      font-weight: 700;
      letter-spacing: 0;
    }}
    h2 {{
      margin: 0 0 10px;
      font-size: 15px;
      letter-spacing: 0;
    }}
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    main {{
      width: min(1440px, 100%);
      margin: 0 auto;
      padding: 16px 24px 32px;
    }}
    .toolbar {{
      display: flex;
      align-items: end;
      flex-wrap: wrap;
      gap: 10px;
    }}
    header .toolbar {{
      display: grid;
      grid-template-columns: minmax(320px, 1fr) auto;
      grid-template-areas: "package refresh";
      align-items: end;
      gap: 10px;
    }}
    header .toolbar > .field:first-of-type {{ grid-area: package; }}
    #refresh-button {{ grid-area: refresh; }}
    .field {{
      display: grid;
      gap: 3px;
      min-width: 0;
    }}
    .field label {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }}
    header .toolbar a {{
      min-height: 34px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0 4px;
      font-weight: 700;
    }}
    label {{
      display: grid;
      gap: 4px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 600;
    }}
    input, select, button {{
      height: 30px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      color: var(--text);
      font: inherit;
    }}
    input, select {{ padding: 0 10px; min-width: 0; width: 100%; }}
    input[type="number"] {{ min-width: 76px; width: 100%; }}
    button {{
      padding: 0 14px;
      background: var(--accent);
      border-color: var(--accent);
      color: white;
      cursor: pointer;
    }}
    button[disabled] {{
      background: #e8ecf2;
      border-color: var(--line);
      color: var(--muted);
      cursor: not-allowed;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(12, minmax(0, 1fr));
      gap: 14px;
      align-items: start;
    }}
    section {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--surface);
      padding: 14px;
      min-width: 0;
    }}
    .span-12 {{ grid-column: span 12; }}
    .span-8 {{ grid-column: span 8; }}
    .span-6 {{ grid-column: span 6; }}
    .span-4 {{ grid-column: span 4; }}
    .summary {{
      display: grid;
      grid-template-columns: 2fr repeat(4, minmax(110px, 1fr));
      gap: 10px;
    }}
    .metric {{
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 9px 10px;
      background: #fbfcfd;
    }}
    .metric .label {{ color: var(--muted); font-size: 12px; }}
    .metric .value {{ margin-top: 4px; font-size: 15px; font-weight: 700; overflow-wrap: anywhere; }}
    table {{
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
    }}
    th, td {{
      padding: 8px 7px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      overflow-wrap: anywhere;
    }}
    th {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      background: #fbfcfd;
    }}
    code, pre {{
      font: 12px/1.45 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }}
    pre {{
      margin: 0;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 6px;
      overflow: auto;
      background: #fbfcfd;
      max-height: 62vh;
    }}
    .muted {{ color: var(--muted); }}
    .badge {{
      display: inline-block;
      padding: 2px 7px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: #f7f8fa;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      white-space: nowrap;
    }}
    .badge.good {{ color: var(--good); border-color: #9ad3bd; background: #effaf5; }}
    .badge.warn {{ color: var(--warn); border-color: #e3bd7a; background: #fff8eb; }}
    .badge.bad {{ color: var(--bad); border-color: #e3a0a0; background: #fff3f3; }}
    .callout {{
      border: 1px solid #b7d8e4;
      border-left: 4px solid var(--accent);
      border-radius: 8px;
      padding: 12px;
      background: #f1f9fc;
      margin-bottom: 12px;
    }}
    .callout.warn {{
      border-color: #e3bd7a;
      border-left-color: var(--warn);
      background: #fff8eb;
    }}
    .callout.bad {{
      border-color: #e3a0a0;
      border-left-color: var(--bad);
      background: #fff3f3;
    }}
    .primary-section {{
      border-left: 4px solid var(--accent);
      box-shadow: 0 1px 2px rgba(24, 32, 47, 0.04);
    }}
    .flow-steps {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 10px;
      margin: 12px 0;
    }}
    .flow-step {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfd;
      padding: 10px;
    }}
    .flow-step strong {{
      display: block;
      margin-bottom: 5px;
    }}
    .route-summary {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfd;
      padding: 12px;
      margin: 12px 0;
    }}
    .stage-pills {{
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      margin-top: 10px;
    }}
    .stage-pill {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: var(--surface);
      padding: 4px 8px;
      font-size: 12px;
      font-weight: 700;
      color: var(--text);
    }}
    .wizard-head {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 12px;
      align-items: start;
      margin-bottom: 12px;
    }}
    .wizard-kicker {{
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .03em;
    }}
    .wizard-title {{
      margin-top: 4px;
      font-size: 20px;
      font-weight: 800;
    }}
    .checklist {{
      display: grid;
      gap: 8px;
      margin-top: 12px;
    }}
    .check-row {{
      display: grid;
      grid-template-columns: 140px minmax(0, 1fr);
      gap: 10px;
      align-items: start;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
      background: #fbfcfd;
    }}
    .check-row .name {{
      font-weight: 700;
    }}
    .check-row .detail {{
      color: var(--muted);
    }}
    .help-row {{ display: none; }}
    .approval-panel {{
      display: grid;
      gap: 10px;
      margin: 12px 0;
      padding: 12px;
      border: 1px solid #e3bd7a;
      border-radius: 8px;
      background: #fff8eb;
    }}
    .approval-panel h3 {{
      margin: 0;
      font-size: 14px;
    }}
    .approval-panel input {{
      width: min(100%, 760px);
    }}
    details.advanced {{
      margin-top: 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfd;
      padding: 10px 12px;
    }}
    details.advanced > summary {{
      cursor: pointer;
      font-weight: 700;
      color: var(--muted);
    }}
    .stack {{ display: grid; gap: 14px; }}
    .path-list {{ margin: 0; padding-left: 18px; }}
    .error {{ color: var(--bad); font-weight: 700; }}
    .tabs {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }}
    .tab-button {{
      background: #eef6fa;
      border-color: #b7d8e4;
      color: var(--accent);
    }}
    .tab-button.active {{
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
    }}
    .tab-panel[hidden] {{ display: none; }}
    .workflow-map-controls {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      margin: 10px 0 14px;
    }}
    .workflow-mode-button, .workflow-filter-button, .secondary-button {{
      background: #eef6fa;
      border-color: #b7d8e4;
      color: var(--accent);
    }}
    .workflow-mode-button.active, .workflow-filter-button.active {{
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
    }}
    .workflow-section {{
      display: grid;
      gap: 10px;
      margin-top: 14px;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #fbfcfd;
    }}
    .lifecycle-columns {{
      display: grid;
      grid-auto-flow: column;
      grid-auto-columns: 360px;
      grid-template-columns: none;
      gap: 12px;
      margin-top: 14px;
      overflow-x: auto;
      overflow-y: hidden;
      padding-bottom: 10px;
      scroll-snap-type: x proximity;
    }}
    .lifecycle-lane {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
      background: #ffffff;
      min-width: 360px;
      scroll-snap-align: start;
    }}
    .lifecycle-lane > h3 {{
      margin: 0 0 8px;
      font-size: 13px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }}
    .lifecycle-lane .workflow-section {{
      margin-top: 10px;
      padding: 10px;
    }}
    .workflow-section-head {{
      display: flex;
      gap: 12px;
      align-items: start;
      justify-content: space-between;
    }}
    .workflow-step-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 10px;
    }}
    .workflow-step {{
      height: auto;
      min-height: 116px;
      padding: 10px;
      text-align: left;
      background: white;
      color: var(--text);
      border-color: var(--line);
      display: grid;
      gap: 7px;
      align-content: start;
    }}
    .workflow-step:hover {{
      border-color: var(--accent);
      box-shadow: 0 3px 12px rgba(23, 107, 135, 0.12);
    }}
    .workflow-step.blocked {{
      border-color: #e3a0a0;
      background: #fff8f8;
    }}
    .workflow-step.current {{
      border-left: 4px solid var(--accent);
    }}
    .workflow-step-title {{
      font-weight: 800;
      overflow-wrap: anywhere;
    }}
    .workflow-step-meta {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      align-items: center;
    }}
    .workflow-detail {{
      margin-top: 14px;
      border: 1px solid #b7d8e4;
      border-left: 4px solid var(--accent);
      border-radius: 8px;
      padding: 12px;
      background: #f5fbfd;
    }}
    .disabled-action {{
      display: inline-grid;
      gap: 4px;
      margin: 4px 8px 4px 0;
      vertical-align: top;
    }}
    .disabled-action small {{
      max-width: 240px;
      color: var(--muted);
    }}
    @media (max-width: 1120px) {{
      main, header {{ padding-left: 14px; padding-right: 14px; }}
      header .toolbar {{
        grid-template-columns: minmax(0, 1fr) auto;
        grid-template-areas:
          "package refresh";
      }}
      header .toolbar button, header .toolbar a {{
        width: 100%;
        min-width: 0;
      }}
      #editorial-report-button {{
        white-space: normal;
        line-height: 1.15;
      }}
    }}
    @media (max-width: 640px) {{
      header {{ padding-top: 7px; padding-bottom: 6px; }}
      h1 {{ font-size: 16px; }}
      .grid, .summary {{ display: block; }}
      .flow-steps {{ display: block; }}
      .flow-step {{ margin-bottom: 10px; }}
      .wizard-head, .check-row {{ display: block; }}
      section, .metric {{ margin-bottom: 12px; }}
      input {{ min-width: 0; width: min(100%, 340px); }}
    }}
  </style>
  <script>window.COCKPIT_INITIAL = {json.dumps(initial)};</script>
</head>
<body>
{body}
</body>
</html>
""".encode("utf-8")


def index_page(config: CockpitConfig) -> bytes:
    body = """
<header>
    <h1>Content Agent Cockpit</h1>
  <div class="toolbar">
    <div class="field">
      <select id="package-input" title="Choose a publication package. The dashboard resolves status.yaml, next action, gates, and recent runs for this package.">
        <option value="">All packages</option>
      </select>
    </div>
    <button id="refresh-button" type="button" title="Reload package status, next action, gates, and recent runs.">Refresh</button>
  </div>
</header>
<main>
  <div id="status" class="stack"></div>
  <div id="action-output" class="stack"></div>
</main>
<script>
const initial = window.COCKPIT_INITIAL || {};
const params = new URLSearchParams(window.location.search);
const packageInput = document.getElementById("package-input");
let currentStatusReport = null;
let currentNextReport = null;
let currentWorkflowMap = null;
let activeCockpitTab = (new URLSearchParams(window.location.search)).get("tab") || "workflow-map";
let workflowMapMode = (new URLSearchParams(window.location.search)).get("mode") || "active_route";
let workflowStepFilter = (new URLSearchParams(window.location.search)).get("filter") || "all";
let selectedWorkflowId = (new URLSearchParams(window.location.search)).get("workflow") || "";
let selectedWorkflowStepId = (new URLSearchParams(window.location.search)).get("step") || "";
packageInput.value = params.get("package") || initial.package || "";
document.getElementById("refresh-button").addEventListener("click", loadStatus);
packageInput.addEventListener("change", loadStatus);

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[char]));
}

function badge(value) {
  const raw = String(value ?? "unknown");
  let cls = "badge";
  if (["pass", "passed", "completed", "resolved", "true", "ready"].includes(raw)) cls += " good";
  if (["pending", "warning", "deferred", "gated", "needs approval", "needs research setup", "follow-up", "future", "inferred", "current"].includes(raw)) cls += " warn";
  if (["blocked", "failed", "failing", "error", "invalid", "rejected", "false"].includes(raw)) cls += " bad";
  return `<span class="${cls}">${esc(raw)}</span>`;
}

function artifact(path, label) {
  if (!path) return '<span class="muted">none</span>';
  return `<a class="artifact-link" href="/artifact?path=${encodeURIComponent(path)}" data-artifact-path="${esc(path)}">${esc(label || path)}</a>`;
}

document.addEventListener("click", async (event) => {
  const link = event.target.closest("a.artifact-link");
  if (!link) return;
  event.preventDefault();
  await openArtifactInline(link.dataset.artifactPath || "", link.textContent || "artifact");
});

async function openArtifactInline(path, label) {
  const output = actionOutput();
  if (!path) return;
  showCockpitTab("diagnostics");
  output.innerHTML = `<section>Opening ${esc(label)}...</section>`;
  const response = await fetch(`/artifact?path=${encodeURIComponent(path)}`);
  const text = await response.text();
  output.innerHTML = `<section>
    <h2>${esc(label)}</h2>
    <div class="callout">Previewing repository artifact inline. This does not edit package state.</div>
    <pre>${esc(text)}</pre>
  </section>`;
  output.scrollIntoView({behavior: "smooth", block: "start"});
}

function packageStatusPath(packageKey, filename) {
  if (!packageKey) return null;
  return `publications/${packageKey}/${filename}`;
}

function urlParams() {
  return new URLSearchParams(window.location.search);
}

function urlParam(name) {
  return urlParams().get(name);
}

function updateUrlFromState() {
  const limitInput = document.getElementById("limit-input");
  const limitValue = (limitInput ? limitInput.value : (urlParam("limit") || initial.limit || 5)).toString().trim();
  syncUrlState(packageInput.value.trim(), limitValue);
}

function syncUrlState(packageValue, limitValue) {
  const query = new URLSearchParams();
  if (packageValue) query.set("package", packageValue);
  if (limitValue) query.set("limit", limitValue);
  if (activeCockpitTab) query.set("tab", activeCockpitTab);
  if (workflowMapMode) query.set("mode", workflowMapMode);
  if (workflowStepFilter) query.set("filter", workflowStepFilter);
  if (selectedWorkflowId && selectedWorkflowStepId) {
    query.set("workflow", selectedWorkflowId);
    query.set("step", selectedWorkflowStepId);
  }
  const nextUrl = `${window.location.pathname}${query.toString() ? `?${query.toString()}` : ""}`;
  window.history.replaceState({}, "", nextUrl);
}

async function switchToPackage(packageKey) {
  packageInput.value = packageKey;
  await loadStatus();
}

function inlineValue(value) {
  if (value === null || value === undefined || value === "") return "none";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function actionOutput() {
  return document.getElementById("diagnostic-action-output") || document.getElementById("action-output");
}

function renderCollapsed(title, body, open = false) {
  return `<details class="advanced"${open ? " open" : ""}>
    <summary>${esc(title)}</summary>
    <div style="margin-top:12px">${body}</div>
  </details>`;
}

function showCockpitTab(tabName) {
  activeCockpitTab = tabName;
  for (const button of document.querySelectorAll(".tab-button")) {
    button.classList.toggle("active", button.dataset.tab === tabName);
  }
  for (const panel of document.querySelectorAll(".tab-panel")) {
    panel.hidden = panel.dataset.tab !== tabName;
  }
  updateUrlFromState();
}

async function loadPackageOptions() {
  const selected = packageInput.value || urlParam("package") || initial.package || "";
  try {
    const response = await fetch("/api/packages");
    const payload = await response.json();
    const packages = payload.packages || [];
    const options = ['<option value="">All packages</option>'];
    let hasSelected = selected === "";
    for (const pkg of packages) {
      const key = pkg.key || "";
      if (key === selected) hasSelected = true;
      options.push(`<option value="${esc(key)}">${esc(key)}</option>`);
    }
    if (selected && !hasSelected) options.push(`<option value="${esc(selected)}">${esc(selected)}</option>`);
    packageInput.innerHTML = options.join("");
    packageInput.value = selected;
  } catch (error) {
    packageInput.innerHTML = `<option value="${esc(selected)}">${esc(selected || "All packages")}</option>`;
    packageInput.value = selected;
  }
}

function gateHref(gate) {
  const id = gate.gate_id || gate.path;
  return `/gate?gate=${encodeURIComponent(id)}`;
}

async function loadStatus() {
  const query = new URLSearchParams();
  const packageValue = packageInput.value.trim();
  const limitInput = document.getElementById("limit-input");
  const limitValue = (limitInput ? limitInput.value : (urlParam("limit") || initial.limit || 5)).toString().trim();
  if (packageValue) query.set("package", packageValue);
  if (limitValue) query.set("limit", limitValue);
  syncUrlState(packageValue, limitValue);
  document.getElementById("status").innerHTML = '<section class="span-12">Loading...</section>';
  const response = await fetch(`/api/status?${query.toString()}`);
  const payload = await response.json();
  if (!response.ok) {
    document.getElementById("status").innerHTML = `<section><div class="error">${esc(payload.error || response.statusText)}</div></section>`;
    return;
  }
  renderStatus(payload);
  await loadNextAction(packageValue || (payload.status?.package?.package || ""));
}

async function rerunValidation() {
  const packageValue = packageInput.value.trim();
  const output = actionOutput();
  showCockpitTab("diagnostics");
  output.innerHTML = '<section>Running contract scan...</section>';
  const response = await fetch("/api/validate", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({package: packageValue || null})
  });
  const payload = await response.json();
  await loadStatus();
  showCockpitTab("diagnostics");
  actionOutput().innerHTML = renderValidationActionResult(payload, response.ok);
}

async function runEditorialReport() {
  const packageValue = packageInput.value.trim();
  const output = actionOutput();
  showCockpitTab("diagnostics");
  if (!packageValue) {
    output.innerHTML = '<section><div class="error">Select a package before running the editorial report.</div></section>';
    return;
  }
  output.innerHTML = '<section>Running editorial report...</section>';
  const response = await fetch("/api/editorial-report", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({package: packageValue})
  });
  const payload = await response.json();
  output.innerHTML = renderEditorialReportResult(payload, response.ok);
}

function commandStdout(payload) {
  return payload && payload.stdout && typeof payload.stdout === "object" ? payload.stdout : null;
}

function renderValidationActionResult(payload, ok) {
  const report = commandStdout(payload);
  const allFindings = report?.findings || [];
  const counts = allFindings.reduce((acc, finding) => {
    const severity = finding.severity || "info";
    acc[severity] = (acc[severity] || 0) + 1;
    return acc;
  }, {});
  const visibleFindings = allFindings.slice(0, 8);
  const findings = visibleFindings.map((finding) => `
    <tr>
      <td>${badge(finding.severity || "info")}</td>
      <td>${esc(finding.workflow_id || "")}</td>
      <td>${esc(finding.surface || "")}</td>
      <td>${artifact(finding.path, finding.path || "")}</td>
      <td>${esc(finding.message || "")}</td>
      <td>${esc(explainFinding(finding).action)}</td>
    </tr>`).join("");
  if (!report) {
    return `<section>
      <h2>Contract Scan</h2>
      <div class="callout bad">The scan did not return a structured validation report.</div>
      <details class="advanced"><summary>Raw command result</summary><pre>${esc(JSON.stringify(payload, null, 2))}</pre></details>
    </section>`;
  }
  return `<section>
    <h2>Contract Scan</h2>
    <div class="${allFindings.length ? "callout warn" : "callout"}">
      <strong>${allFindings.length ? badge("follow-up") : badge("pass")} Background architecture scan.</strong>
      This is not the active gate verdict and it does not block the visible Next Step unless a finding explicitly names the selected route.
      Found ${esc(allFindings.length)} findings: ${esc(counts.error || 0)} errors, ${esc(counts.warning || 0)} warnings.
    </div>
    <details class="advanced">
      <summary>Findings (${esc(allFindings.length)} total, showing ${esc(visibleFindings.length)})</summary>
      <table style="margin-top:12px">
        <thead><tr><th>Severity</th><th>Workflow</th><th>Surface</th><th>Path</th><th>Message</th><th>What to do</th></tr></thead>
        <tbody>${findings || '<tr><td colspan="6" class="muted">No findings.</td></tr>'}</tbody>
      </table>
    </details>
    <details class="advanced"><summary>Raw JSON</summary><pre>${esc(JSON.stringify(payload, null, 2))}</pre></details>
  </section>`;
}

function renderEditorialReportResult(payload, ok) {
  const report = commandStdout(payload);
  if (!ok || !report || report.kind !== "editorial_automation_report") {
    const message = payload.stderr || (typeof payload.stdout === "string" ? payload.stdout : payload.error) || "Editorial report is not available for this package.";
    return `<section>
      <h2>Editorial Report</h2>
      <div class="callout warn">
        The editorial report could not produce a structured package report. This usually means the selected package is not a leaf/live-draft package or is missing editorial inputs such as <code>config.markdown_path</code>.
      </div>
      <table><tbody>
        <tr><th>Selected package</th><td>${esc(packageInput.value.trim() || "none")}</td></tr>
        <tr><th>Command status</th><td>${badge(ok ? "completed" : "failed")}</td></tr>
        <tr><th>Message</th><td>${esc(message)}</td></tr>
        <tr><th>What to do</th><td>Use this only on a package with a live draft. For the current umbrella gate, use Operator Brief instead.</td></tr>
      </tbody></table>
      <details class="advanced"><summary>Raw command result</summary><pre>${esc(JSON.stringify(payload, null, 2))}</pre></details>
    </section>`;
  }
  const counts = report.severity_counts || {};
  const findings = (report.findings || []).slice(0, 12).map((finding) => `
    <tr>
      <td>${badge(finding.severity || "advisory")}</td>
      <td>${esc(finding.check_id || "")}</td>
      <td>${artifact(finding.path, finding.line ? `${finding.path}:${finding.line}` : finding.path)}</td>
      <td>${esc(finding.message || "")}</td>
    </tr>`).join("");
  const suggestions = renderListItems((report.source_improvement_suggestions || []).map((item) => item.suggestion || item.id));
  return `<section>
    <h2>Editorial Report</h2>
    <table><tbody>
      <tr><th>Package</th><td>${esc(report.package?.key || "")}</td></tr>
      <tr><th>Live draft</th><td>${artifact(report.package?.live_draft_path)}</td></tr>
      <tr><th>Counts</th><td>${esc(counts.error || 0)} errors, ${esc(counts.warning || 0)} warnings, ${esc(counts.advisory || 0)} advisory</td></tr>
      <tr><th>State effects</th><td><code>${esc(JSON.stringify(report.state_effects || {}))}</code></td></tr>
    </tbody></table>
    <h2 style="margin-top:14px">Findings</h2>
    <table>
      <thead><tr><th>Severity</th><th>Check</th><th>Path</th><th>Message</th></tr></thead>
      <tbody>${findings || '<tr><td colspan="4" class="muted">No findings.</td></tr>'}</tbody>
    </table>
    <h2 style="margin-top:14px">Source Improvement Suggestions</h2>
    <ul class="path-list">${suggestions || '<li class="muted">none</li>'}</ul>
    <details class="advanced"><summary>Raw report</summary><pre>${esc(JSON.stringify(report, null, 2))}</pre></details>
  </section>`;
}

function renderStatus(payload) {
  const report = payload.status || {};
  currentStatusReport = report;
  const gates = report.review_gates || {};
  const runs = report.recent_runs || {};
  const health = report.validation_health || {};
  const root = report.root_surfaces || {};
  const yamlRuns = runs.yaml_run_records || [];
  const legacyRuns = runs.legacy_json_logs || [];
  const packageLabel = report.package?.package || "all packages";
  const contractScanState = health.success === true ? "pass" : "follow-up";
  const currentRouteState = routeHealthFromRuns(report, legacyRuns);
  configureToolbarForPackage(report.package);
  const summary = `
    <div class="summary">
      <div class="metric"><div class="label">Package</div><div class="value">${esc(packageLabel)}</div></div>
      <div class="metric"><div class="label">Current flow</div><div class="value">${badge(currentRouteState.label)}</div></div>
      <div class="metric"><div class="label">Background scan</div><div class="value">${badge(contractScanState)}</div></div>
      <div class="metric"><div class="label">Review gate files</div><div class="value">${esc(gates.pending_count || 0)} pending</div></div>
      <div class="metric"><div class="label">Recent runs</div><div class="value">${esc(yamlRuns.length + legacyRuns.length)}</div></div>
    </div>`;
  document.getElementById("status").innerHTML = `
    <div class="tabs" role="tablist" aria-label="Cockpit sections">
      <button class="tab-button" type="button" data-tab="workflow-map" onclick="showCockpitTab('workflow-map')">Workflow Map</button>
      <button class="tab-button" type="button" data-tab="wizard" onclick="showCockpitTab('wizard')">Wizard</button>
      <button class="tab-button" type="button" data-tab="gates" onclick="showCockpitTab('gates')">Gates</button>
      <button class="tab-button" type="button" data-tab="diagnostics" onclick="showCockpitTab('diagnostics')">Diagnostics</button>
    </div>
    <div class="grid">
      <div class="span-12 tab-panel" data-tab="workflow-map">
        <section id="workflow-map-section"><h2>Workflow Map</h2><p class="muted">Resolving...</p></section>
      </div>
      <div class="span-12 tab-panel" data-tab="wizard" hidden>
        <section class="primary-section" id="next-action-section">${renderNextPlaceholder(report.package)}</section>
      </div>
      <div class="span-12 tab-panel" data-tab="gates" hidden>
        <section id="gate-readiness-section"><h2>Gate Readiness</h2><p class="muted">Resolving...</p></section>
        <section>${renderGates(gates)}</section>
      </div>
      <div class="span-12 tab-panel" data-tab="diagnostics" hidden>
        <section>${renderDiagnosticsControls()}</section>
        <div id="diagnostic-action-output" class="stack"></div>
        <section id="routing-diagnostics-section"><h2>Routing Diagnostics</h2><p class="muted">Resolving...</p></section>
        <section>${renderCollapsed("Package context", renderFlowContext(report))}</section>
        <section>${renderCollapsed("Dashboard metrics", summary)}</section>
        <section>${renderCollapsed("Package details", renderPackage(report.package, root))}</section>
        <section>${renderCollapsed("Recent run records", renderRuns(yamlRuns, legacyRuns))}</section>
        <section>${renderCollapsed("Background contract scan", renderValidation(health))}</section>
      </div>
    </div>`;
  configureToolbarForPackage(report.package);
  showCockpitTab(urlParam("tab") || activeCockpitTab || "workflow-map");
}

function renderDiagnosticsControls() {
  const limitValue = urlParam("limit") || initial.limit || 5;
  return `<h2>Diagnostics Controls</h2>
    <div class="toolbar">
      <label for="limit-input">Recent limit
        <input id="limit-input" type="number" min="1" max="50" value="${esc(limitValue)}" title="How many recent run records to show. It does not change package state.">
      </label>
      <button id="validate-button" type="button" onclick="rerunValidation()" title="Run the broad workflow-contract scan. This is architecture feedback, not the active gate verdict.">Contract Scan</button>
      <button id="editorial-report-button" type="button" onclick="runEditorialReport()" title="Run the report-only editorial scan. Most useful for leaf packages with a live draft.">Editorial Report</button>
    </div>`;
}

function renderFlowContext(report) {
  const pkg = report.package || {};
  const route = pkg.umbrella_route || {};
  if (pkg.kind === "umbrella") {
    const successor = route.active_successor_leaf;
    const switchButton = successor
      ? `<button type="button" onclick="switchToPackage('${esc(successor)}')">Open successor leaf</button>`
      : "";
    return `<h2>Why this is the next step</h2>
      <div class="callout">
        <strong>Viewing umbrella package.</strong>
        This screen is the parent container for donor history, pivot evidence, and successor routing.
        ${successor ? "The successor leaf already exists; continue the work there." : "No successor leaf is initialized yet."}
      </div>
      <div class="flow-steps">
        <div class="flow-step"><strong>1. Parent context</strong>Use this umbrella only to understand the pivot route and parent evidence.</div>
        <div class="flow-step"><strong>2. Working package</strong>${successor ? "Open the successor leaf and continue there." : "Initialize or approve the successor leaf before drafting."}</div>
        <div class="flow-step"><strong>3. Diagnostics</strong>Treat background scan findings as architecture cleanup unless the active Next Step names them as blockers.</div>
      </div>
      <details class="advanced">
        <summary>Route context</summary>
        <table style="margin-top:12px"><tbody>
        <tr><th>Active candidate</th><td>${esc(route.active_candidate || "none")}</td></tr>
        <tr><th>Donor leaf</th><td>${esc(route.donor_leaf || "none")}</td></tr>
        <tr><th>Successor leaf</th><td>${esc(successor || "not initialized")}</td></tr>
        <tr><th>Umbrella next action</th><td>${esc(route.next_action || "none")}</td></tr>
        </tbody></table>
      </details>`;
  }
  const parent = pkg.package && pkg.package.includes("/") ? pkg.package.split("/").slice(0, -1).join("/") : "";
  const handoffPath = packageStatusPath(pkg.package, "research-handoff.md");
  return `<h2>Why this is the next step</h2>
    <div class="callout warn">
      <strong>Viewing leaf package.</strong>
      This is the working object. The current job is to make the research stage runnable, not to draft or publish.
    </div>
    <div class="flow-steps">
      <div class="flow-step"><strong>1. Read handoff</strong>Open the research handoff and status file from the Next Step card.</div>
      <div class="flow-step"><strong>2. Define question</strong>Fill the current research question or thesis direction in the leaf package state.</div>
      <div class="flow-step"><strong>3. Recheck route</strong>Return to this cockpit after the research setup exists.</div>
    </div>
    <details class="advanced">
      <summary>Leaf context</summary>
      <table style="margin-top:12px"><tbody>
        <tr><th>Parent umbrella</th><td>${parent ? `<button type="button" onclick="switchToPackage('${esc(parent)}')">Open ${esc(parent)}</button>` : '<span class="muted">none</span>'}</td></tr>
        <tr><th>Research handoff</th><td>${artifact(handoffPath)}</td></tr>
        <tr><th>Current stage</th><td>${esc(pkg.current_stage || "none")}</td></tr>
      </tbody></table>
    </details>`;
}

function configureToolbarForPackage(pkg) {
  const editorialButton = document.getElementById("editorial-report-button");
  if (!editorialButton) return;
  const isLeaf = pkg && pkg.kind !== "umbrella";
  const stage = pkg?.current_stage || "";
  const isDraftStage = isLeaf && !["", "paper_intake", "research"].includes(stage);
  editorialButton.disabled = !isDraftStage;
  editorialButton.textContent = isDraftStage ? "Editorial Report" : "Editorial Report (draft only)";
  editorialButton.title = isDraftStage
    ? "Run the report-only editorial scan for this live-draft package."
    : "Disabled until the selected leaf has a live draft/editorial stage. Use research handoff/status links for this package.";
}

function routeHealthFromRuns(report, legacyRuns) {
  const pkg = report.package || {};
  if (pkg.kind === "leaf" && pkg.current_stage === "research") {
    return {label: "needs research setup"};
  }
  const route = report.package?.umbrella_route || {};
  if (route.active_workflow === "post_ceiling_pivot") {
    const groundingPass = (legacyRuns || []).some((run) => run.gate_id === "pivot_research_grounding" && run.status === "pass");
    const northStarPass = (legacyRuns || []).some((run) => run.gate_id === "pivot_north_star_viability" && run.status === "pass");
    if (groundingPass && northStarPass) return {label: "route passed"};
    if (groundingPass || northStarPass) return {label: "partial"};
  }
  return {label: "unknown"};
}

function renderNextPlaceholder(pkg) {
  if (!pkg) {
    return '<h2>Next Action</h2><p class="muted">Select a package to resolve the next action.</p>';
  }
  return '<h2>Next Action</h2><p class="muted">Resolving...</p>';
}

async function loadNextAction(packageValue) {
  const section = document.getElementById("next-action-section");
  if (!section || !packageValue) return;
  const response = await fetch(`/api/next?package=${encodeURIComponent(packageValue)}`);
  const payload = await response.json();
  if (!response.ok) {
    section.innerHTML = `<h2>Next Action</h2><div class="error">${esc(payload.error || response.statusText)}</div>`;
    return;
  }
  const next = payload.next || {};
  currentNextReport = next;
  currentWorkflowMap = next.cockpit_view_model?.workflow_map || {};
  const workflowMapSection = document.getElementById("workflow-map-section");
  if (workflowMapSection) workflowMapSection.innerHTML = renderWorkflowMap(currentWorkflowMap);
  section.innerHTML = renderNextAction(next);
  const gateSection = document.getElementById("gate-readiness-section");
  if (gateSection) gateSection.innerHTML = renderGateReadinessTab(next);
  const diagnosticsSection = document.getElementById("routing-diagnostics-section");
  if (diagnosticsSection) diagnosticsSection.innerHTML = renderRoutingDiagnostics(next);
}

function renderListItems(items) {
  return (items || []).map((item) => `<li>${esc(item)}</li>`).join("");
}

function renderInlineList(items) {
  const values = items || [];
  return values.length ? values.map((item) => `<li>${esc(item)}</li>`).join("") : '<li class="muted">none</li>';
}

function deriveStepState(step) {
  return step?.state || "inferred";
}

function setWorkflowMapMode(mode) {
  workflowMapMode = mode;
  selectedWorkflowId = "";
  selectedWorkflowStepId = "";
  const body = document.getElementById("workflow-map-body");
  if (body && currentWorkflowMap) body.innerHTML = renderWorkflowMapBody(currentWorkflowMap);
  const wizard = document.getElementById("next-action-section");
  if (wizard && currentNextReport) wizard.innerHTML = renderNextAction(currentNextReport);
  for (const button of document.querySelectorAll(".workflow-mode-button")) {
    button.classList.toggle("active", button.dataset.mode === workflowMapMode);
  }
  updateUrlFromState();
}

function setWorkflowStepFilter(filter) {
  workflowStepFilter = filter;
  const body = document.getElementById("workflow-map-body");
  if (body && currentWorkflowMap) body.innerHTML = renderWorkflowMapBody(currentWorkflowMap);
  for (const button of document.querySelectorAll(".workflow-filter-button")) {
    button.classList.toggle("active", button.dataset.filter === workflowStepFilter);
  }
  updateUrlFromState();
}

function workflowStepMatchesFilter(step) {
  const state = deriveStepState(step);
  if (workflowStepFilter === "current_blocked") return step.is_current || state === "blocked" || state === "current";
  if (workflowStepFilter === "runnable") return state === "available" && !["codex_session", "external_mutation_gated"].includes(step.mode);
  if (workflowStepFilter === "gated") return Boolean(step.gate_id) || String(step.mode || "").includes("gated");
  return true;
}

function renderWorkflowMap(map) {
  currentWorkflowMap = map || {};
  workflowMapMode = urlParam("mode") || workflowMapMode || currentWorkflowMap.default_mode || "active_route";
  workflowStepFilter = urlParam("filter") || workflowStepFilter || currentWorkflowMap.default_filter || "all";
  return `<h2>Workflow Map</h2>
    <p class="muted">Sequential workflow steps derived from workflow.yaml and package state. This is an operator map, not workflow authority.</p>
    ${renderLifecycleStatusSummary()}
    <div class="workflow-map-controls">
      <button class="workflow-mode-button ${workflowMapMode === "active_route" ? "active" : ""}" type="button" data-mode="active_route" onclick="setWorkflowMapMode('active_route')">Active route</button>
      <button class="workflow-mode-button ${workflowMapMode === "all_workflows" ? "active" : ""}" type="button" data-mode="all_workflows" onclick="setWorkflowMapMode('all_workflows')">All workflows</button>
      <span class="muted">Filter</span>
      <button class="workflow-filter-button ${workflowStepFilter === "all" ? "active" : ""}" type="button" data-filter="all" onclick="setWorkflowStepFilter('all')">All</button>
      <button class="workflow-filter-button ${workflowStepFilter === "current_blocked" ? "active" : ""}" type="button" data-filter="current_blocked" onclick="setWorkflowStepFilter('current_blocked')">Current/blocked</button>
      <button class="workflow-filter-button ${workflowStepFilter === "runnable" ? "active" : ""}" type="button" data-filter="runnable" onclick="setWorkflowStepFilter('runnable')">Runnable</button>
      <button class="workflow-filter-button ${workflowStepFilter === "gated" ? "active" : ""}" type="button" data-filter="gated" onclick="setWorkflowStepFilter('gated')">Gated</button>
    </div>
    <div id="workflow-map-body">${renderWorkflowMapBody(currentWorkflowMap)}</div>`;
}

function stageLabel(stage) {
  return String(stage || "none").replaceAll("_", " ");
}

function renderStagePills(stages, currentStage) {
  return (stages || []).map((stage) => {
    const id = stage.stage || "";
    const state = stage.done === true ? "completed" : (id === currentStage ? "current" : "pending");
    const date = stage.last_updated ? ` · ${esc(stage.last_updated)}` : "";
    return `<span class="stage-pill ${esc(state)}">${badge(state)} ${esc(stageLabel(id))}${date}</span>`;
  }).join("");
}

function renderLifecycleStatusSummary() {
  const pkg = currentStatusReport?.package || {};
  const stages = pkg.stages || [];
  if (!stages.length) return "";
  const currentStage = currentNextReport?.next_stage || pkg.current_stage || "";
  const completed = stages.filter((stage) => stage.done === true);
  const remaining = stages.filter((stage) => stage.done !== true);
  const blockers = currentNextReport?.blocking_issues || [];
  const missingContext = (currentNextReport?.required_context || []).filter((item) => item.status === "missing" || item.blocking === true);
  return `<div class="route-summary">
    <div class="summary">
      <div class="metric"><div class="label">Completed</div><div class="value">${esc(completed.length)} / ${esc(stages.length)}</div></div>
      <div class="metric"><div class="label">Current stage</div><div class="value">${esc(stageLabel(currentStage || "none"))}</div></div>
      <div class="metric"><div class="label">Next workflow</div><div class="value">${esc(stageLabel(currentNextReport?.effective_workflow || currentStage || "none"))}</div></div>
      <div class="metric"><div class="label">Missing context</div><div class="value">${esc(missingContext.length)}</div></div>
      <div class="metric"><div class="label">Blockers</div><div class="value">${esc(blockers.length)}</div></div>
    </div>
    <div class="stage-pills">${renderStagePills(stages, currentStage)}</div>
    <div class="muted" style="margin-top:8px">Done: ${esc(completed.map((stage) => stageLabel(stage.stage)).join(", ") || "none")}. Left: ${esc(remaining.map((stage) => stageLabel(stage.stage)).join(", ") || "none")}.</div>
  </div>`;
}

function renderWorkflowMapBody(map) {
  const mode = map?.modes?.[workflowMapMode] || map?.modes?.active_route || {};
  const workflows = mode.workflows || [];
  const sections = workflowMapMode === "all_workflows"
    ? renderLifecycleWorkflowColumns(workflows)
    : workflows.map((workflow) => renderWorkflowSection(workflow)).join("");
  const empty = '<div class="callout warn">No workflow steps matched this mode/filter.</div>';
  const selected = selectedWorkflowId && selectedWorkflowStepId ? findWorkflowStep(selectedWorkflowId, selectedWorkflowStepId) : {};
  const selectedDetails = selected.step ? renderStepDetails(selected.workflow, selected.step) : "";
  return `<div class="callout">
      <strong>${esc(mode.label || "Workflow map")}</strong>
      <div class="muted" style="margin-top:4px">${esc(mode.description || "")}</div>
    </div>
    ${sections || empty}
    <div id="workflow-step-details" class="workflow-detail"${selectedDetails ? "" : " hidden"}>${selectedDetails}</div>`;
}

function workflowLifecycleLane(workflow) {
  const id = String(workflow.id || "").replaceAll("-", "_");
  if (id.includes("topic")) return "Discovery";
  if (id === "research" || id.includes("alphaxiv")) return "Research";
  if (id.includes("paper_intake") || id.includes("evidence")) return "Evidence";
  if (id.includes("essay")) return "Drafting";
  if (id.includes("notebooklm") || id.includes("youtube_production")) return "Artifacts";
  if (id.includes("article_polish") || id.includes("release")) return "Polish";
  if (id.includes("substack") && !id.includes("archive")) return "Publishing";
  if (id.includes("distribution")) return "Distribution";
  return "Maintenance";
}

function renderLifecycleWorkflowColumns(workflows) {
  const laneNames = ["Discovery", "Research", "Evidence", "Drafting", "Artifacts", "Polish", "Publishing", "Distribution", "Maintenance"];
  const lanes = Object.fromEntries(laneNames.map((name) => [name, []]));
  for (const workflow of workflows) {
    const rendered = renderWorkflowSection(workflow);
    if (!rendered) continue;
    lanes[workflowLifecycleLane(workflow)].push(rendered);
  }
  const columns = laneNames.map((name) => `<div class="lifecycle-lane">
    <h3>${esc(name)}</h3>
    ${lanes[name].join("") || '<p class="muted">No matching workflows.</p>'}
  </div>`).join("");
  return `<div class="lifecycle-columns">${columns}</div>`;
}

function renderWorkflowSection(workflow) {
  const steps = (workflow.steps || []).filter(workflowStepMatchesFilter);
  if (!steps.length) return "";
  const stepCards = steps.map((step) => renderWorkflowStep(workflow, step)).join("");
  const meta = [workflow.workflow_kind, workflow.workflow_group, workflow.stability].filter(Boolean).join(" · ");
  return `<div class="workflow-section">
    <div class="workflow-section-head">
      <div>
        <h3 style="margin:0">${esc(workflow.id || "workflow")}${workflow.is_active ? ` ${badge("current")}` : ""}</h3>
        <div class="muted" style="margin-top:4px">${esc(meta || "workflow")}</div>
        <div class="muted" style="margin-top:4px">${esc(workflow.summary || "")}</div>
      </div>
      <div>${artifact(workflow.path, "workflow.yaml")}</div>
    </div>
    <div class="workflow-step-grid">${stepCards}</div>
  </div>`;
}

function renderWorkflowStep(workflow, step) {
  const state = deriveStepState(step);
  const actionText = step.action ? `${esc(step.action).slice(0, 180)}${String(step.action).length > 180 ? "..." : ""}` : "No action summary.";
  return `<button class="workflow-step ${esc(state)} ${step.is_current ? "current" : ""}" type="button" onclick="openWorkflowStep('${esc(workflow.id)}', '${esc(step.id)}')">
    <div class="workflow-step-meta">${badge(state)} ${step.gate_id ? badge(`gate:${step.gate_id}`) : ""}</div>
    <div class="workflow-step-title">${esc(step.title || step.id)}</div>
    <div class="muted">${esc(step.id || "")} · ${esc(step.mode || "unknown")}</div>
    <div>${actionText}</div>
  </button>`;
}

function findWorkflowStep(workflowId, stepId) {
  const mode = currentWorkflowMap?.modes?.[workflowMapMode] || {};
  for (const workflow of mode.workflows || []) {
    if (workflow.id !== workflowId) continue;
    for (const step of workflow.steps || []) {
      if (step.id === stepId) return {workflow, step};
    }
  }
  return {};
}

function openWorkflowStep(workflowId, stepId) {
  selectedWorkflowId = workflowId;
  selectedWorkflowStepId = stepId;
  const match = findWorkflowStep(workflowId, stepId);
  const details = document.getElementById("workflow-step-details");
  if (!details || !match.step) return;
  details.hidden = false;
  details.innerHTML = renderStepDetails(match.workflow, match.step);
  const wizard = document.getElementById("next-action-section");
  if (wizard && currentNextReport) wizard.innerHTML = renderNextAction(currentNextReport);
  updateUrlFromState();
  details.scrollIntoView({behavior: "smooth", block: "nearest"});
}

function renderStepDetails(workflow, step) {
  const enabled = step.actions?.enabled || [];
  const disabled = step.actions?.disabled || [];
  const enabledButtons = enabled.map((action) => {
    if (action.id === "wizard") return '<button type="button" onclick="showCockpitTab(\\'wizard\\')">Open in Wizard</button>';
    if (action.id === "gates") return '<button type="button" onclick="showCockpitTab(\\'gates\\')">Open Gates</button>';
    if (action.id === "diagnostics") return '<button type="button" onclick="showCockpitTab(\\'diagnostics\\')">Open Diagnostics</button>';
    if (action.id === "copy_instruction") return `<button type="button" data-instruction="${esc(action.instruction || step.instruction || "")}" onclick="copyWorkflowInstruction(this)">Copy Codex instruction</button>`;
    if (action.id === "prepare_template") return `<button type="button" onclick="submitWorkflowTemplate('${esc(action.workflow || workflow.id)}', '${esc(action.step || step.id)}')">Prepare research-exit templates</button>`;
    return "";
  }).join("");
  const disabledButtons = disabled.map((action) => `<span class="disabled-action">
    <button type="button" disabled>${esc(action.label)}</button>
    <small>${esc(action.reason)}</small>
  </span>`).join("");
  return `<div class="workflow-section-head">
      <div>
        <h3 style="margin:0">${esc(step.title || step.id)}</h3>
        <div class="muted" style="margin-top:4px">${esc(workflow.id)} · ${esc(step.id)} · ${esc(step.mode)}</div>
      </div>
      <div>${badge(deriveStepState(step))}</div>
    </div>
    <div class="callout" style="margin-top:10px">
      <strong>Why this state?</strong>
      <div class="muted" style="margin-top:4px">${esc(step.state_reason || "Derived from workflow.yaml and current package state.")}</div>
    </div>
    <p>${esc(step.action || "No action summary.")}</p>
    <table><tbody>
      <tr><th>Consumes</th><td><ul class="path-list">${renderInlineList(step.consumes)}</ul></td></tr>
      <tr><th>Produces</th><td><ul class="path-list">${renderInlineList(step.produces)}</ul></td></tr>
      <tr><th>Validation hooks</th><td><ul class="path-list">${renderInlineList(step.validation_hooks)}</ul></td></tr>
      <tr><th>Missing artifacts</th><td><ul class="path-list">${renderInlineList(step.missing_artifacts)}</ul></td></tr>
      <tr><th>Gate</th><td>${esc(step.gate_id || "none")}</td></tr>
      <tr><th>Executor</th><td>${esc(step.executor_command || "not directly executable from cockpit v1")}</td></tr>
    </tbody></table>
    <div class="toolbar" style="margin-top:12px">${enabledButtons}</div>
    <div style="margin-top:8px">${disabledButtons}</div>
    <div id="workflow-step-copy-result" class="muted" style="margin-top:8px"></div>`;
}

async function copyWorkflowInstruction(button) {
  const instruction = button.dataset.instruction || "";
  if (!instruction) return;
  await navigator.clipboard.writeText(instruction);
  const result = document.getElementById("workflow-step-copy-result");
  if (result) result.textContent = "Codex instruction copied.";
}

async function submitWorkflowTemplate(workflow, step) {
  const result = document.getElementById("workflow-step-copy-result") || actionOutput();
  result.textContent = "Preparing deterministic template artifacts...";
  const response = await fetch("/api/workflow-template", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({package: packageInput.value.trim(), workflow, step})
  });
  const payload = await response.json();
  if (!response.ok) {
    result.innerHTML = `<span class="error">${esc(payload.error || response.statusText)}</span>`;
    return;
  }
  const created = (payload.created_paths || []).map((path) => `<li>${artifact(path, path)}</li>`).join("");
  const skipped = (payload.skipped_existing_paths || []).map((path) => `<li>${artifact(path, path)}</li>`).join("");
  result.innerHTML = `<div class="callout">
    <strong>${esc(payload.message || "Template action complete.")}</strong>
    <div style="margin-top:8px"><strong>Created</strong><ul class="path-list">${created || '<li class="muted">none</li>'}</ul></div>
    <div style="margin-top:8px"><strong>Already existed</strong><ul class="path-list">${skipped || '<li class="muted">none</li>'}</ul></div>
  </div>`;
  await loadStatus();
}

const defaultResearchQuestions = {
  "literate-workflow-programming/specification-surface-source-of-truth": "How do controlled, typed, linted, validated, and trace-linked specification surfaces become the governed source-of-truth artifact in AI-assisted software work, and why is this different from treating natural language prompts as code?"
};

async function submitResearchQuestion() {
  const input = document.getElementById("research-question-input");
  const output = document.getElementById("research-question-result") || document.getElementById("action-output");
  const packageValue = packageInput.value.trim();
  const researchQuestion = input ? input.value.trim() : "";
  if (!researchQuestion) {
    output.innerHTML = '<div class="callout bad">Research question is required.</div>';
    return;
  }
  output.innerHTML = '<div class="callout">Saving research question...</div>';
  const response = await fetch("/api/research-question", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      package: packageValue,
      research_question: researchQuestion
    })
  });
  const payload = await response.json();
  output.innerHTML = `
    <div class="${response.ok ? "callout" : "callout bad"}">${esc(payload.message || payload.error || "Research question action completed.")}</div>
    <details class="advanced"><summary>Action result</summary><pre>${esc(JSON.stringify(payload, null, 2))}</pre></details>
  `;
  if (response.ok) await loadStatus();
}

function updateNextExecuteButton() {
  const checkbox = document.getElementById("next-execute-approved");
  const button = document.getElementById("next-execute-button");
  if (!button) return;
  button.disabled = !(checkbox && checkbox.checked);
}

async function executeNextStep() {
  const checkbox = document.getElementById("next-execute-approved");
  const output = document.getElementById("next-execute-result") || document.getElementById("action-output");
  const packageValue = packageInput.value.trim();
  if (!checkbox || !checkbox.checked) {
    output.innerHTML = '<div class="callout bad">Approve the local execution checkbox first.</div>';
    return;
  }
  const ok = window.confirm(`Generate the guided research-stage launch pack for ${packageValue}? This may write local reviewable-run artifacts, but it will not publish or send anything externally.`);
  if (!ok) return;
  output.innerHTML = '<div class="callout">Executing next step: generating launch pack...</div>';
  const response = await fetch("/api/next/execute", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      package: packageValue,
      approved: true
    })
  });
  const payload = await response.json();
  output.innerHTML = `
    <div class="${response.ok ? "callout" : "callout bad"}">${esc(payload.message || payload.error || "Next-step execution completed.")}</div>
    <details class="advanced"><summary>Execution result</summary><pre>${esc(JSON.stringify(payload, null, 2))}</pre></details>
  `;
  await loadStatus();
}

async function copyCodexInstruction() {
  const input = document.getElementById("codex-next-instruction");
  const result = document.getElementById("codex-next-instruction-result");
  if (!input) return;
  input.select();
  try {
    await navigator.clipboard.writeText(input.value);
    if (result) result.innerHTML = '<div class="callout">Instruction copied.</div>';
  } catch (error) {
    if (result) result.innerHTML = '<div class="callout warn">Select the text and copy it manually.</div>';
  }
}

function explainBlocker(message, next) {
  const text = String(message || "");
  if (text.includes("Runner mode 'guided'") && text.includes("launch_mode 'none'")) {
    return {
      meaning: "The workflow is intentionally guided. The dashboard can show the next action and record approval, but it cannot automatically perform the package edit.",
      action: "Emit a launch pack or have Codex perform the guided research-stage file work."
    };
  }
  if (text.includes("Missing required context:")) {
    const missing = text.split("Missing required context:").pop().trim();
    return {
      meaning: "The workflow.yaml contract names this context as required, and the package state has not resolved it yet.",
      action: `Provide ${missing || "the missing context"} before trying to run this workflow.`
    };
  }
  if (text.includes("Gate 'research_exit' is blocked")) {
    return {
      meaning: "The research question is now admitted, but the leaf does not yet have the research-exit gate artifact and claim-boundary surface required to leave research.",
      action: "Prepare the research-exit gate packet before trying to draft."
    };
  }
  if (text.includes("Pending review gate blocks governed progress")) {
    return {
      meaning: "A file-backed review gate is waiting for approve, reject, or defer.",
      action: "Open the gate from Review Gates and record a decision."
    };
  }
  if (next?.effective_requires_approval === true || next?.requires_approval === true) {
    return {
      meaning: "The next action crosses a governed approval boundary.",
      action: "Record approval only if the displayed workflow, action, and gate match what you intend."
    };
  }
  return {
    meaning: "The runner cannot continue until this condition is resolved.",
    action: "Use the suggested command or inspect the linked workflow/status artifact."
  };
}

function renderBlockers(blockingIssues, next) {
  const rows = (blockingIssues || []).map((message) => {
    const explanation = explainBlocker(message, next);
    return `<tr>
      <td>${esc(message)}</td>
      <td>${esc(explanation.meaning)}</td>
      <td>${esc(explanation.action)}</td>
    </tr>`;
  }).join("");
  return `<table>
    <thead><tr><th>Raw issue</th><th>Meaning</th><th>What to do</th></tr></thead>
    <tbody>${rows || '<tr><td colspan="3" class="muted">No blocking issues.</td></tr>'}</tbody>
  </table>`;
}

function renderRequiredContextChecklist(next) {
  const items = next.required_context || [];
  if (!items.length) return "";
  const rows = items.map((item) => {
    const status = item.status || "unknown";
    const value = item.value === undefined || item.value === null ? "" : inlineValue(item.value);
    const blocking = item.blocking === true ? "blocking" : "supporting";
    return `<div class="check-row">
      <div>
        ${badge(status)}
        <div class="muted" style="margin-top:5px">${esc(blocking)}</div>
      </div>
      <div>
        <div class="name">${esc(item.name || "context")}</div>
        <div class="detail">${esc(value || "No value resolved yet.")}</div>
      </div>
    </div>`;
  }).join("");
  return `<h3>Required context from workflow.yaml</h3>
    <div class="checklist">${rows}</div>`;
}

function renderGateChecklist(next) {
  const gates = next.gate_statuses || {};
  const entries = Object.values(gates);
  if (!entries.length) return "";
  const rows = entries.map((gate) => {
    const missing = (gate.missing_artifacts || []).join(", ") || "none";
    const recommendation = gate.recommended_workflow || gate.recommended_validator || "none";
    return `<div class="check-row">
      <div>
        ${badge(gate.status || "unknown")}
        <div class="muted" style="margin-top:5px">${esc(gate.blocking ? "blocking" : "supporting")}</div>
      </div>
      <div>
        <div class="name">${esc(gate.gate_id || "gate")}</div>
        <div class="detail">Missing: ${esc(missing)}</div>
        <div class="detail">Recommended: ${esc(recommendation)}</div>
      </div>
    </div>`;
  }).join("");
  return `<h3>Gate readiness from status/workflow policy</h3>
    <div class="checklist">${rows}</div>`;
}

function renderGateReadinessTab(next) {
  return `<h2>Gate Readiness</h2>
    <div class="callout">This tab is for gate status, missing gate artifacts, validators, and review decisions. It is separate from the operational wizard.</div>
    ${renderGateChecklist(next) || '<p class="muted">No stage gate status is available for the selected package.</p>'}`;
}

function renderRoutingDiagnostics(next) {
  const canExecute = next.can_execute === true || next.effective_can_execute === true;
  const requiresApproval = next.requires_approval === true || next.effective_requires_approval === true;
  const approvalGate = next.approval_gate || next.effective_approval_gate || "none";
  const action = next.effective_next_action || next.next_overlay_action || next.next_packet_action || next.umbrella_route_next_action || "none";
  const workflow = next.effective_workflow || next.active_overlay || next.umbrella_route_workflow || next.next_stage || "none";
  const route = next.effective_route || next.umbrella_route_state || next.overlay_phase || "none";
  const validator = next.recommended_validator || next.overlay_recommended_validator || "none";
  const gateRows = renderGateBlockers(next.pending_review_gate_blockers || []);
  const commands = renderListItems(next.suggested_commands || []);
  return `<h2>Routing Diagnostics</h2>
    <table><tbody>
      <tr><th>Workflow</th><td>${esc(workflow)}</td></tr>
      <tr><th>Route / phase</th><td>${esc(route)}</td></tr>
      <tr><th>Next stage</th><td>${esc(next.next_stage || "none")}</td></tr>
      <tr><th>Next action</th><td>${esc(action)}</td></tr>
      <tr><th>Can execute</th><td>${badge(String(canExecute))}</td></tr>
      <tr><th>Requires approval</th><td>${badge(String(requiresApproval))}</td></tr>
      <tr><th>Approval gate</th><td>${esc(approvalGate)}</td></tr>
      <tr><th>Pipeline profile</th><td>${esc(next.pipeline_profile || "none")}</td></tr>
      <tr><th>Recommended validator</th><td><code>${esc(validator)}</code></td></tr>
    </tbody></table>
    <h2 style="margin-top:14px">Blocking Issues</h2>
    ${renderBlockers(next.blocking_issues || [], next)}
    <h2 style="margin-top:14px">Pending Gate Blockers</h2>
    <table>
      <thead><tr><th>Status</th><th>Gate</th><th>Workflow</th><th>Reason</th></tr></thead>
      <tbody>${gateRows || '<tr><td colspan="4" class="muted">No pending gate blockers.</td></tr>'}</tbody>
    </table>
    <h2 style="margin-top:14px">Suggested Commands</h2>
    <ul class="path-list">${commands || '<li class="muted">none</li>'}</ul>`;
}

function deriveBlockedAction(next) {
  const issues = next.blocking_issues || [];
  const gateStatuses = next.gate_statuses || {};
  if (gateStatuses.research_exit?.blocking || issues.some((issue) => String(issue).includes("research_exit"))) {
    return "prepare research-exit gate";
  }
  if (issues.some((issue) => String(issue).includes("Runner mode 'guided'"))) {
    return "emit guided launch pack";
  }
  return "resolve blocker";
}

function isResearchExitBlocked(next) {
  const gateStatuses = next.gate_statuses || {};
  const issues = next.blocking_issues || [];
  return Boolean(gateStatuses.research_exit?.blocking) || issues.some((issue) => String(issue).includes("research_exit"));
}

function renderNextExecutionPanel(next) {
  if (!isResearchExitBlocked(next)) return "";
  const wizard = next.cockpit_wizard || {};
  const launchPack = wizard.launch_pack || null;
  if (launchPack) {
    const instruction = wizard.next_instruction || "";
    return `<div class="approval-panel">
      <h3>Completed: guided handoff</h3>
      <p class="muted">The launch-pack step has already been completed. Generating it again will not clear the gate.</p>
      <table><tbody>
        <tr><th>Launch pack</th><td>${artifact(launchPack.path, launchPack.run_id || "Open launch pack")}</td></tr>
        <tr><th>Generated</th><td>${esc(launchPack.timestamp || "recorded")}</td></tr>
      </tbody></table>
      <h3 style="margin-top:14px">Next: nudge Codex to continue</h3>
      <p class="muted">The next substantive action is to create the missing research-exit gate artifact and claim-boundary surface.</p>
      <textarea id="codex-next-instruction" rows="3" readonly style="width:100%; padding:10px; border:1px solid var(--line); border-radius:6px; font:inherit;">${esc(instruction)}</textarea>
      <div class="toolbar" style="margin-top:10px">
        <button type="button" onclick="copyCodexInstruction()">Copy Codex instruction</button>
      </div>
      <div id="codex-next-instruction-result" style="margin-top:10px"></div>
    </div>`;
  }
  const packageValue = packageInput.value.trim();
  return `<div class="approval-panel">
    <h3>Next: nudge Codex to continue</h3>
    <p class="muted">The next substantive action is to create the missing research-exit gate artifact and claim-boundary surface. Handoff/log-only actions are kept out of the primary wizard path.</p>
    <textarea id="codex-next-instruction" rows="3" readonly style="width:100%; padding:10px; border:1px solid var(--line); border-radius:6px; font:inherit;">Create the research-exit gate artifact and claim-boundary surface for ${esc(packageValue)}.</textarea>
    <div class="toolbar" style="margin-top:10px">
      <button type="button" onclick="copyCodexInstruction()">Copy Codex instruction</button>
    </div>
    <div id="codex-next-instruction-result" style="margin-top:10px"></div>
  </div>`;
}

function renderVisibleBlockerPanel(next) {
  const issues = next.blocking_issues || [];
  if (!issues.length) return "";
  const commands = renderListItems(next.suggested_commands || []);
  return `<div class="approval-panel">
    <h3>Operator checklist</h3>
    ${renderRequiredContextChecklist(next)}
    ${renderGateChecklist(next)}
    <details class="advanced">
      <summary>Detailed blocker explanation</summary>
      <div style="margin-top:12px">${renderBlockers(issues, next)}</div>
    </details>
    <details class="advanced">
      <summary>Suggested commands</summary>
      <ul class="path-list">${commands || '<li class="muted">none</li>'}</ul>
    </details>
    ${renderNextExecutionPanel(next)}
  </div>`;
}

function renderApprovalBoundaryContext(next, stageLabel, workflowLabel, approvalGate) {
  const issues = next.blocking_issues || [];
  const contextChecklist = renderRequiredContextChecklist(next);
  const commands = renderListItems(next.suggested_commands || []);
  if (!issues.length && !contextChecklist && !commands) return "";
  return `<div class="approval-panel">
    <h3>Approval boundary context</h3>
    <p class="muted">This is the workflow state the operator should inspect before recording a boundary decision. Approval here records intent only; missing context still has to be supplied through the workflow.</p>
    <table><tbody>
      <tr><th>Stage</th><td>${esc(stageLabel)}</td></tr>
      <tr><th>Workflow</th><td>${esc(workflowLabel)}</td></tr>
      <tr><th>Approval gate</th><td>${esc(approvalGate)}</td></tr>
    </tbody></table>
    ${contextChecklist}
    <h3 style="margin-top:14px">Blocking issues</h3>
    ${renderBlockers(issues, next)}
    <details class="advanced">
      <summary>Suggested commands</summary>
      <ul class="path-list">${commands || '<li class="muted">none</li>'}</ul>
    </details>
  </div>`;
}

function renderGateBlockers(gates) {
  return (gates || []).map((gate) => `
    <tr>
      <td>${badge(gate.status)}</td>
      <td><a href="${gateHref(gate)}">${esc(gate.gate_id || gate.path)}</a></td>
      <td>${esc(gate.workflow_id || "")}</td>
      <td>${esc(gate.stop_reason || "")}</td>
    </tr>`).join("");
}

function selectedWorkflowStepMatch() {
  if (!selectedWorkflowId || !selectedWorkflowStepId || !currentWorkflowMap) return {};
  return findWorkflowStep(selectedWorkflowId, selectedWorkflowStepId);
}

function clearSelectedWorkflowStep() {
  selectedWorkflowId = "";
  selectedWorkflowStepId = "";
  updateUrlFromState();
  const wizard = document.getElementById("next-action-section");
  if (wizard && currentNextReport) wizard.innerHTML = renderNextAction(currentNextReport);
  const body = document.getElementById("workflow-map-body");
  if (body && currentWorkflowMap) body.innerHTML = renderWorkflowMapBody(currentWorkflowMap);
}

function renderSelectedStepWizard(next, workflow, step) {
  const gateStatuses = next.gate_statuses || {};
  const gate = step.gate_id ? gateStatuses[step.gate_id] : null;
  const missing = step.missing_artifacts || gate?.missing_artifacts || [];
  const enabled = step.actions?.enabled || [];
  const disabled = step.actions?.disabled || [];
  const prepareAction = enabled.find((action) => action.id === "prepare_template");
  const copyAction = enabled.find((action) => action.id === "copy_instruction");
  const gateCallout = gate
    ? `<div class="callout ${gate.blocking ? "bad" : ""}" style="margin-top:10px">
        <strong>Gate ${esc(step.gate_id)}: ${badge(gate.status || "unknown")}</strong>
        <div class="muted" style="margin-top:6px">${esc(gate.decision || gate.recommended_workflow || "Gate status is available in Gates.")}</div>
        <table style="margin-top:8px"><tbody>
          <tr><th>Missing artifacts</th><td><ul class="path-list">${renderInlineList(missing)}</ul></td></tr>
          <tr><th>Recommended workflow</th><td>${esc(gate.recommended_workflow || "none")}</td></tr>
          <tr><th>Recommended validator</th><td>${esc(gate.recommended_validator || "none")}</td></tr>
        </tbody></table>
      </div>`
    : "";
  const disabledRows = disabled.map((action) => `<span class="disabled-action">
    <button type="button" disabled>${esc(action.label)}</button>
    <small>${esc(action.reason)}</small>
  </span>`).join("");
  return `<div class="wizard-head">
      <div>
        <div class="wizard-kicker">Selected workflow step</div>
        <div class="wizard-title">${esc(step.title || step.id)}</div>
        <div class="muted" style="margin-top:4px">${esc(workflow.id)} · ${esc(step.id)} · ${esc(step.mode)}</div>
      </div>
      <div>${badge(deriveStepState(step))}</div>
    </div>
    <div class="callout">
      <strong>This Wizard is now focused on the selected Workflow Map step.</strong>
      <div class="muted" style="margin-top:6px">${esc(step.state_reason || "Derived from workflow.yaml and current package state.")}</div>
    </div>
    ${gateCallout}
    <section style="margin-top:12px">
      <h2>Immediate action</h2>
      <p>${esc(step.action || "No action summary.")}</p>
      <div class="toolbar" style="margin-top:10px">
        <button type="button" onclick="showCockpitTab('workflow-map')">Back to Workflow Map</button>
        ${step.gate_id ? '<button type="button" onclick="showCockpitTab(\\'gates\\')">Open Gates</button>' : ""}
        <button type="button" onclick="showCockpitTab('diagnostics')">Open Diagnostics</button>
        ${copyAction ? `<button type="button" data-instruction="${esc(copyAction.instruction || step.instruction || "")}" onclick="copyWorkflowInstruction(this)">Copy Codex instruction</button>` : ""}
        ${prepareAction ? `<button type="button" onclick="submitWorkflowTemplate('${esc(prepareAction.workflow || workflow.id)}', '${esc(prepareAction.step || step.id)}')">Prepare research-exit templates</button>` : ""}
        <button class="secondary-button" type="button" onclick="clearSelectedWorkflowStep()">Clear selected step</button>
      </div>
      <div id="workflow-step-copy-result" class="muted" style="margin-top:8px"></div>
      <div style="margin-top:8px">${disabledRows}</div>
    </section>`;
}

function renderNextAction(next) {
  const selected = selectedWorkflowStepMatch();
  if (selected.step) return renderSelectedStepWizard(next, selected.workflow, selected.step);
  const commands = renderListItems(next.suggested_commands || []);
  const gateRows = renderGateBlockers(next.pending_review_gate_blockers || []);
  const canExecute = next.can_execute === true || next.effective_can_execute === true;
  const requiresApproval = next.requires_approval === true || next.effective_requires_approval === true;
  const approvalGate = next.approval_gate || next.effective_approval_gate || "none";
  const action = next.effective_next_action || next.next_overlay_action || next.next_packet_action || next.umbrella_route_next_action || "none";
  const workflow = next.effective_workflow || next.active_overlay || next.umbrella_route_workflow || next.next_stage || "none";
  const route = next.effective_route || next.umbrella_route_state || next.overlay_phase || "none";
  const selectedPackage = currentStatusReport?.package || {};
  const selectedRoute = selectedPackage.umbrella_route || {};
  const successorLeaf = selectedRoute.active_successor_leaf;
  const umbrellaHasSuccessor = selectedPackage.kind === "umbrella" && successorLeaf;
  const missingResearchQuestion = (next.blocking_issues || []).some((issue) => String(issue).includes("current research question"));
  const genericBlocked = !umbrellaHasSuccessor && !missingResearchQuestion && !canExecute && !requiresApproval;
  const executionState = umbrellaHasSuccessor ? "ready" : (canExecute ? "ready" : (requiresApproval ? "needs approval" : (missingResearchQuestion ? "needs research setup" : "blocked")));
  const displayAction = umbrellaHasSuccessor
    ? "continue in successor leaf"
    : (missingResearchQuestion && action === "none"
      ? "define current research question"
      : (genericBlocked && action === "none" ? deriveBlockedAction(next) : action));
  const validator = next.recommended_validator || next.overlay_recommended_validator || "none";
  const guidance = umbrellaHasSuccessor
    ? "The pivot has already produced a successor leaf. Continue there; this umbrella is now context, not the working object."
    : (missingResearchQuestion
      ? "This leaf needs a research question or thesis direction before the research workflow can run."
      : (requiresApproval && !canExecute && !(next.pending_review_gate_blockers || []).length
        ? "This is an approval boundary from the workflow/package state, not a materialized review-gate file. The cockpit can record an operator decision, but it will not move lifecycle state by itself."
        : (canExecute
          ? "This action is executable from the governed runner."
          : "The research question is admitted. The remaining work is a guided research-stage packet, not a direct cockpit run.")));
  const calloutClass = umbrellaHasSuccessor || canExecute ? "callout" : (requiresApproval ? "callout warn" : "callout bad");
  const primaryButtons = umbrellaHasSuccessor
    ? `<div class="toolbar" style="margin-top:10px"><button type="button" onclick="switchToPackage('${esc(successorLeaf)}')">Continue in successor leaf</button></div>`
    : (missingResearchQuestion
      ? `<div class="approval-panel">
          <h3>Set research question</h3>
          <p class="muted">This saves the research question into the selected leaf status file so the research workflow has a concrete target.</p>
          <label>Research question
            <textarea id="research-question-input" rows="4" style="width:100%; min-height:88px; padding:10px; border:1px solid var(--line); border-radius:6px; font:inherit;">${esc(defaultResearchQuestions[selectedPackage.package] || "")}</textarea>
          </label>
          <div class="toolbar" style="margin-top:10px">
            <button type="button" onclick="submitResearchQuestion()">Save research question</button>
            ${artifact(packageStatusPath(selectedPackage.package, "research-handoff.md"), "Preview handoff")}
            ${artifact(selectedPackage.status_path, "Preview status.yaml")}
          </div>
          <div id="research-question-result" style="margin-top:10px"></div>
        </div>`
      : (genericBlocked ? renderVisibleBlockerPanel(next) : ""));
  const stageLabel = next.next_stage || selectedPackage.current_stage || "none";
  const workflowLabel = workflow === "none" ? stageLabel : workflow;
  const syntheticApprovalContext = !umbrellaHasSuccessor && requiresApproval && !canExecute && !(next.pending_review_gate_blockers || []).length
    ? renderApprovalBoundaryContext(next, stageLabel, workflowLabel, approvalGate)
    : "";
  const syntheticApprovalControls = !umbrellaHasSuccessor && requiresApproval && !canExecute && !(next.pending_review_gate_blockers || []).length
    ? `<details class="advanced">
      <summary>Record approval boundary</summary>
      <div class="approval-panel">
      <p class="muted">Use these when the displayed workflow, route, action, and gate match your intent. This writes an approval log only; it does not initialize leaves, publish, promote, or edit package state. If the Contract Scan is failing, keep that as follow-up architecture cleanup; it does not by itself mean this active gate failed.</p>
      <label>Decision reason
        <input id="next-approval-reason" placeholder="why this route is approved, rejected, or deferred" title="Required. This is written into reviewable-runs/logs as the operator rationale.">
      </label>
      <div class="toolbar" style="margin-top:10px">
        <button type="button" onclick="submitNextApproval('approve')" title="Record approval for the displayed workflow/action/gate. No lifecycle files are changed by this button.">Approve boundary</button>
        <button type="button" onclick="submitNextApproval('defer')" title="Record that this boundary is not ready yet.">Defer</button>
        <button type="button" onclick="submitNextApproval('reject')" title="Record that this route should not proceed.">Reject</button>
      </div>
      </div>
    </details>`
    : "";
  return `<div class="wizard-head">
      <div>
        <div class="wizard-kicker">Workflow wizard</div>
        <div class="wizard-title">${esc(selectedPackage.package || next.package || "selected package")}</div>
        <div class="muted" style="margin-top:4px">Stage: <strong>${esc(stageLabel)}</strong> · Workflow: <strong>${esc(workflowLabel)}</strong></div>
      </div>
      <div>${badge(executionState)}</div>
    </div>
    <div class="${calloutClass}">
      <strong>${badge(executionState)} ${esc(displayAction)}</strong>
      <div class="muted" style="margin-top:6px">${esc(guidance)}</div>
      ${primaryButtons}
    </div>
    ${syntheticApprovalContext}
    ${syntheticApprovalControls}`;
}

function renderPackage(pkg, root) {
  if (!pkg) {
    return `<h2>Package State</h2>
      <p class="muted">No package filter selected.</p>
      <table><tbody>
        <tr><th>Gate contracts</th><td>${esc(root.gate_contract_count || 0)}</td></tr>
        <tr><th>Pipeline profiles</th><td>${esc(root.pipeline_profile_count || 0)}</td></tr>
        <tr><th>Policy</th><td>${artifact(root.harness_policy_path || "harness_policy.yaml")}</td></tr>
      </tbody></table>`;
  }
  const stages = (pkg.stages || []).map((stage) => `
    <tr>
      <td>${esc(stage.stage)}</td>
      <td>${badge(String(stage.done === true))}</td>
      <td>${esc(stage.last_updated || "")}</td>
    </tr>`).join("");
  return `<h2>Package State</h2>
    <table><tbody>
      <tr><th>Package</th><td>${esc(pkg.package)}</td></tr>
      <tr><th>Kind</th><td>${esc(pkg.kind)}</td></tr>
      <tr><th>Current stage</th><td>${esc(pkg.current_stage || "none")}</td></tr>
      <tr><th>Umbrella route</th><td>${renderUmbrellaRoute(pkg.umbrella_route)}</td></tr>
      <tr><th>Status file</th><td>${artifact(pkg.status_path)}</td></tr>
    </tbody></table>
    <h2 style="margin-top:14px">Lifecycle Stages</h2>
    <table>
      <thead><tr><th>Stage</th><th>Done</th><th>Updated</th></tr></thead>
      <tbody>${stages || '<tr><td colspan="3" class="muted">No stage records.</td></tr>'}</tbody>
    </table>`;
}

function renderUmbrellaRoute(route) {
  if (!route || typeof route !== "object") return `<span class="muted">${esc(inlineValue(route))}</span>`;
  return `<table><tbody>
    <tr><th>Workflow</th><td>${esc(route.active_workflow || "none")}</td></tr>
    <tr><th>Route</th><td>${esc(route.active_route || "none")}</td></tr>
    <tr><th>Next action</th><td>${esc(route.next_action || "none")}</td></tr>
    <tr><th>Candidate</th><td>${esc(route.active_candidate || "none")}</td></tr>
    <tr><th>Successor leaf</th><td>${esc(route.active_successor_leaf || "not initialized")}</td></tr>
  </tbody></table>`;
}

function explainFinding(finding) {
  const surface = finding.surface || "";
  const message = finding.message || "";
  const workflow = finding.workflow_id || "";
  if (surface === "context_admission") {
    return {
      meaning: "A workflow needs runtime input or package config that is missing for this broad validation scan.",
      action: workflow === "post_ceiling_pivot"
        ? "Relevant to the active route; inspect the workflow input."
        : "Usually background noise unless you are trying to run this workflow now."
    };
  }
  if (surface === "package_route_resolution") {
    return {
      meaning: "The selected package shape does not match that workflow. Umbrella packages should not run every leaf-only workflow.",
      action: workflow === "post_ceiling_pivot"
        ? "Relevant to the active route."
        : "Ignore for the current route unless you intended to enter that workflow."
    };
  }
  if (surface === "review_gates") {
    return {
      meaning: "A file-backed review gate artifact has a structural or decision issue.",
      action: "Open the linked gate artifact and fix or decide it before governed progress."
    };
  }
  return {
    meaning: "A contract validation check reported a mismatch.",
    action: "Inspect only if the workflow is part of the current route."
  };
}

function renderValidation(health) {
  const counts = health.severity_counts || {};
  const findings = (health.top_findings || []).map((finding) => `
    <tr>
      <td>${badge(finding.severity || "info")}</td>
      <td>${esc(finding.workflow_id || "")}</td>
      <td>${esc(finding.surface || "")}</td>
      <td>${artifact(finding.path, finding.path || "")}</td>
      <td>${esc(finding.message || "")}</td>
      <td>${esc(explainFinding(finding).meaning)}</td>
      <td>${esc(explainFinding(finding).action)}</td>
    </tr>`).join("");
  return `<h2>Background Contract Scan</h2>
    <div class="callout warn">This scan is failing because broad workflow contracts are being checked against the selected package shape. It is architecture cleanup, not the active route verdict.</div>
    <table><tbody>
      <tr><th>Mode</th><td>${esc(health.mode || "")}</td></tr>
      <tr><th>Findings</th><td>${esc(health.finding_count || 0)} total, ${esc(counts.error || 0)} errors, ${esc(counts.warning || 0)} warnings</td></tr>
      <tr><th>Evidence counts</th><td><code>${esc(JSON.stringify(health.execution_evidence_counts || {}))}</code></td></tr>
    </tbody></table>
    <h2 style="margin-top:14px">Top Findings</h2>
    <table>
      <thead><tr><th>Severity</th><th>Workflow</th><th>Surface</th><th>Path</th><th>Message</th><th>Meaning</th><th>What to do</th></tr></thead>
      <tbody>${findings || '<tr><td colspan="7" class="muted">No findings.</td></tr>'}</tbody>
    </table>`;
}

function renderGates(gates) {
  const rows = [...(gates.pending || []), ...(gates.resolved || []), ...(gates.invalid || [])].map((gate) => `
    <tr>
      <td>${badge(gate.status)}</td>
      <td><a href="${gateHref(gate)}">${esc(gate.gate_id || gate.path)}</a></td>
      <td>${esc(gate.package_key || gate.package || "")}</td>
      <td>${esc(gate.workflow_id || "")}<br><span class="muted">${esc(gate.step_id || "")}</span></td>
      <td>${esc(gate.gate_type || gate.gate_contract || "")}</td>
      <td>${esc(gate.created_at || gate.decided_at || "")}</td>
      <td>${artifact(gate.path, "artifact")}</td>
    </tr>`).join("");
  return `<h2>Review Gates</h2>
    <table>
      <thead><tr><th>Status</th><th>Gate</th><th>Package</th><th>Workflow</th><th>Class</th><th>Time</th><th>File</th></tr></thead>
      <tbody>${rows || '<tr><td colspan="7" class="muted">No review gates.</td></tr>'}</tbody>
    </table>`;
}

function renderRuns(yamlRuns, legacyRuns) {
  const yamlRows = yamlRuns.map((run) => `
    <tr>
      <td>${badge(run.terminal_status || "recorded")}</td>
      <td>${esc(run.run_id || "")}</td>
      <td>${esc(run.package_key || run.package || "")}</td>
      <td>${esc(run.workflow_id || "")}</td>
      <td>${esc(run.ended_at || run.started_at || "")}</td>
      <td>${artifact(run.path, "artifact")}</td>
    </tr>`).join("");
  const legacyRows = legacyRuns.map((run) => `
    <tr>
      <td>${badge(run.status || run.kind || "recorded")}</td>
      <td>${esc(run.run_id || run.gate_id || "")}</td>
      <td>${esc(run.package_key || run.package || "")}</td>
      <td>${esc(run.workflow || run.stage || "")}</td>
      <td>${esc(run.timestamp || "")}</td>
      <td>${artifact(run.path, "artifact")}</td>
    </tr>`).join("");
  return `<h2>Recent Run Records</h2>
    <table>
      <thead><tr><th>Status</th><th>Run</th><th>Package</th><th>Workflow</th><th>Time</th><th>File</th></tr></thead>
      <tbody>${yamlRows}${legacyRows || ""}${(!yamlRows && !legacyRows) ? '<tr><td colspan="6" class="muted">No recent run records.</td></tr>' : ""}</tbody>
    </table>`;
}

async function submitNextApproval(outcome) {
  const reasonInput = document.getElementById("next-approval-reason");
  const output = document.getElementById("action-output");
  const reason = reasonInput ? reasonInput.value.trim() : "";
  if (!reason) {
    output.innerHTML = '<section><div class="error">Decision reason is required.</div></section>';
    return;
  }
  const packageValue = packageInput.value.trim();
  const ok = window.confirm(`Record ${outcome} for the current approval boundary on ${packageValue}? This writes a local approval log only; it does not edit package state.`);
  if (!ok) return;
  output.innerHTML = '<section>Recording current approval boundary decision...</section>';
  const response = await fetch("/api/next/approval", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      package: packageValue,
      outcome,
      reason,
      decided_by: "content-cockpit"
    })
  });
  const payload = await response.json();
  output.innerHTML = `<section><h2>Approval Boundary Decision</h2><pre>${esc(JSON.stringify(payload, null, 2))}</pre></section>`;
  await loadStatus();
}

loadPackageOptions().then(loadStatus);
</script>
"""
    return page_shell("Content Agent Cockpit", body, config)


def gate_page(config: CockpitConfig, gate_identifier: str) -> bytes:
    body = f"""
<header>
  <h1>Review Gate</h1>
  <div class="toolbar">
    <a href="/">Cockpit</a>
    <a id="gate-json-link" href="/api/gate?gate={quote(gate_identifier)}" target="_blank">JSON</a>
  </div>
</header>
<main>
  <div id="decision-output" class="stack"></div>
  <div id="gate" class="stack">Loading...</div>
</main>
<script>
const gateIdentifier = {json.dumps(gate_identifier)};
function esc(value) {{
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({{
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }}[char]));
}}
function badge(value) {{
  const raw = String(value ?? "unknown");
  let cls = "badge";
  if (["passed", "completed", "resolved", "true"].includes(raw)) cls += " good";
  if (["pending", "warning", "deferred", "gated"].includes(raw)) cls += " warn";
  if (["failed", "error", "invalid", "rejected", "false"].includes(raw)) cls += " bad";
  return `<span class="${{cls}}">${{esc(raw)}}</span>`;
}}
function artifact(path, label) {{
  if (!path) return '<span class="muted">none</span>';
  return `<a href="/artifact?path=${{encodeURIComponent(path)}}" target="_blank">${{esc(label || path)}}</a>`;
}}
async function submitDecision(outcome) {{
  const reasonInput = document.getElementById("decision-reason");
  const output = document.getElementById("decision-output");
  const reason = reasonInput ? reasonInput.value.trim() : "";
  if (!reason) {{
    output.innerHTML = '<section><div class="error">Decision reason is required.</div></section>';
    return;
  }}
  output.innerHTML = '<section>Recording decision...</section>';
  const response = await fetch("/api/gate/decision", {{
    method: "POST",
    headers: {{"Content-Type": "application/json"}},
    body: JSON.stringify({{
      gate: gateIdentifier,
      outcome,
      reason,
      decided_by: "content-cockpit"
    }})
  }});
  const payload = await response.json();
  output.innerHTML = `<section><h2>Decision Result</h2><pre>${{esc(JSON.stringify(payload, null, 2))}}</pre></section>`;
  await loadGate();
}}
async function loadGate() {{
  const response = await fetch(`/api/gate?gate=${{encodeURIComponent(gateIdentifier)}}`);
  const payload = await response.json();
  if (!response.ok) {{
    document.getElementById("gate").innerHTML = `<section><div class="error">${{esc(payload.error || response.statusText)}}</div></section>`;
    return;
  }}
  const report = payload.review_gate || {{}};
  const gate = report.gate || {{}};
  const artifactData = report.artifact || {{}};
  const evidence = artifactData.evidence || {{}};
  const showDecisionControls = gate.status === "pending";
  const previewPaths = (evidence.preview_paths || []).map((path) => `<li>${{artifact(path)}}</li>`).join("");
  const evidencePaths = (evidence.evidence_paths || []).map((path) => `<li>${{artifact(path)}}</li>`).join("");
  const decisionControls = showDecisionControls ? `
      <section class="span-12">
        <h2>Gate Decision</h2>
        <label>Reason
          <input id="decision-reason" placeholder="required decision reason">
        </label>
        <div class="toolbar" style="margin-top:10px">
          <button type="button" onclick="submitDecision('approve')">Approve</button>
          <button type="button" onclick="submitDecision('reject')">Reject</button>
          <button type="button" onclick="submitDecision('defer')">Defer</button>
        </div>
      </section>` : "";
  document.getElementById("gate").innerHTML = `
    <div class="grid">
      <section class="span-4">
        <h2>Gate Summary</h2>
        <table><tbody>
          <tr><th>Status</th><td>${{badge(gate.status)}}</td></tr>
          <tr><th>Gate</th><td>${{esc(gate.gate_id || "")}}</td></tr>
          <tr><th>Package</th><td>${{esc(gate.package_key || gate.package || "")}}</td></tr>
          <tr><th>Workflow</th><td>${{esc(gate.workflow_id || "")}}</td></tr>
          <tr><th>Step</th><td>${{esc(gate.step_id || "")}}</td></tr>
          <tr><th>Created</th><td>${{esc(gate.created_at || "")}}</td></tr>
          <tr><th>Artifact</th><td>${{artifact(gate.path)}}</td></tr>
        </tbody></table>
      </section>
      <section class="span-8">
        <h2>Evidence Links</h2>
        <table><tbody>
          <tr><th>Preview</th><td><ul class="path-list">${{previewPaths || '<li class="muted">none</li>'}}</ul></td></tr>
          <tr><th>Evidence</th><td><ul class="path-list">${{evidencePaths || '<li class="muted">none</li>'}}</ul></td></tr>
          <tr><th>Run record</th><td>${{artifact((artifactData.run || {{}}).run_record_path)}}</td></tr>
          <tr><th>Resolved run</th><td>${{artifact((artifactData.run || {{}}).resolved_run_path)}}</td></tr>
        </tbody></table>
      </section>
      <section class="span-12">
        <h2>Exact Gate Artifact</h2>
        <pre>${{esc(JSON.stringify(artifactData, null, 2))}}</pre>
      </section>
      ${{decisionControls}}
    </div>`;
}}
loadGate();
</script>
"""
    return page_shell("Review Gate", body, config)


class CockpitHandler(BaseHTTPRequestHandler):
    config: CockpitConfig

    server_version = "ContentCockpit/0.1"

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        try:
            if parsed.path in {"/", "/index.html"}:
                self.send_bytes(index_page(self.config), "text/html; charset=utf-8")
                return
            if parsed.path == "/gate":
                gate = first_query_value(query, "gate")
                if not gate:
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "missing gate query parameter")
                    return
                self.send_bytes(gate_page(self.config, gate), "text/html; charset=utf-8")
                return
            if parsed.path == "/api/status":
                package_arg = first_query_value(query, "package") or self.config.package_arg
                limit = clamp_limit(first_query_value(query, "limit"), self.config.limit)
                self.send_json(cockpit_status_payload(package_arg, limit))
                return
            if parsed.path == "/api/packages":
                self.send_json(cockpit_package_list_payload())
                return
            if parsed.path == "/api/next":
                package_arg = first_query_value(query, "package") or self.config.package_arg
                if not package_arg:
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "package is required")
                    return
                self.send_json(cockpit_next_payload(package_arg))
                return
            if parsed.path == "/api/gates":
                package_arg = first_query_value(query, "package") or self.config.package_arg
                status_filter = first_query_value(query, "status") or "all"
                if status_filter not in {"pending", "resolved", "all"}:
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "status must be pending, resolved, or all")
                    return
                self.send_json(cockpit_gate_list_payload(package_arg, status_filter))
                return
            if parsed.path == "/api/gate":
                gate = first_query_value(query, "gate")
                if not gate:
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "missing gate query parameter")
                    return
                self.send_json(cockpit_gate_payload(gate))
                return
            if parsed.path == "/artifact":
                path_value = first_query_value(query, "path")
                if not path_value:
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "missing path query parameter")
                    return
                self.send_artifact(path_value)
                return
            self.send_json_error(HTTPStatus.NOT_FOUND, "not found")
        except Exception as exc:  # pragma: no cover - server response path
            self.send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            body = self.read_json_body()
            if parsed.path == "/api/validate":
                package_arg = body.get("package") if isinstance(body.get("package"), str) else self.config.package_arg
                payload = validation_action_payload(package_arg)
                status = HTTPStatus.OK if payload.get("success") is True else HTTPStatus.BAD_REQUEST
                self.send_json(payload, status)
                return
            if parsed.path == "/api/editorial-report":
                package_arg = body.get("package") if isinstance(body.get("package"), str) else self.config.package_arg
                if not package_arg:
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "package is required")
                    return
                payload = editorial_report_action_payload(package_arg)
                status = HTTPStatus.OK if payload.get("success") is True else HTTPStatus.BAD_REQUEST
                self.send_json(payload, status)
                return
            if parsed.path == "/api/next/approval":
                package_arg = body.get("package") if isinstance(body.get("package"), str) else self.config.package_arg
                outcome = body.get("outcome")
                reason = body.get("reason")
                decided_by = body.get("decided_by", "content-cockpit")
                if not isinstance(package_arg, str) or not package_arg.strip():
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "package is required")
                    return
                if not isinstance(outcome, str):
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "outcome is required")
                    return
                if not isinstance(reason, str):
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "reason is required")
                    return
                if not isinstance(decided_by, str):
                    decided_by = "content-cockpit"
                payload = current_next_gate_decision_action_payload(
                    package_arg,
                    outcome,
                    reason=reason,
                    decided_by=decided_by,
                )
                self.send_json(payload, HTTPStatus.OK)
                return
            if parsed.path == "/api/research-question":
                package_arg = body.get("package") if isinstance(body.get("package"), str) else self.config.package_arg
                research_question = body.get("research_question")
                if not isinstance(package_arg, str) or not package_arg.strip():
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "package is required")
                    return
                if not isinstance(research_question, str):
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "research_question is required")
                    return
                payload = research_question_action_payload(package_arg, research_question)
                self.send_json(payload, HTTPStatus.OK)
                return
            if parsed.path == "/api/next/execute":
                package_arg = body.get("package") if isinstance(body.get("package"), str) else self.config.package_arg
                approved = body.get("approved")
                if not isinstance(package_arg, str) or not package_arg.strip():
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "package is required")
                    return
                payload = next_execute_action_payload(package_arg, approved is True)
                status = HTTPStatus.OK if payload.get("success") is True else HTTPStatus.BAD_REQUEST
                self.send_json(payload, status)
                return
            if parsed.path == "/api/workflow-template":
                package_arg = body.get("package") if isinstance(body.get("package"), str) else self.config.package_arg
                workflow_id = body.get("workflow")
                step_id = body.get("step")
                if not isinstance(package_arg, str) or not package_arg.strip():
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "package is required")
                    return
                if not isinstance(workflow_id, str) or not isinstance(step_id, str):
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "workflow and step are required")
                    return
                payload = prepare_workflow_template_action_payload(package_arg, workflow_id, step_id)
                self.send_json(payload, HTTPStatus.OK)
                return
            if parsed.path == "/api/gate/decision":
                gate = body.get("gate")
                outcome = body.get("outcome")
                reason = body.get("reason")
                decided_by = body.get("decided_by", "content-cockpit")
                if not isinstance(gate, str) or not gate.strip():
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "gate is required")
                    return
                if not isinstance(outcome, str):
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "outcome is required")
                    return
                if not isinstance(reason, str):
                    self.send_json_error(HTTPStatus.BAD_REQUEST, "reason is required")
                    return
                if not isinstance(decided_by, str):
                    decided_by = "content-cockpit"
                payload = gate_decision_action_payload(
                    gate,
                    outcome,
                    reason=reason,
                    decided_by=decided_by,
                )
                status = HTTPStatus.OK if payload.get("success") is True else HTTPStatus.BAD_REQUEST
                self.send_json(payload, status)
                return
            self.send_json_error(HTTPStatus.NOT_FOUND, "not found")
        except ValueError as exc:
            self.send_json_error(HTTPStatus.BAD_REQUEST, str(exc))
        except Exception as exc:  # pragma: no cover - server response path
            self.send_json_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def read_json_body(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        if length > MAX_ACTION_BODY_BYTES:
            raise ValueError("request body is too large")
        raw = self.rfile.read(length)
        payload = parse_json_bytes(raw) if raw else {}
        if payload is None:
            return {}
        if not isinstance(payload, dict):
            raise ValueError("request body must be a JSON object")
        return payload

    def send_json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        self.send_bytes(json_bytes(payload), "application/json; charset=utf-8", status)

    def send_json_error(self, status: HTTPStatus, message: str) -> None:
        self.send_json({"success": False, "error": message}, status)

    def send_bytes(
        self,
        body: bytes,
        content_type: str,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> None:
        self.send_response(status.value)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_artifact(self, path_value: str) -> None:
        path = repo_artifact_path(path_value)
        if not path.exists():
            self.send_json_error(HTTPStatus.NOT_FOUND, f"artifact not found: {path_value}")
            return
        if path.is_dir():
            entries = [item.relative_to(content_agent.REPO_ROOT).as_posix() for item in sorted(path.iterdir())]
            body = "\n".join(entries).encode("utf-8")
            self.send_bytes(body, "text/plain; charset=utf-8")
            return
        mime_type, _ = mimetypes.guess_type(path.name)
        if is_text_artifact(path, mime_type):
            data = path.read_bytes()
            truncated = len(data) > self.config.artifact_max_bytes
            if truncated:
                data = data[: self.config.artifact_max_bytes]
                data += b"\n\n[content-cockpit truncated this artifact preview]\n"
            self.send_bytes(data, "text/plain; charset=utf-8")
            return
        self.send_bytes(path.read_bytes(), mime_type or "application/octet-stream")

    def log_message(self, format: str, *args: object) -> None:
        sys.stderr.write("content-cockpit: " + (format % args) + "\n")


def build_handler(config: CockpitConfig) -> type[CockpitHandler]:
    class ConfiguredCockpitHandler(CockpitHandler):
        pass

    ConfiguredCockpitHandler.config = config
    return ConfiguredCockpitHandler


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Serve the read-only Phase 2 local cockpit.")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host interface to bind. Defaults to localhost.")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to bind.")
    parser.add_argument("--package", dest="package_arg", help="Optional default package key/path.")
    parser.add_argument("--limit", type=int, default=content_agent.DEFAULT_RECENT_LIMIT, help="Recent run limit.")
    parser.add_argument(
        "--artifact-max-bytes",
        type=int,
        default=DEFAULT_ARTIFACT_MAX_BYTES,
        help="Maximum bytes to show for text artifact previews.",
    )
    parser.add_argument("--once", action="store_true", help="Print one read-only snapshot instead of serving HTTP.")
    parser.add_argument("--format", choices=["json", "html"], default="json", help="Output format for --once.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = CockpitConfig(
        host=args.host,
        port=args.port,
        package_arg=args.package_arg,
        limit=max(1, min(args.limit, MAX_RECENT_LIMIT)),
        artifact_max_bytes=max(1, args.artifact_max_bytes),
    )
    if args.once:
        if args.format == "html":
            sys.stdout.buffer.write(index_page(config))
            return
        print(json.dumps(cockpit_status_payload(config.package_arg, config.limit), indent=2, default=str))
        return

    server = ThreadingHTTPServer((config.host, config.port), build_handler(config))
    url = f"http://{config.host}:{config.port}/"
    print(f"content-cockpit serving {url}")
    print("press Ctrl-C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\ncontent-cockpit stopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
