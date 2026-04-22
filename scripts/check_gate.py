#!/usr/bin/env python3
"""Evaluate a first-class workflow gate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from harness import evaluate_gate, log_gate_check
from lifecycle import REPO_ROOT


def resolve_packet_path(packet_arg: str | None) -> Path | None:
    if not packet_arg:
        return None
    candidate = Path(packet_arg)
    if not candidate.is_absolute():
        candidate = (REPO_ROOT / packet_arg).resolve()
    return candidate


def print_gate_result(result: dict, log_path: str) -> None:
    print(f"Gate: {result['gate_id']}")
    print(f"Status: {result['status']}")
    print(f"Decision: {result['decision']}")
    print(f"Blocking: {result['blocking']}")
    print(f"Recommended Workflow: {result['recommended_workflow']}")
    print(f"Recommended Validator: {result['recommended_validator']}")
    print(f"Proof Mode: {result['proof_mode']}")
    print(f"Log: {log_path}")

    if result["missing_artifacts"]:
        print("\nMissing Artifacts:")
        for item in result["missing_artifacts"]:
            print(f"  - {item}")

    if result.get("details"):
        print("\nDetails:")
        for key, value in result["details"].items():
            if value in (None, "", []):
                continue
            print(f"  - {key}: {value}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate a first-class workflow gate.")
    parser.add_argument("--gate", required=True, help="Gate id from gate_contracts.yaml")
    parser.add_argument("--package", help="Package path relative to publications/")
    parser.add_argument("--packet", help="Packet path for packet-scoped gates.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    packet_path = resolve_packet_path(args.packet)
    try:
        result = evaluate_gate(args.gate, package_arg=args.package, packet_path=packet_path)
        log_path = log_gate_check(result, args.package, packet_path)
    except (FileNotFoundError, ValueError, KeyError) as exc:
        payload = {"error": str(exc)}
        if args.format == "json":
            print(json.dumps(payload, indent=2))
        else:
            print(f"ERROR: {exc}")
        sys.exit(1)

    payload = {**result, "log_path": log_path}
    if args.format == "json":
        print(json.dumps(payload, indent=2))
        if result["blocking"]:
            sys.exit(1)
        return

    print_gate_result(result, log_path)
    if result["blocking"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
