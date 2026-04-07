#!/usr/bin/env python3
"""
Start Refinement: Begin a new refinement cycle for a publication package.

Bumps the revision counter, selectively resets specified stages,
and optionally syncs the archive snapshot into the package.

Usage:
  .venv/bin/python scripts/start_refinement.py --package neural-architectures --reset research,essay_iteration --slug neural-architecture-design-as-a-compositional-32e
"""

import argparse
import subprocess
import sys
import yaml
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLICATIONS_DIR = REPO_ROOT / "publications"

# Import STAGES from the runner for validation
sys.path.insert(0, str(Path(__file__).parent))
from run_stage import STAGES


def load_status(package_path):
    status_path = package_path / "status.yaml"
    if not status_path.exists():
        return None
    with open(status_path) as f:
        return yaml.safe_load(f)


def save_status(package_path, data):
    status_path = package_path / "status.yaml"
    with open(status_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def main():
    parser = argparse.ArgumentParser(description="Start a refinement cycle for a publication package.")
    parser.add_argument("--package", required=True, help="Package name (e.g., neural-architectures)")
    parser.add_argument("--reset", required=True,
                        help="Comma-separated stages to reset (e.g., research,essay_iteration,substack_publishing)")
    parser.add_argument("--slug", help="Substack slug for archive sync (required for umbrella packages)")
    parser.add_argument("--no-sync", action="store_true",
                        help="Skip the archive sync step (start from existing package draft)")
    args = parser.parse_args()

    package_path = PUBLICATIONS_DIR / args.package
    if not package_path.exists():
        print(f"ERROR: Package not found: {package_path}")
        sys.exit(1)

    # Validate stages
    stages_to_reset = [s.strip() for s in args.reset.split(",")]
    invalid = [s for s in stages_to_reset if s not in STAGES]
    if invalid:
        print(f"ERROR: Invalid stage(s): {', '.join(invalid)}")
        print(f"Valid stages: {', '.join(STAGES)}")
        sys.exit(1)

    status_data = load_status(package_path)
    if not status_data:
        print(f"ERROR: No status.yaml found for package '{args.package}'")
        sys.exit(1)

    # 1. Sync from archive (unless --no-sync)
    if not args.no_sync:
        print("=" * 60)
        print("Step 1: Syncing from archive...")
        print("=" * 60)
        sync_cmd = [
            sys.executable, str(REPO_ROOT / "scripts" / "sync_from_archive.py"),
            "--package", args.package,
        ]
        if args.slug:
            sync_cmd.extend(["--slug", args.slug])

        result = subprocess.run(sync_cmd, cwd=str(REPO_ROOT))
        if result.returncode != 0:
            print("WARNING: Archive sync failed or was skipped. Continuing with existing package state.")
        print()

        # Reload status (sync_from_archive may have updated config)
        status_data = load_status(package_path)

    # 2. Bump revision
    current_rev = status_data.get("revision", 1)
    new_rev = current_rev + 1
    status_data["revision"] = new_rev

    # 3. Reset specified stages
    print("=" * 60)
    print(f"Step 2: Starting refinement cycle (rev {current_rev} → {new_rev})")
    print("=" * 60)

    for stage in stages_to_reset:
        if stage in status_data.get("stages", {}):
            was_done = status_data["stages"][stage].get("done", False)
            status_data["stages"][stage]["done"] = False
            status_data["stages"][stage]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            marker = " (was done)" if was_done else " (was already not done)"
            print(f"  Reset: {stage}{marker}")
        else:
            print(f"  WARNING: Stage '{stage}' not found in status.yaml, skipping")

    # Show what's kept
    print()
    kept = [s for s in STAGES if s not in stages_to_reset
            and status_data.get("stages", {}).get(s, {}).get("done", False)]
    if kept:
        print(f"  Kept as done: {', '.join(kept)}")

    # 4. Save
    save_status(package_path, status_data)
    print(f"\n  Revision bumped to {new_rev}")
    print(f"  Status saved: {package_path / 'status.yaml'}")

    # 5. Summary
    print()
    print("=" * 60)
    print("Refinement cycle started. Next steps:")
    print("=" * 60)
    for stage in stages_to_reset:
        print(f"  npm run run -- --package {args.package} --stage {stage}")
    print()
    print("  Stages can be run in any order. The runner will warn about")
    print("  upstream dependencies but will not block execution.")


if __name__ == "__main__":
    main()
