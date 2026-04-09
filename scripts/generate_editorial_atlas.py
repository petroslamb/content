from __future__ import annotations

import argparse
import json

from editorial_atlas_utils import (
    ATLAS_DATA_PATH,
    DIMENSIONS,
    EDITORIAL_ATLAS_DIR,
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
        models = atlas.get("models", {})
        print(
            json.dumps(
                {
                    "checked": str(ATLAS_DATA_PATH),
                    "models": list(models.keys()),
                    "essays_per_model": {m: len(models[m]["essays"]) for m in models},
                },
                indent=2,
            )
        )
        return

    rubric_paths = sorted(EDITORIAL_ATLAS_DIR.glob("rubric_assessments_*.yaml"))
    
    combined_atlas = {
        "models": {},
        "defaultModel": "",
        "dimensions": DIMENSIONS
    }
    
    for path in rubric_paths:
        if path.name == "rubric_assessments_template.yaml":
            continue
            
        model_id = path.stem.replace("rubric_assessments_", "").replace("_", "-")
        try:
            atlas_node = build_editorial_atlas_data(rubric_path=path)
            if not atlas_node:
                continue
            combined_atlas["models"][model_id] = atlas_node
        except SystemExit as e:
            print(f"Skipping model {model_id} due to incomplete audit: {e}")
            continue
            
    if "gpt-5-4-xhigh" in combined_atlas["models"]:
        combined_atlas["defaultModel"] = "gpt-5-4-xhigh"
    elif rubric_paths:
        combined_atlas["defaultModel"] = rubric_paths[0].stem.replace("rubric_assessments_", "").replace("_", "-")
            
    ATLAS_DATA_PATH.write_text(render_json(combined_atlas), encoding="utf-8")
    
    print(
        json.dumps(
            {
                "wrote": str(ATLAS_DATA_PATH),
                "models_included": list(combined_atlas["models"].keys()),
                "total_models": len(combined_atlas["models"]),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
