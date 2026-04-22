#!/usr/bin/env python3
"""
Resolve, execute, or update a publication lifecycle stage.
"""

from __future__ import annotations

import argparse
import json
import shlex
import string
import subprocess
import sys
from datetime import datetime

from audit_package import print_report
from harness import (
    build_stage_resolution,
    emit_launch_pack,
    repo_relpath,
)
from lifecycle import (
    DEPENDENCY_MAP,
    REPO_ROOT,
    STAGES,
    load_status_ref,
    load_workflow_contract,
    save_status,
)


def parse_extra_args(unknown: list[str]) -> dict:
    extra_args: dict[str, str | bool] = {}
    idx = 0
    while idx < len(unknown):
        token = unknown[idx]
        if token.startswith("--"):
            key = token[2:].replace("-", "_")
            if idx + 1 < len(unknown) and not unknown[idx + 1].startswith("--"):
                extra_args[key] = unknown[idx + 1]
                idx += 2
            else:
                extra_args[key] = True
                idx += 1
        else:
            idx += 1
    return extra_args


def extract_template_fields(templates: list[str]) -> set[str]:
    fields = set()
    for template in templates:
        for _, field_name, _, _ in string.Formatter().parse(template):
            if field_name:
                fields.add(field_name)
    return fields


def filter_passthrough_args(unknown: list[str], template_fields: set[str]) -> list[str]:
    passthrough = []
    idx = 0
    while idx < len(unknown):
        token = unknown[idx]
        if token.startswith("--"):
            key = token[2:].replace("-", "_")
            has_value = idx + 1 < len(unknown) and not unknown[idx + 1].startswith("--")
            if key in template_fields:
                idx += 2 if has_value else 1
                continue
            passthrough.append(token)
            if has_value:
                passthrough.append(unknown[idx + 1])
                idx += 2
            else:
                idx += 1
            continue
        passthrough.append(token)
        idx += 1
    return passthrough


def resolve_args(package_key: str, status_data: dict, extra_args: dict) -> dict:
    config = status_data.get("config", {})
    package_path = f"publications/{package_key}"
    inferred = {
        "package_key": package_key,
        "package_name": package_key.split("/")[-1],
        "package_path": package_path,
        "publication": status_data.get("publication", package_key.split("/")[-1]),
    }
    return {**inferred, **config, **extra_args}


def get_dependency_warnings(stage: str, status_data: dict) -> list[str]:
    warnings = []
    for dependency in DEPENDENCY_MAP.get(stage, []):
        dep_status = status_data.get("stages", {}).get(dependency, {})
        if not dep_status.get("done"):
            warnings.append(
                f"Stage '{stage}' typically follows '{dependency}', which is not done."
            )
    return warnings


def enforce_single_mutation(args: argparse.Namespace) -> None:
    actions = [args.execute, args.mark_done, args.mark_undone]
    if sum(bool(action) for action in actions) > 1:
        raise ValueError("Use only one of --execute, --mark-done, or --mark-undone per invocation.")


def format_commands(templates: list[str], resolved_args: dict, passthrough_args: list[str]) -> list[str]:
    commands = []
    for template in templates:
        command = template.format(**resolved_args)
        if passthrough_args:
            command = f"{command} {shlex.join(passthrough_args)}"
        commands.append(command)
    return commands


def maybe_block_for_done_stage(args: argparse.Namespace, stage_data: dict, action_label: str) -> str | None:
    if action_label == "execute" and stage_data.get("done") and not args.force:
        return "Stage is already marked done. Use --force to execute it again."
    if action_label == "mark-done" and stage_data.get("done") and not args.force:
        return "Stage is already marked done. Use --force to update the timestamp anyway."
    if action_label == "mark-undone" and not stage_data.get("done") and not args.force:
        return "Stage is already marked not done. Use --force to update the timestamp anyway."
    return None


