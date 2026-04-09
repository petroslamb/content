#!/usr/bin/env python3
"""
Resolve, execute, or update a publication lifecycle stage.

Examples:
  .venv/bin/python scripts/run_stage.py --package neural-architectures/neural-architecture-design-as-a-compositional-32e --stage essay_iteration
  .venv/bin/python scripts/run_stage.py --package neural-architectures/neural-architecture-design-as-a-compositional-32e --stage archive_sync --execute
  .venv/bin/python scripts/run_stage.py --package neural-architectures/neural-architecture-design-as-a-compositional-32e --stage essay_iteration --mark-done
"""

from __future__ import annotations

import argparse
import shlex
import string
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from audit_package import audit_package, print_report
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
    package_path = Path("publications") / package_key
    inferred = {
        "package_key": package_key,
        "package_name": package_path.name,
        "package_path": str(package_path),
        "publication": status_data.get("publication", package_path.name),
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


def format_context_item(item: str, resolved_args: dict) -> str:
    if item.startswith("config."):
        key = item.split(".", 1)[1]
        value = resolved_args.get(key)
        if value is None:
            return f"{item}: <missing>"
        return f"{item}: {value}"
    return item


def print_stage_summary(
    package_key: str,
    status_data: dict,
    stage: str,
    workflow_contract: dict,
    resolved_args: dict,
) -> None:
    metadata = workflow_contract["metadata"]
    stage_data = status_data.get("stages", {}).get(stage, {})
    workflow_relpath = workflow_contract["path"].relative_to(REPO_ROOT)

    print(f"PACKAGE: {package_key}")
    print(f"Publication: {status_data.get('publication', package_key)}")
    print(f"Stage: {stage}")
    print(f"Current State: done={stage_data.get('done', False)} last_updated={stage_data.get('last_updated')}")
    print(f"Workflow Doc: {workflow_relpath}")
    print(f"Runner Mode: {metadata['runner_mode']}")
    print(f"Default Skill: {metadata['default_skill'] or 'none'}")
    print(f"Approval Gate: {metadata['approval_gate']}")

    warnings = get_dependency_warnings(stage, status_data)
    if warnings:
        print("\nDependency Warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    print("\nRequired Context:")
    for item in metadata["required_context"]:
        print(f"  - {format_context_item(item, resolved_args)}")

    print("\nExpected Outputs:")
    for item in metadata["expected_outputs"]:
        print(f"  - {item}")

    print("\nDone When:")
    for item in metadata["done_when"]:
        print(f"  - {item}")

    if metadata["launch_templates"]:
        print("\nLaunch Templates:")
        for template in metadata["launch_templates"]:
            print(f"  - {template}")
    else:
        print("\nLaunch Templates: none")


def log_run(package_key: str, stage: str, action: str, success: bool, output: str, commands: list[str]) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    package_id = package_key.replace("/", "__")
    run_id = f"{timestamp}_{package_id}_{stage}_{action}"
    run_dir = Path("reviewable-runs/examples/proofs") / run_id
    packet_dir = run_dir / "review-packet"
    packet_dir.mkdir(parents=True, exist_ok=True)

    status_str = "SUCCESS" if success else "FAILURE"
    command_block = "\n".join(commands) if commands else "None"

    task_spec = f"""# Task Spec

## Run Type
Lifecycle Stage {action}: {stage}

## Objective
Process the '{stage}' stage for '{package_key}' using the '{action}' action.

## Success Criteria
- The requested action completes without error
- The resulting manifest state matches the runner mode contract
"""
    (packet_dir / "task-spec.md").write_text(task_spec)

    execution_trace = f"""# Execution Trace

1. Target package: {package_key}
2. Stage: {stage}
3. Action: {action}
4. Commands attempted:
```
{command_block}
```
5. Execution timestamp: {timestamp}

## Raw Output Snippet
```
{output[-4000:]}
```
"""
    (packet_dir / "execution-trace.md").write_text(execution_trace)

    verification_report = f"""# Verification Report

## Outcome
Status: {status_str}

## Details
Stage '{stage}' was processed for package '{package_key}' using action '{action}'.
"""
    (packet_dir / "verification-report.md").write_text(verification_report)

    readme = f"""# Run Record: {run_id}

- **Package**: {package_key}
- **Stage**: {stage}
- **Action**: {action}
- **Status**: {status_str}
- **Packet**: [review-packet/](review-packet/)
"""
    (run_dir / "README.md").write_text(readme)

    print(f"Reviewable Run recorded to {run_dir}")


def format_commands(templates: list[str], resolved_args: dict, passthrough_args: list[str]) -> list[str]:
    commands = []
    for template in templates:
        command = template.format(**resolved_args)
        if passthrough_args:
            command = f"{command} {shlex.join(passthrough_args)}"
        commands.append(command)
    return commands


def maybe_block_for_done_stage(args: argparse.Namespace, stage_data: dict, action_label: str) -> bool:
    if action_label == "execute" and stage_data.get("done") and not args.force:
        print("Stage is already marked done. Use --force to execute it again.")
        return True
    if action_label == "mark-done" and stage_data.get("done") and not args.force:
        print("Stage is already marked done. Use --force to update the timestamp anyway.")
        return True
    if action_label == "mark-undone" and not stage_data.get("done") and not args.force:
        print("Stage is already marked not done. Use --force to update the timestamp anyway.")
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve, execute, or update a publication lifecycle stage.")
    parser.add_argument("--package", required=True, help="Package path relative to publications/")
    parser.add_argument("--stage", required=True, choices=STAGES, help="Stage to inspect or mutate")
    parser.add_argument("--strict-deps", action="store_true", help="Block execute/mark-done when dependencies are not done")
    parser.add_argument("--force", action="store_true", help="Allow reruns or redundant state changes")
    parser.add_argument("--execute", action="store_true", help="Execute launch templates for scripted or hybrid stages")
    parser.add_argument("--mark-done", action="store_true", help="Mark the stage as done without executing a command")
    parser.add_argument("--mark-undone", action="store_true", help="Mark the stage as not done")
    args, unknown = parser.parse_known_args()

    try:
        enforce_single_mutation(args)
        manifest_ref, status_data = load_status_ref(args.package)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    try:
        workflow_contract = load_workflow_contract(args.stage)
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    extra_args = parse_extra_args(unknown)
    resolved_args = resolve_args(manifest_ref.package_key, status_data, extra_args)
    print_stage_summary(manifest_ref.package_key, status_data, args.stage, workflow_contract, resolved_args)

    try:
        report = audit_package(manifest_ref.package_key)
        print()
        print_report(report)
    except Exception as exc:
        print(f"\n[WARNING] Pre-flight audit failed to run: {exc}")

    stage_data = status_data.setdefault("stages", {}).setdefault(
        args.stage,
        {"done": False, "last_updated": None},
    )
    warnings = get_dependency_warnings(args.stage, status_data)
    if args.strict_deps and warnings and (args.execute or args.mark_done):
        print("\nERROR: Dependency check failed with --strict-deps enabled.")
        for warning in warnings:
            print(f"  - {warning}")
        sys.exit(1)

    if not any([args.execute, args.mark_done, args.mark_undone]):
        return

    metadata = workflow_contract["metadata"]
    if args.execute:
        if maybe_block_for_done_stage(args, stage_data, "execute"):
            return
        if metadata["runner_mode"] == "guided":
            print("ERROR: Guided stages do not support --execute. Resolve the stage and use --mark-done after completing the work.")
            sys.exit(1)
        if not metadata["launch_templates"]:
            print("ERROR: This stage has no launch templates to execute.")
            sys.exit(1)

        try:
            passthrough_args = filter_passthrough_args(
                unknown,
                extract_template_fields(metadata["launch_templates"]),
            )
            commands = format_commands(metadata["launch_templates"], resolved_args, passthrough_args)
        except KeyError as exc:
            print(f"ERROR: Missing required parameter {exc} for stage '{args.stage}'.")
            print("Provide it through status.yaml config or pass the corresponding CLI flag.")
            sys.exit(1)

        outputs = []
        success = True
        for command in commands:
            print(f"\nExecuting: {command}")
            process = subprocess.run(command, shell=True, capture_output=True, text=True)
            snippet = process.stdout + ("\n" if process.stdout and process.stderr else "") + process.stderr
            outputs.append(f"$ {command}\n{snippet}")
            if process.returncode != 0:
                success = False
                print(process.stderr or process.stdout)
                break

        output = "\n\n".join(outputs)
        if success:
            if metadata["runner_mode"] == "scripted":
                stage_data["done"] = True
                stage_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
                save_status(manifest_ref.package_path, status_data)
                print("Stage executed successfully and was marked done.")
            else:
                print("Stage executed successfully. Review the outcome, then use --mark-done when you want to close it.")
        else:
            print("Stage execution failed.")

        log_run(manifest_ref.package_key, args.stage, "execute", success, output, commands)
        if not success:
            sys.exit(1)
        return

    if args.mark_done:
        if maybe_block_for_done_stage(args, stage_data, "mark-done"):
            return
        stage_data["done"] = True
        stage_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        save_status(manifest_ref.package_path, status_data)
        message = f"Stage '{args.stage}' marked done for '{manifest_ref.package_key}'."
        print(message)
        log_run(manifest_ref.package_key, args.stage, "mark-done", True, message, [])
        return

    if args.mark_undone:
        if maybe_block_for_done_stage(args, stage_data, "mark-undone"):
            return
        stage_data["done"] = False
        stage_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        save_status(manifest_ref.package_path, status_data)
        message = f"Stage '{args.stage}' marked not done for '{manifest_ref.package_key}'."
        print(message)
        log_run(manifest_ref.package_key, args.stage, "mark-undone", True, message, [])
        return


if __name__ == "__main__":
    main()
