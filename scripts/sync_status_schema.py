#!/usr/bin/env python3
"""
Sync status.yaml manifests with the latest lifecycle stage list.
Adds missing stages and the leaf-manifest defaults used by the runner.
"""

from __future__ import annotations

from lifecycle import STAGES, iter_status_refs, load_status, save_status


def main() -> None:
    refs = iter_status_refs()
    print(f"Syncing schema for {len(refs)} manifests...")

    for ref in refs:
        data = load_status(ref.package_path)
        if not data:
            continue

        updated = False
        if "kind" not in data:
            data["kind"] = "leaf"
            updated = True

        if "publication" not in data:
            data["publication"] = ref.package_path.name
            updated = True

        if len(ref.package_key.split("/")) > 1 and "parent_package" not in data:
            data["parent_package"] = ref.package_key.split("/", 1)[0]
            updated = True

        stages = data.setdefault("stages", {})
        for stage in STAGES:
            if stage not in stages:
                stages[stage] = {"done": False, "last_updated": None}
                print(f"  [{ref.package_key}] Added missing stage: {stage}")
                updated = True

        if updated:
            save_status(ref.package_path, data)

    print("\nSchema sync complete.")


if __name__ == "__main__":
    main()
