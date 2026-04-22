#!/usr/bin/env python3
"""
Resolve the next valid lifecycle action for a package.
"""

from __future__ import annotations

import argparse
import json
import sys

from harness import build_stage_resolution, next_stage_for_package
from lifecycle import load_status_ref


def build_next_action(package_arg: str) -> dict:
    manifest_ref, status_data = load_status_ref(package_arg)
    next_stage = next_stage_for_package(manifest_ref.package_path, status_data)
    base = {
        "package": manifest_ref.package_key,
        "revision": status_data.get("revision", 1),
        "all_stages_complete": next_stage is None,
        "next_stage": next_stage,
        "runner_mode": None,
        "approval_gate": None,
        "requires_approval": False,
        "can_execute": False,
        "blocking_issues": [],
        "required_context": [],
        "suggested_commands": [],
        "log_target": "reviewable-runs/logs/",
        "packet_phase": None,
        "next_packet_action": None,
        "recommended_validator": None,
        "pipeline_profile": None,
        "recommended_workflows": [],
        "gate_statuses": {},
        "overlay_candidates": [],
        "effective_workflow": None,
        "effective_workflow_kind": None,
        "effective_workflow_doc": None,
        "effective_next_action": None,
        "effective_route": None,
        "effective_can_execute": False,
        "effective_requires_approval": False,
        "effective_approval_gate": None,
        "active_overlay": None,
        "overlay_phase": None,
        "next_overlay_action": None,
        "overlay_route": None,
        "overlay_recommended_validator": None,
        "active_overlay_root": None,
    }
    if next_stage is None:
        return base

    resolution = build_stage_resolution(package_arg, next_stage)
    return {
        **base,
        "runner_mode": resolution["runner_mode"],
        "approval_gate": resolution["approval_gate"],
        "requires_approval": resolution["requires_approval"],
        "can_execute": resolution["can_execute"],
        "blocking_issues": resolution["blocking_issues"],
        "required_context": resolution["required_context"],
        "suggested_commands": resolution["suggested_commands"],
        "log_target": resolution["log_target"],
        "packet_phase": resolution.get("packet_phase"),
        "next_packet_action": resolution.get("next_packet_action"),
        "recommended_validator": resolution.get("recommended_validator"),
        "pipeline_profile": resolution.get("pipeline_profile"),
        "recommended_workflows": resolution.get("recommended_workflows", []),
        "gate_statuses": resolution.get("gate_statuses", {}),
        "overlay_candidates": resolution.get("overlay_candidates", []),
        "effective_workflow": resolution.get("effective_workflow"),
        "effective_workflow_kind": resolution.get("effective_workflow_kind"),
        "effective_workflow_doc": resolution.get("effective_workflow_doc"),
        "effective_next_action": resolution.get("effective_next_action"),
        "effective_route": resolution.get("effective_route"),
        "effective_can_execute": resolution.get("effective_can_execute"),
        "effective_requires_approval": resolution.get("effective_requires_approval"),
        "effective_approval_gate": resolution.get("effective_approval_gate"),
        "active_overlay": resolution.get("active_overlay"),
        "overlay_phase": resolution.get("overlay_phase"),
        "next_overlay_action": resolution.get("next_overlay_action"),
        "overlay_route": resolution.get("overlay_route"),
        "overlay_recommended_validator": resolution.get("overlay_recommended_validator"),
        "active_overlay_root": resolution.get("active_overlay_root"),
    }


def print_text(payload: dict) -> None:
    print(f"PACKAGE: {payload['package']}")
    print(f"Revision: {payload['revision']}")
    print(f"All Stages Complete: {payload['all_stages_complete']}")
    print(f"Compatibility Stage: {payload['next_stage']}")
    if payload["next_stage"] is None:
        return
    print(f"Runner Mode: {payload['runner_mode']}")
    print(f"Approval Gate: {payload['approval_gate']}")
    print(f"Requires Approval: {payload['requires_approval']}")
    print(f"Can Execute: {payload['can_execute']}")
    print(f"Pipeline Profile: {payload.get('pipeline_profile')}")
    if payload.get("effective_workflow"):
        print(f"Effective Workflow: {payload.get('effective_workflow')}")
        print(f"Effective Kind: {payload.get('effective_workflow_kind')}")
        print(f"Effective Can Execute: {payload.get('effective_can_execute')}")
        print(f"Effective Approval Gate: {payload.get('effective_approval_gate')}")
        print(f"Effective Requires Approval: {payload.get('effective_requires_approval')}")
        print(f"Effective Next Action: {payload.get('effective_next_action')}")
        if payload.get("effective_route"):
            print(f"Effective Route: {payload.get('effective_route')}")

    if payload.get("packet_phase"):
        print(f"Packet Phase: {payload['packet_phase']}")
        print(f"Next Packet Action: {payload.get('next_packet_action')}")
        print(f"Recommended Validator: {payload.get('recommended_validator')}")

    if payload.get("recommended_workflows"):
        print("\nRecommended Workflows:")
        for workflow_id in payload["recommended_workflows"]:
            print(f"  - {workflow_id}")

    if payload.get("overlay_candidates"):
        print("\nOverlay Candidates:")
        for workflow_id in payload["overlay_candidates"]:
            print(f"  - {workflow_id}")

    if payload.get("active_overlay"):
        print(f"\nActive Overlay: {payload['active_overlay']}")
        print(f"Overlay Root: {payload.get('active_overlay_root')}")
        print(f"Overlay Phase: {payload.get('overlay_phase')}")
        print(f"Next Overlay Action: {payload.get('next_overlay_action')}")
        if payload.get("overlay_route"):
            print(f"Overlay Route: {payload.get('overlay_route')}")
        print(f"Overlay Validator: {payload.get('overlay_recommended_validator')}")

    if payload.get("gate_statuses"):
        print("\nGate Statuses:")
        for gate_id, gate_status in payload["gate_statuses"].items():
            print(f"  - {gate_id}: {gate_status.get('status')} ({gate_status.get('decision')})")

    if payload["blocking_issues"]:
        print("\nBlocking Issues:")
        for issue in payload["blocking_issues"]:
            print(f"  - {issue}")

    print("\nRequired Context:")
    for item in payload["required_context"]:
        value = item.get("value")
        if value is None:
            print(f"  - {item['name']}: {item['status']}")
        else:
            print(f"  - {item['name']}: {item['status']} ({value})")

    print("\nSuggested Commands:")
    for command in payload["suggested_commands"]:
        print(f"  - {command}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve the next valid lifecycle action for a package.")
    parser.add_argument("--package", required=True, help="Package path relative to publications/")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    try:
        payload = build_next_action(args.package)
    except (FileNotFoundError, ValueError, KeyError) as exc:
        if args.format == "json":
            print(json.dumps({"error": str(exc)}, indent=2))
        else:
            print(f"ERROR: {exc}")
        sys.exit(1)

    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return
    print_text(payload)


if __name__ == "__main__":
    main()
