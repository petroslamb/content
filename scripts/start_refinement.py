#!/usr/bin/env python3
"""
Start a new refinement cycle for a publication package.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime

from lifecycle import REPO_ROOT, STAGES, load_status_ref, save_status


def main() -> None:
    parser = argparse.ArgumentParser(description="Start a refinement cycle for a publication package.")
    parser.add_argument("--package", required=True, help="Package path relative to publications/")
    parser.add_argument(
        "--reset",
        required=True,
        help="Comma-separated stages to reset (e.g. research,essay_iteration,substack_publishing)",
    )
    parser.add_argument("--slug", help="Substack slug for archive sync when bootstrapping from an umbrella package")
    parser.add_argument("--no-sync", action="store_true", help="Skip the archive sync step")
    args = parser.parse_args()

    stages_to_reset = [stage.strip() for stage in args.reset.split(",") if stage.strip()]
    invalid = [stage for stage in stages_to_reset if stage not in STAGES]
    if invalid:
        print(f"ERROR: Invalid stage(s): {', '.join(invalid)}")
        print(f"Valid stages: {', '.join(STAGES)}")
        sys.exit(1)

    try:
        manifest_ref, status_data = load_status_ref(args.package)
    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)

    if not args.no_sync:
        print("=" * 60)
        print("Step 1: Syncing from archive...")
        print("=" * 60)
        sync_cmd = [
            sys.executable,
            str(REPO_ROOT / "scripts" / "sync_from_archive.py"),
            "--package",
            manifest_ref.package_key,
        ]
        if args.slug:
            sync_cmd.extend(["--slug", args.slug])

        result = subprocess.run(sync_cmd, cwd=str(REPO_ROOT))
        if result.returncode != 0:
            print("WARNING: Archive sync failed or was skipped. Continuing with existing package state.")
        print()

        _, status_data = load_status_ref(manifest_ref.package_key)

    current_revision = status_data.get("revision", 1)
    new_revision = current_revision + 1
    status_data["revision"] = new_revision

    print("=" * 60)
    print(f"Step 2: Starting refinement cycle (rev {current_revision} -> {new_revision})")
    print("=" * 60)

    for stage in stages_to_reset:
        stage_data = status_data.setdefault("stages", {}).setdefault(stage, {"done": False, "last_updated": None})
        was_done = stage_data.get("done", False)
        stage_data["done"] = False
        stage_data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        marker = " (was done)" if was_done else " (was already not done)"
        print(f"  Reset: {stage}{marker}")

    kept = [
        stage
        for stage in STAGES
        if stage not in stages_to_reset and status_data.get("stages", {}).get(stage, {}).get("done", False)
    ]
    if kept:
        print()
        print(f"  Kept as done: {', '.join(kept)}")

    save_status(manifest_ref.package_path, status_data)
    print(f"\n  Revision bumped to {new_revision}")
    print(f"  Status saved: {manifest_ref.status_path}")

    print()
    print("=" * 60)
    print("Refinement cycle started. Next steps:")
    print("=" * 60)
    for stage in stages_to_reset:
        print(f"  npm run run -- --package {manifest_ref.package_key} --stage {stage}")


if __name__ == "__main__":
    main()