def log_run(
    package_key: str,
    stage: str,
    action: str,
    success: bool,
    output: str,
    commands: list[str],
    workflow_doc: str,
    status_path: str,
    resolution: dict | None = None,
    stage_state_before: dict | None = None,
    stage_state_after: dict | None = None,
    dependency_warnings: list[str] | None = None,
) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    package_id = package_key.replace("/", "__")
    log_dir = REPO_ROOT / "reviewable-runs" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{timestamp}_{package_id}_{stage}_{action}.json"

    output_limit = 6000
    output_excerpt = output[-output_limit:]
    approval_gate = (resolution or {}).get("approval_gate", "unknown")
    requires_approval = bool((resolution or {}).get("requires_approval", False))
    approval_status = "not_required" if not requires_approval else "not_recorded_in_log"
    command_check = "pass" if success else "fail"
    payload = {
        "kind": "lifecycle_stage_run",
        "schema_version": 2,
        "timestamp": timestamp,
        "run_id": f"{timestamp}_{package_id}_{stage}_{action}",
        "package": package_key,
        "stage": stage,
        "action": action,
        "success": success,
        "boundary": {
            "type": "explicit non-approval reason",
            "reason": "Local lifecycle-stage operation. The log records repo-state work, not an external publish or channel mutation.",
            "external_side_effect": False,
            "approval_gate": approval_gate,
            "approval_required": requires_approval,
            "approval_status": approval_status,
        },
        "task": {
            "objective": f"Run lifecycle action '{action}' for package '{package_key}' stage '{stage}'.",
            "stop_condition": "Command finished and a lifecycle log was written.",
            "non_goals": [
                "Do not treat this routine log as retained proof.",
                "Do not claim external publication or channel mutation from this log alone.",
            ],
        },
        "execution": {
            "commands": commands,
            "output_excerpt": output_excerpt,
            "output_truncated": len(output) > output_limit,
            "state_before": stage_state_before or {},
            "state_after": stage_state_after or {},
            "dependency_warnings": dependency_warnings or [],
        },
        "evidence": {
            "workflow_doc": workflow_doc,
            "status_path": status_path,
            "required_context": (resolution or {}).get("required_context", []),
            "expected_outputs": (resolution or {}).get("expected_outputs", []),
            "done_when": (resolution or {}).get("done_when", []),
        },
        "verification": {
            "checks": [
                {
                    "name": "command_exit_status",
                    "result": command_check,
                    "notes": "For mark-only actions, this is the local status update result.",
                },
                {
                    "name": "lifecycle_log_written",
                    "result": "pass",
                    "notes": repo_relpath(log_path),
                },
            ],
            "residual_risk": "This lightweight log preserves the operational boundary. Promote to a full Reviewable Runs packet only when the run crosses a stronger review or proof boundary.",
        },
        "failure_or_risk": {
            "actual_failure": None if success else "Lifecycle action failed; inspect output_excerpt.",
            "possible_failures": [
                "Stage marked done without enough human review.",
                "External system state assumed from local state.",
                "Routine log mistaken for retained proof artifact.",
            ],
        },
        "workflow_doc": workflow_doc,
        "status_path": status_path,
        "commands": commands,
        "output_excerpt": output_excerpt,
        "output_truncated": len(output) > output_limit,
    }
    log_path.write_text(json.dumps(payload, indent=2) + "\n")
    return repo_relpath(log_path)


