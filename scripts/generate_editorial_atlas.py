from __future__ import annotations

import argparse
import json

from editorial_atlas_utils import (
    ATLAS_DATA_PATH,
    RUBRIC_ASSESSMENTS_PATH,
    build_editorial_atlas_data,
    ensure_checked_in_atlas_matches_generated,
    render_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate publication_strategy_and_archive/editorial_atlas/atlas_data.json from rubric assessments."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate that the checked-in atlas_data.json matches the rubric source without writing changes.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.check:
        atlas = ensure_checked_in_atlas_matches_generated()
        print(
            json.dumps(
                {
                    "checked": str(ATLAS_DATA_PATH),
                    "source": str(RUBRIC_ASSESSMENTS_PATH),
                    "essays": len(atlas["essays"]),
                    "drafts": len(atlas["drafts"]),
                },
                indent=2,
            )
        )
        return

    atlas = build_editorial_atlas_data()
    ATLAS_DATA_PATH.write_text(render_json(atlas), encoding="utf-8")
    print(
        json.dumps(
            {
                "wrote": str(ATLAS_DATA_PATH),
                "source": str(RUBRIC_ASSESSMENTS_PATH),
                "essays": len(atlas["essays"]),
                "drafts": len(atlas["drafts"]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
