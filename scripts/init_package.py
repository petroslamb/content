#!/usr/bin/env python3
"""
Initialize a minimal publication package from an idea.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from harness import initialize_package
from lifecycle import REPO_ROOT


def resolve_topic_packet_path(packet_arg: str | None) -> Path | None:
    if not packet_arg:
        return None
    candidate = Path(packet_arg)
    if not candidate.is_absolute():
        candidate = (REPO_ROOT / packet_arg).resolve()
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a minimal publication package from an idea.")
    parser.add_argument("--idea", help="Idea or working thesis for the new package.")
    parser.add_argument("--slug", help="Optional package slug. If omitted, derive one from the idea.")
    parser.add_argument("--from-topic-packet", help="Canonical topic-discovery packet to hand off into package init.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args()

    if not args.idea and not args.from_topic_packet:
        parser.error("Provide --idea or --from-topic-packet.")

    try:
        payload = initialize_package(
            args.idea,
            args.slug,
            topic_packet_path=resolve_topic_packet_path(args.from_topic_packet),
        )
    except (ValueError, FileExistsError) as exc:
        if args.format == "json":
            print(json.dumps({"error": str(exc)}, indent=2))
        else:
            print(f"ERROR: {exc}")
        sys.exit(1)

    if args.format == "json":
        print(json.dumps(payload, indent=2))
        return

    print(f"Initialized package: {payload['package_path']}")
    print(f"Live draft: {payload['markdown_path']}")
    print(f"Status: {payload['status_path']}")
    print(f"Next stage: {payload['next_stage']}")
    print(f"Suggested command: {payload['suggested_command']}")


if __name__ == "__main__":
    main()