def print_stage_summary(resolution: dict, dependency_warnings: list[str], launch_pack_path: str | None) -> None:
    state = resolution["current_state"]
    print(f"PACKAGE: {resolution['package']}")
    print(f"Stage: {resolution['stage']}")
    print(f"Current State: done={state.get('done', False)} last_updated={state.get('last_updated')}")
    print(f"Workflow Doc: {resolution['workflow_doc']}")
    print(f"Runner Mode: {resolution['runner_mode']}")
    print(f"Launch Mode: {resolution['launch_mode']}")
    print(f"Default Skill: {resolution['default_skill'] or 'none'}")
    print(f"Approval Gate: {resolution['approval_gate']}")
    print(f"Requires Approval: {resolution['requires_approval']}")
    print(f"Can Execute: {resolution['can_execute']}")
    print(f"Pipeline Profile: {resolution.get('pipeline_profile')}")
    governing_brief = resolution.get("package_context_paths", {}).get("governing_brief_path")
    if governing_brief:
        print(f"Governing Brief: {governing_brief}")
    lifecycle_report = resolution.get("lifecycle_report", {})
    if lifecycle_report.get("warning_count"):
        print(f"Lifecycle Warnings: {lifecycle_report['warning_count']}")

    if dependency_warnings:
        print("\nDependency Warnings:")
        for warning in dependency_warnings:
            print(f"  - {warning}")

    if resolution["blocking_issues"]:
        print("\nBlocking Issues:")
        for issue in resolution["blocking_issues"]:
            print(f"  - {issue}")

    if resolution.get("recommended_workflows"):
        print("\nRecommended Workflows:")
        for workflow_id in resolution["recommended_workflows"]:
            print(f"  - {workflow_id}")

    if resolution.get("overlay_candidates"):
        print("\nOverlay Candidates:")
        for workflow_id in resolution["overlay_candidates"]:
            print(f"  - {workflow_id}")

    if resolution.get("active_overlay"):
        print("\nActive Overlay:")
        print(f"  - workflow: {resolution['active_overlay']}")
        print(f"  - root: {resolution.get('active_overlay_root')}")
        print(f"  - phase: {resolution.get('overlay_phase')}")
        print(f"  - next action: {resolution.get('next_overlay_action')}")
        if resolution.get("overlay_route"):
            print(f"  - route: {resolution.get('overlay_route')}")
        print(f"  - recommended validator: {resolution.get('overlay_recommended_validator')}")

    if resolution.get("gate_statuses"):
        print("\nGate Statuses:")
        for gate_id, gate_status in resolution["gate_statuses"].items():
            print(f"  - {gate_id}: {gate_status.get('status')} ({gate_status.get('decision')})")

    print("\nRequired Context:")
    for item in resolution["required_context"]:
        value = item.get("value")
        if value is None:
            print(f"  - {item['name']}: {item['status']}")
        else:
            print(f"  - {item['name']}: {item['status']} ({value})")

    print("\nExpected Outputs:")
    for item in resolution["expected_outputs"]:
        print(f"  - {item}")

    print("\nDone When:")
    for item in resolution["done_when"]:
        print(f"  - {item}")

    if resolution["launch_templates"]:
        print("\nLaunch Templates:")
        for template in resolution["launch_templates"]:
            print(f"  - {template}")
    else:
        print("\nLaunch Templates: none")

    if resolution["packet_templates"]:
        print("\nPacket Templates:")
        for template in resolution["packet_templates"]:
            print(f"  - {template}")

    if resolution["validator_commands"]:
        print("\nValidator Commands:")
        for command in resolution["validator_commands"]:
            print(f"  - {command}")

    if resolution["prohibited_moves"]:
        print("\nProhibited Moves:")
        for move in resolution["prohibited_moves"]:
            print(f"  - {move}")

    if resolution["packet_paths"]:
        print("\nPacket Paths:")
        for name, path in resolution["packet_paths"].items():
            print(f"  - {name}: {path}")

    if resolution.get("packet_phase"):
        print("\nPacket Progress:")
        print(f"  - phase: {resolution['packet_phase']}")
        print(f"  - next action: {resolution.get('next_packet_action')}")
        print(f"  - recommended validator: {resolution.get('recommended_validator')}")

    print("\nSuggested Commands:")
    for command in resolution["suggested_commands"]:
        print(f"  - {command}")

    if launch_pack_path:
        print(f"\nLaunch pack written to {launch_pack_path}")


