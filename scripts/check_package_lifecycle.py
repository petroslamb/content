#!/usr/bin/env python3
"""
Check lifecycle guardrails for one leaf publication package.
"""

from __future__ import annotations

import argparse
import json
import sys

from package_lifecycle import inspect_package_lifecycle


def print_report(report: dict) -> None:
    print(f"LIFECYCLE CHECK: {report['package']}")
    print(f"Current stage: {report['current_stage'] or 'complete'}")
    print(f"README stage: {report['readme_current_stage'] or 'missing'}")
    print(
        "Governing brief: "
        + (
            f"{report['governing_brief_path']} ({report['governing_brief_source']})"
            if report["governing_brief_path"]
            else "unresolved"
        )
    )
    print(
        "Packet scaffold: "
        + (
            report["packet_manifest_path"]
            if report["packet_scaffold_exists"] and report["packet_manifest_path"]
            else "missing"
        )
    )
    if not report["issues"]:
        print("No lifecycle warnings.")
        return

    print("Warnings:")
    for issue in report["issues"]:
        marker = "BLOCK" if issue["blocking"] else "WARN"
        print(f"  [{marker}] {issue['message']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check lifecycle guardrails for one package.")
    parser.add_argument("--package", required=True, help="Leaf package path relative to publications/")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    try:
        report = inspect_package_lifecycle(args.package)
    except (FileNotFoundError, ValueError) as exc:
        if args.format == "json":
            print(json.dumps({"success": False, "error": str(exc)}, indent=2))
        else:
            print(f"ERROR: {exc}")
        sys.exit(1)

    payload = {
        "success": True,
        **report,
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
