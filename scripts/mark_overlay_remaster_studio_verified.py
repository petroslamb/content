#!/usr/bin/env python3
"""Mark overlay-remaster items as Studio related-video verified."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mark remastered Shorts as Studio-verified.")
    parser.add_argument("--crosswalk", type=Path, required=True)
    parser.add_argument("--new-video-id", action="append", default=[], help="New remaster video ID to mark verified. Repeatable.")
    parser.add_argument("--all", action="store_true", help="Mark every remaster in the crosswalk verified.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.all and not args.new_video_id:
        raise SystemExit("Provide --all or at least one --new-video-id.")
    wanted = set(args.new_video_id)
    crosswalk = load_json(args.crosswalk)
    marked = []
    for item in crosswalk.get("items", []):
        if args.all or item.get("new_video_id") in wanted:
            item["studio_related_verified"] = True
            marked.append(
                {
                    "package_key": item["package_key"],
                    "slug": item["slug"],
                    "new_video_id": item.get("new_video_id"),
                }
            )
    crosswalk["updated_at"] = datetime.now(timezone.utc).isoformat()
    write_json(args.crosswalk, crosswalk)
    print(json.dumps({"crosswalk": str(args.crosswalk), "marked": marked}, indent=2))


if __name__ == "__main__":
    main()
