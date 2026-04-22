#!/usr/bin/env python3
"""Resolve or run a generic workflow module/overlay/stage."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

from harness import (
    build_workflow_resolution,
    emit_workflow_launch_pack,
    log_workflow_run,
)
from lifecycle import REPO_ROOT


def resolve_packet_path(packet_arg: str | None) -> Path | None:
    if not packet_arg:
        return None
    candidate = Path(packet_arg)
    if not candidate.is_absolute():
        candidate = (REPO_ROOT / packet_arg).resolve()
    return candidate


def append_passthrough(commands: list[str], passthrough: list[str]) -> list[str]:
    if not passthrough:
        return commands
    suffix = shlex.join(passthrough)
    return [f"{command} {suffix}" for command in commands]


def print_workflow_resolution(resolution: dict, launch_pack_path: str | None) -> None:
    print(f"Workflow: {resolution['workflow_id']}")
    print(f"Kind: {resolution['workflow_kind']}")
    print(f"Stability: {resolution['stability']}")
    print(f"Package: {resolution.get('package') or 'none'}")
    print(f"Workflow Doc: {resolution['workflow_doc']}")
    print(f"Approval Gate: {resolution['approval_gate']}")
    print(f"Requires Approval: {resolution['requires_approval']}")
    print(f"Can Execute: {resolution['can_execute']}")
    print(f"Recommended Gates: {', '.join(resolution['recommended_gates']) or 'none'}")
    if resolution.get("overlay_phase"):
        print(f"Overlay Phase: {resolution.get('overlay_phase')}")
        print(f"Next Overlay Action: {resolution.get('next_overlay_action')}")
        print(f"Overlay Validator: {resolution.get('recommended_validator')}")
        print(f"Active Overlay Root: {resolution.get('active_overlay_root')}")
    if launch_pack_path:
        print(f"Launch Pack: {launch_pack_path}")

    if resolution["blocking_issues"]:
        print("\nBlocking Issues:")
        for issue in resolution["blocking_issues"]:
            print(f"  - {issue}")

    print("\nRequired Context:")
    for item in resolution["required_context"]:
        value = item.get("value")
        if value is None:
            print(f"  - {item['name']}: {item['status']}")
        else:
            print(f"  - {item['name']}: {item['status']} ({value})")

    if resolution.get("topic_packet_details"):
        print("\nTopic Packet:")
        for key, value in resolution["topic_packet_details"].items():
            if value in (None, "", []):
                continue
            print(f"  - {key}: {value}")

    print("\nSuggested Commands:")
    for command in resolution["suggested_commands"]:
        print(f"  - {command}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve or run a generic workflow.")
    parser.add_argument("--workflow", required=True, help="Tracked workflow id.")
    parser.add_argument("--package", help="Package path relative to publications/")
    parser.add_argument("--packet", help="Optional packet path for pre-package workflows such as topic discovery.")
    parser.add_argument("--emit-launch-pack", action="store_true", help="Write a workflow launch pack log.")
    parser.add_argument("--execute", action="store_true", help="Execute rendered launch templates when supported.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args, unknown = parser.parse_known_args()

    packet_path = resolve_packet_path(args.packet)

    try:
        resolution = build_workflow_resolution(
            args.workflow,
            package_arg=args.package,
            packet_path=packet_path,
        )
    except (FileNotFoundError, ValueError, KeyError) as exc:
        payload = {"error": str(exc)}
        if args.format == "json":
            print(json.dumps(payload, indent=2))
        else:
            print(f"ERROR: {exc}")
        sys.exit(1)

    launch_pack_path = None
    if args.emit_launch_pack or (args.execute and not resolution["can_execute"]):
        launch_pack = emit_workflow_launch_pack(resolution)
        launch_pack_path = str(launch_pack.relative_to(REPO_ROOT))
        log_workflow_run(
            resolution,
            "emit_launch_pack",
            True,
            f"Launch pack written to {launch_pack_path}",
            resolution["launch_templates"],
        )

    execution_output = None
    if args.execute and resolution["can_execute"] and resolution["launch_templates"]:
        commands = append_passthrough(list(resolution["launch_templates"]), unknown)
        outputs: list[str] = []
        success = True
        for command in commands:
            proc = subprocess.run(
                command,
                shell=True,
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            )
            outputs.append(f"$ {command}\n{proc.stdout}{proc.stderr}")
            if proc.returncode != 0:
                success = False
                break
        execution_output = "\n".join(outputs)
        log_path = log_workflow_run(resolution, "execute", success, execution_output, commands)
        payload = {
            "success": success,
            "workflow_id": resolution["workflow_id"],
            "package": resolution.get("package"),
            "commands": commands,
            "log_path": log_path,
            "output": execution_output,
        }
        if args.format == "json":
            print(json.dumps(payload, indent=2))
        else:
            print(execution_output)
            print(f"\nWorkflow log: {log_path}")
        if not success:
            sys.exit(1)
        return

    payload = {
        **resolution,
        "launch_pack_path": launch_pack_path,
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return
    print_workflow_resolution(resolution, launch_pack_path)


if __name__ == "__main__":
    main()