def emit_result(payload: dict, output_format: str) -> None:
    if output_format == "json":
        print(json.dumps(payload, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve, execute, or update a publication lifecycle stage.")
    parser.add_argument("--package", required=True, help="Package path relative to publications/")
    parser.add_argument("--stage", required=True, choices=STAGES, help="Stage to inspect or mutate")
    parser.add_argument("--strict-deps", action="store_true", help="Block execute/mark-done when dependencies are not done")
    parser.add_argument("--force", action="store_true", help="Allow reruns or redundant state changes")
    parser.add_argument("--execute", action="store_true", help="Execute launch templates for scripted stages")
    parser.add_argument("--mark-done", action="store_true", help="Mark the stage as done without executing a command")
    parser.add_argument("--mark-undone", action="store_true", help="Mark the stage as not done")
    parser.add_argument("--emit-launch-pack", action="store_true", help="Write a machine-readable launch pack to reviewable-runs/logs/")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args, unknown = parser.parse_known_args()

    try:
        enforce_single_mutation(args)
        manifest_ref, status_data = load_status_ref(args.package)
        workflow_contract = load_workflow_contract(args.stage)
        resolution = build_stage_resolution(args.package, args.stage)
    except (FileNotFoundError, ValueError, KeyError) as exc:
        if args.format == "json":
            print(json.dumps({"error": str(exc)}, indent=2))
        else:
            print(f"ERROR: {exc}")
        sys.exit(1)

    stage_data = status_data.setdefault("stages", {}).setdefault(
        args.stage,
        {"done": False, "last_updated": None},
    )
    dependency_warnings = get_dependency_warnings(args.stage, status_data)
    if args.strict_deps and dependency_warnings and (args.execute or args.mark_done):
        message = {
            "error": "Dependency check failed with --strict-deps enabled.",
            "dependency_warnings": dependency_warnings,
        }
        if args.format == "json":
            print(json.dumps(message, indent=2))
        else:
            print("\nERROR: Dependency check failed with --strict-deps enabled.")
            for warning in dependency_warnings:
                print(f"  - {warning}")
        sys.exit(1)

    launch_pack_path = None
    if args.emit_launch_pack:
        launch_pack_path = repo_relpath(emit_launch_pack(resolution))
        resolution["launch_pack_path"] = launch_pack_path
        resolution["log_target"] = launch_pack_path

    if not any([args.execute, args.mark_done, args.mark_undone]):
        if args.format == "json":
            print(json.dumps(resolution, indent=2))
            return
        print_stage_summary(resolution, dependency_warnings, launch_pack_path)
        print()
        print_report(resolution["package_audit"])
        return

    metadata = workflow_contract["metadata"]

    if args.execute:
        block_message = maybe_block_for_done_stage(args, stage_data, "execute")
        if block_message:
            if args.format == "json":
                print(json.dumps({"message": block_message, "stage": args.stage, "package": manifest_ref.package_key}, indent=2))
            else:
                print(block_message)
            return
        if not resolution["can_execute"]:
            message = {
                "error": f"Stage '{args.stage}' is not executable under the current Phase 1.5 policy.",
                "blocking_issues": resolution["blocking_issues"],
            }
            if args.format == "json":
                print(json.dumps(message, indent=2))
            else:
                print(message["error"])
                for issue in resolution["blocking_issues"]:
                    print(f"  - {issue}")
            sys.exit(1)
        if not metadata["launch_templates"]:
            message = {"error": f"Stage '{args.stage}' has no launch templates to execute."}
            if args.format == "json":
                print(json.dumps(message, indent=2))
            else:
                print(message["error"])
            sys.exit(1)

        try:
            extra_args = parse_extra_args(unknown)
            resolved_args = resolve_args(manifest_ref.package_key, status_data, extra_args)
            passthrough_args = filter_passthrough_args(
                unknown,
                extract_template_fields(metadata["launch_templates"]),
            )
            commands = format_commands(metadata["launch_templates"], resolved_args, passthrough_args)
        except KeyError as exc:
            message = {
                "error": f"Missing required parameter {exc} for stage '{args.stage}'.",
                "blocking_issues": [f"Provide {exc} through status.yaml config or the CLI."],
            }
            if args.format == "json":
                print(json.dumps(message, indent=2))
            else:
                print(message["error"])
            sys.exit(1)

        stage_state_before = dict(stage_data)
        outputs = []
        success = True
        for command in commands:
            if args.format == "text":
                print(f"\nExecuting: {command}")
            process = subprocess.run(command, shell=True, capture_output=True, text=True)
            snippet = process.stdout + ("\n" if process.stdout and process.stderr else "") + process.stderr
            outputs.append(f"$ {command}\n{snippet}")
            if process.returncode != 0:
                success = False
                break

        output = "\n\n".join(outputs)
        if success and resolution["auto_mark_done_allowed"]:
            stage_data["done"] = True
            stage_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            save_status(manifest_ref.package_path, status_data)
            outcome = "Stage executed successfully and was marked done."
        elif success:
            outcome = "Stage executed successfully. Review the outcome, then use --mark-done when appropriate."
        else:
            outcome = "Stage execution failed."

        log_path = log_run(
            manifest_ref.package_key,
            args.stage,
            "execute",
            success,
            output,
            commands,
            resolution["workflow_doc"],
            repo_relpath(manifest_ref.status_path),
            resolution=resolution,
            stage_state_before=stage_state_before,
            stage_state_after=dict(stage_data),
            dependency_warnings=dependency_warnings,
        )
        payload = {
            **resolution,
            "action": "execute",
            "success": success,
            "commands": commands,
            "output_excerpt": output[-6000:],
            "log_path": log_path,
            "message": outcome,
            "current_state": stage_data,
        }
        if args.format == "json":
            print(json.dumps(payload, indent=2))
        else:
            print(outcome)
            print(f"Lifecycle run logged to {log_path}")
        if not success:
            sys.exit(1)
        return

    if args.mark_done:
        block_message = maybe_block_for_done_stage(args, stage_data, "mark-done")
        if block_message:
            if args.format == "json":
                print(json.dumps({"message": block_message, "stage": args.stage, "package": manifest_ref.package_key}, indent=2))
            else:
                print(block_message)
            return
        stage_state_before = dict(stage_data)
        stage_data["done"] = True
        stage_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        save_status(manifest_ref.package_path, status_data)
        message = f"Stage '{args.stage}' marked done for '{manifest_ref.package_key}'."
        log_path = log_run(
            manifest_ref.package_key,
            args.stage,
            "mark-done",
            True,
            message,
            [],
            resolution["workflow_doc"],
            repo_relpath(manifest_ref.status_path),
            resolution=resolution,
            stage_state_before=stage_state_before,
            stage_state_after=dict(stage_data),
            dependency_warnings=dependency_warnings,
        )
        payload = {**resolution, "action": "mark-done", "success": True, "log_path": log_path, "message": message}
        if args.format == "json":
            print(json.dumps(payload, indent=2))
        else:
            print(message)
            print(f"Lifecycle run logged to {log_path}")
        return

    block_message = maybe_block_for_done_stage(args, stage_data, "mark-undone")
    if block_message:
        if args.format == "json":
            print(json.dumps({"message": block_message, "stage": args.stage, "package": manifest_ref.package_key}, indent=2))
        else:
            print(block_message)
        return
    stage_state_before = dict(stage_data)
    stage_data["done"] = False
    stage_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    save_status(manifest_ref.package_path, status_data)
    message = f"Stage '{args.stage}' marked not done for '{manifest_ref.package_key}'."
    log_path = log_run(
        manifest_ref.package_key,
        args.stage,
        "mark-undone",
        True,
        message,
        [],
        resolution["workflow_doc"],
        repo_relpath(manifest_ref.status_path),
        resolution=resolution,
        stage_state_before=stage_state_before,
        stage_state_after=dict(stage_data),
        dependency_warnings=dependency_warnings,
    )
    payload = {**resolution, "action": "mark-undone", "success": True, "log_path": log_path, "message": message}
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(message)
        print(f"Lifecycle run logged to {log_path}")


if __name__ == "__main__":
    main()
