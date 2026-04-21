#!/usr/bin/env python3
"""
Display a lifecycle table for all runnable leaf packages discovered recursively
under publications/.
"""

from __future__ import annotations

from lifecycle import STAGES, iter_leaf_status_refs
from package_lifecycle import inspect_package_lifecycle


def main() -> None:
    manifests = sorted(iter_leaf_status_refs(), key=lambda item: item[0].package_key)
    if not manifests:
        print("No runnable leaf status.yaml files found under publications/.")
        return

    package_width = max(max(len(ref.package_key) for ref, _ in manifests), len("Package"))

    header = f"{'Package':<{package_width}} | rev | wrn | "
    divider = f"{'-' * package_width}-|-----|-----|-"
    for stage in STAGES:
        short_name = "".join(part[0] for part in stage.split("_"))
        header += f"{short_name:^3} | "
        divider += f"{'-' * 3}-|-"

    print(header)
    print(divider)

    warning_summary: list[tuple[str, int]] = []
    for ref, status_data in manifests:
        revision = status_data.get("revision", 1)
        lifecycle_report = inspect_package_lifecycle(ref.package_key)
        warning_count = lifecycle_report["warning_count"]
        warning_marker = str(warning_count) if warning_count else "."
        if warning_count:
            warning_summary.append((ref.package_key, warning_count))
        row = f"{ref.package_key:<{package_width}} | {revision:>3} | {warning_marker:^3} | "
        for stage in STAGES:
            stage_data = status_data.get("stages", {}).get(stage, {})
            icon = "[x]" if stage_data.get("done", False) else "[ ]"
            row += f"{icon:^3} | "
        print(row)

    print("\nLegend:")
    print("  wrn: lifecycle warning count ('.' means none)")
    for stage in STAGES:
        short_name = "".join(part[0] for part in stage.split("_"))
        print(f"  {short_name}: {stage.replace('_', ' ').title()}")

    if warning_summary:
        print("\nLifecycle warnings:")
        for package_key, warning_count in warning_summary:
            print(f"  {package_key}: {warning_count}")


if __name__ == "__main__":
    main()
