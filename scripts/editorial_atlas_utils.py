from __future__ import annotations

import difflib
import json
import math
from pathlib import Path
from typing import Any

import yaml

from archive_utils import METADATA_PATH

REPO_ROOT = Path(__file__).resolve().parents[1]
EDITORIAL_ATLAS_DIR = REPO_ROOT / "publication_strategy_and_archive" / "editorial_atlas"
RUBRIC_ASSESSMENTS_PATH = EDITORIAL_ATLAS_DIR / "rubric_assessments.yaml"
ATLAS_DATA_PATH = EDITORIAL_ATLAS_DIR / "atlas_data.json"

DIMENSIONS = {
    "whole_essay": [
        "traction",
        "craft",
        "publication_power",
        "debate",
        "precision",
        "synthesis",
        "utility",
    ],
    "section": [
        "opening",
        "thesis_lock",
        "development",
        "borders",
        "ending",
        "reference_handling",
    ],
}

DIRECT_KEYS = ("debate", "precision", "synthesis", "utility")
TRACTION_KEYS = (
    "hook_strength",
    "thesis_compression",
    "frame_portability",
    "audience_breadth",
    "debate_energy",
    "public_packaging",
)
CRAFT_KEYS = (
    "sentence_rhythm",
    "paragraph_control",
    "structural_pacing",
    "evidence_integration",
    "ending_strength",
)
SECTION_KEYS = (
    "opening",
    "thesis_lock",
    "development",
    "borders",
    "ending",
    "reference_handling",
)
POSITION_KEYS = ("traction", "craft", "debate", "precision", "synthesis", "utility")
SECTION_LABELS = {
    "Opening",
    "Thesis Lock",
    "Development",
    "Borders / Counterpressure",
    "Ending",
    "Reference Handling",
}
KNOWN_MOVE_IDS = {
    "failure_or_anomaly_cold_open",
    "contrarian_compression",
    "coined_frame_with_borders",
    "scroll_map",
    "builder_first_doctrine",
    "historical_synthesis",
    "practical_heuristic_section",
    "falsifiable_prediction_close",
    "topical_narrative_hijack",
    "series_packaging",
    "chapterized_technical_explainer",
    "doctrine_ending",
}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}
ALLOWED_RUBRIC_STATUS = {"migrated", "audited"}


def load_metadata() -> list[dict[str, Any]]:
    return json.loads(METADATA_PATH.read_text(encoding="utf-8"))


def load_rubric_assessments() -> dict[str, Any]:
    if not RUBRIC_ASSESSMENTS_PATH.exists():
        raise SystemExit(f"Missing editorial atlas rubric source: {RUBRIC_ASSESSMENTS_PATH}")
    loaded = yaml.safe_load(RUBRIC_ASSESSMENTS_PATH.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise SystemExit("Editorial atlas rubric source must be a mapping at the top level")
    return loaded


def load_atlas_data() -> dict[str, Any]:
    if not ATLAS_DATA_PATH.exists():
        raise SystemExit(f"Missing editorial atlas data: {ATLAS_DATA_PATH}")
    return json.loads(ATLAS_DATA_PATH.read_text(encoding="utf-8"))


def build_public_archive_index() -> dict[str, dict[str, Any]]:
    index: dict[str, dict[str, Any]] = {}
    for entry in load_metadata():
        if not entry.get("mirror_enabled") or entry.get("audience") != "everyone":
            continue
        title = entry.get("title")
        if not isinstance(title, str) or not title:
            raise SystemExit(f"Archive metadata entry is missing a usable title: {entry}")
        if title in index:
            raise SystemExit(f"Duplicate public archive title in metadata.json: {title}")
        index[title] = entry
    return index


def round_half_up(value: float) -> int:
    return int(math.floor(value + 0.5))


def validate_int_score(value: Any, context: str) -> int:
    if not isinstance(value, int):
        raise SystemExit(f"{context} must be an integer score: {value!r}")
    if value < 1 or value > 10:
        raise SystemExit(f"{context} must be between 1 and 10: {value}")
    return value


def validate_positive_int(value: Any, context: str) -> int:
    if not isinstance(value, int):
        raise SystemExit(f"{context} must be an integer: {value!r}")
    if value <= 0:
        raise SystemExit(f"{context} must be positive: {value}")
    return value


def validate_non_empty_string(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"{context} must be a non-empty string")
    return value.strip()


def validate_optional_reason(reason: Any, delta: int, context: str) -> str | None:
    if delta == 0:
        if reason in (None, ""):
            return None
        return validate_non_empty_string(reason, context)
    return validate_non_empty_string(reason, context)


def validate_override(mapping: Any, context: str) -> tuple[int, str | None]:
    if mapping is None:
        return 0, None
    if not isinstance(mapping, dict):
        raise SystemExit(f"{context} override must be a mapping")
    delta = mapping.get("delta", 0)
    if not isinstance(delta, int):
        raise SystemExit(f"{context} override delta must be an integer: {delta!r}")
    if delta < -1 or delta > 1:
        raise SystemExit(f"{context} override delta must be between -1 and 1: {delta}")
    reason = validate_optional_reason(mapping.get("reason"), delta, f"{context} override reason")
    return delta, reason


def validate_score_block(mapping: Any, required_keys: tuple[str, ...], context: str) -> dict[str, int]:
    if not isinstance(mapping, dict):
        raise SystemExit(f"{context} must be a mapping")
    missing = [key for key in required_keys if key not in mapping]
    if missing:
        raise SystemExit(f"{context} is missing keys {missing}")
    return {key: validate_int_score(mapping[key], f"{context}.{key}") for key in required_keys}


def derive_composite(
    score_block: dict[str, int],
    ordered_keys: tuple[str, ...],
    override_mapping: Any,
    context: str,
) -> int:
    base = round_half_up(sum(score_block[key] for key in ordered_keys) / len(ordered_keys))
    delta, _ = validate_override(override_mapping, context)
    final = base + delta
    if final < 1 or final > 10:
        raise SystemExit(f"{context} composite is out of range after override: {final}")
    return final


def validate_moves(moves: Any, title: str) -> list[str]:
    if not isinstance(moves, list) or not moves:
        raise SystemExit(f"Editorial atlas essay moves must be a non-empty list: {title}")
    validated: list[str] = []
    for move in moves:
        move_id = validate_non_empty_string(move, f"Move id for {title}")
        if move_id not in KNOWN_MOVE_IDS:
            raise SystemExit(f"Unknown editorial atlas move id '{move_id}' for {title}")
        validated.append(move_id)
    return validated


def validate_rationale_block(mapping: Any, title: str, rubric_status: str) -> dict[str, Any]:
    if mapping is None:
        if rubric_status == "audited":
            raise SystemExit(f"Audited essay is missing rationale block: {title}")
        return {}
    if not isinstance(mapping, dict):
        raise SystemExit(f"Rationale block must be a mapping: {title}")
    if rubric_status == "audited":
        required = ("whole_essay_note", "opening_anchor", "middle_anchor", "ending_anchor")
        missing = [key for key in required if not mapping.get(key)]
        if missing:
            raise SystemExit(f"Audited essay rationale is missing keys {missing}: {title}")
    return mapping


def count_words_from_markdown(markdown_path: Path) -> int:
    text = markdown_path.read_text(encoding="utf-8")
    return len(
        [
            token
            for token in text.replace("\u2019", "'").replace("\u2013", "-").replace("\u2014", "-").split()
            if any(char.isalnum() for char in token)
        ]
    )


def validate_corpus_coverage(source: dict[str, Any], essays: list[dict[str, Any]], archive_index: dict[str, dict[str, Any]]) -> None:
    corpus = source.get("corpus")
    if not isinstance(corpus, dict):
        raise SystemExit("Editorial atlas rubric source must contain a 'corpus' mapping")

    exclusions = corpus.get("exclusions", [])
    if not isinstance(exclusions, list):
        raise SystemExit("Editorial atlas corpus exclusions must be a list")

    excluded_titles: set[str] = set()
    for exclusion in exclusions:
        if not isinstance(exclusion, dict):
            raise SystemExit("Editorial atlas exclusions must be mappings")
        title = validate_non_empty_string(exclusion.get("title"), "Editorial atlas exclusion title")
        validate_non_empty_string(exclusion.get("reason"), f"Editorial atlas exclusion reason for {title}")
        if title not in archive_index:
            raise SystemExit(f"Editorial atlas exclusion does not match a public archive title: {title}")
        if title in excluded_titles:
            raise SystemExit(f"Duplicate editorial atlas exclusion title: {title}")
        excluded_titles.add(title)

    scored_titles = [validate_non_empty_string(essay.get("title"), "Editorial atlas essay title") for essay in essays]
    duplicates = {title for title in scored_titles if scored_titles.count(title) > 1}
    if duplicates:
        raise SystemExit(f"Duplicate editorial atlas essay titles: {sorted(duplicates)}")

    overlap = excluded_titles.intersection(scored_titles)
    if overlap:
        raise SystemExit(f"Editorial atlas titles cannot be both scored and excluded: {sorted(overlap)}")

    unknown_scored = sorted(set(scored_titles).difference(archive_index))
    if unknown_scored:
        raise SystemExit(f"Editorial atlas includes titles not found in the public archive: {unknown_scored}")

    uncovered = sorted(set(archive_index).difference(scored_titles).difference(excluded_titles))
    if uncovered:
        raise SystemExit(
            "Editorial atlas is missing public archive titles with no explicit exclusion: "
            f"{uncovered}"
        )


def derive_essay_record(entry: dict[str, Any], archive_entry: dict[str, Any]) -> dict[str, Any]:
    title = validate_non_empty_string(entry.get("title"), "Editorial atlas essay title")
    rubric_status = validate_non_empty_string(entry.get("rubric_status", "migrated"), f"Rubric status for {title}")
    if rubric_status not in ALLOWED_RUBRIC_STATUS:
        raise SystemExit(f"Unknown rubric status '{rubric_status}' for {title}")

    short_label = validate_non_empty_string(entry.get("short_label"), f"Short label for {title}")
    identity = validate_non_empty_string(entry.get("identity"), f"Identity for {title}")
    signature = validate_non_empty_string(entry.get("signature"), f"Signature for {title}")
    overpull_risk = validate_non_empty_string(entry.get("overpull_risk"), f"Overpull risk for {title}")
    confidence = validate_non_empty_string(entry.get("confidence"), f"Confidence for {title}").lower()
    if confidence not in ALLOWED_CONFIDENCE:
        raise SystemExit(f"Unknown confidence '{confidence}' for {title}")

    direct_scores = validate_score_block(entry.get("direct_scores"), DIRECT_KEYS, f"Direct scores for {title}")
    traction_scores = validate_score_block(entry.get("traction_subscores"), TRACTION_KEYS, f"Traction subscores for {title}")
    craft_scores = validate_score_block(entry.get("craft_subscores"), CRAFT_KEYS, f"Craft subscores for {title}")
    section_scores = validate_score_block(entry.get("section_scores"), SECTION_KEYS, f"Section scores for {title}")
    validate_rationale_block(entry.get("rationale"), title, rubric_status)

    traction = derive_composite(traction_scores, TRACTION_KEYS, entry.get("traction_override"), f"Traction for {title}")
    craft = derive_composite(craft_scores, CRAFT_KEYS, entry.get("craft_override"), f"Craft for {title}")

    publication_power_base = round_half_up((0.6 * traction) + (0.4 * craft))
    publication_delta, _ = validate_override(entry.get("publication_power_override"), f"Publication power for {title}")
    publication_power = publication_power_base + publication_delta
    if publication_power < 1 or publication_power > 10:
        raise SystemExit(f"Publication power is out of range for {title}: {publication_power}")

    markdown_path = REPO_ROOT / archive_entry["md_path"]
    words = entry.get("words")
    if words is None:
        words = count_words_from_markdown(markdown_path)
    words = validate_positive_int(words, f"Word count for {title}")

    return {
        "file": Path(archive_entry["md_path"]).name,
        "title": title,
        "date": validate_non_empty_string(archive_entry.get("post_date"), f"Archive post date for {title}")[:10],
        "words": words,
        "traction": traction,
        "craft": craft,
        "publication_power": publication_power,
        "opening": section_scores["opening"],
        "development": section_scores["development"],
        "ending": section_scores["ending"],
        "evidence": craft_scores["evidence_integration"],
        "identity": identity,
        "signature": signature,
        "overpull_risk": overpull_risk,
        "confidence": confidence,
        "debate": direct_scores["debate"],
        "precision": direct_scores["precision"],
        "synthesis": direct_scores["synthesis"],
        "utility": direct_scores["utility"],
        "moves": validate_moves(entry.get("moves"), title),
        "short_label": short_label,
        "thesis_lock": section_scores["thesis_lock"],
        "borders": section_scores["borders"],
        "reference_handling": section_scores["reference_handling"],
    }


def validate_draft_positions(position: Any, context: str) -> dict[str, int]:
    return validate_score_block(position, POSITION_KEYS, context)


def validate_drafts(drafts: Any, scored_titles: set[str]) -> list[dict[str, Any]]:
    if not isinstance(drafts, list) or not drafts:
        raise SystemExit("Editorial atlas rubric source must contain a non-empty 'drafts' list")

    validated: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for draft in drafts:
        if not isinstance(draft, dict):
            raise SystemExit("Editorial atlas draft entries must be mappings")
        draft_id = validate_non_empty_string(draft.get("id"), "Editorial atlas draft id")
        if draft_id in seen_ids:
            raise SystemExit(f"Duplicate editorial atlas draft id: {draft_id}")
        seen_ids.add(draft_id)

        title = validate_non_empty_string(draft.get("title"), f"Draft title for {draft_id}")
        one_line_identity = validate_non_empty_string(
            draft.get("one_line_identity"),
            f"Draft one_line_identity for {draft_id}",
        )
        problem = validate_non_empty_string(draft.get("problem"), f"Draft problem for {draft_id}")
        current_position = validate_draft_positions(draft.get("current_position"), f"Draft current_position for {draft_id}")
        target_position = validate_draft_positions(draft.get("target_position"), f"Draft target_position for {draft_id}")

        pulls = draft.get("pulls")
        if not isinstance(pulls, list) or not pulls:
            raise SystemExit(f"Editorial atlas draft pulls must be a non-empty list: {draft_id}")
        validated_pulls: list[dict[str, Any]] = []
        for pull in pulls:
            if not isinstance(pull, dict):
                raise SystemExit(f"Editorial atlas draft pull must be a mapping: {draft_id}")
            essay_title = validate_non_empty_string(pull.get("essay"), f"Draft pull essay for {draft_id}")
            if essay_title not in scored_titles:
                raise SystemExit(f"Draft pull essay is not present in atlas essays: {essay_title}")
            section = validate_non_empty_string(pull.get("section"), f"Draft pull section for {draft_id}")
            if section not in SECTION_LABELS:
                raise SystemExit(f"Draft pull section is not recognized for {draft_id}: {section}")
            desired_strength = validate_non_empty_string(
                pull.get("desired_strength"),
                f"Draft desired_strength for {draft_id}",
            )
            pull_record = {
                "essay": essay_title,
                "section": section,
                "desired_strength": desired_strength,
            }
            if pull.get("strength") is not None:
                pull_record["strength"] = validate_non_empty_string(
                    pull.get("strength"),
                    f"Draft pull strength for {draft_id}",
                )
            validated_pulls.append(pull_record)

        resists = draft.get("resists")
        if not isinstance(resists, list):
            raise SystemExit(f"Editorial atlas draft resists must be a list: {draft_id}")
        validated_resists: list[dict[str, Any]] = []
        for resist in resists:
            if not isinstance(resist, dict):
                raise SystemExit(f"Editorial atlas draft resist must be a mapping: {draft_id}")
            essay_title = validate_non_empty_string(resist.get("essay"), f"Draft resist essay for {draft_id}")
            if essay_title not in scored_titles:
                raise SystemExit(f"Draft resist essay is not present in atlas essays: {essay_title}")
            risk = validate_non_empty_string(resist.get("risk"), f"Draft resist risk for {draft_id}")
            validated_resists.append({"essay": essay_title, "risk": risk})

        validated.append(
            {
                "id": draft_id,
                "title": title,
                "one_line_identity": one_line_identity,
                "problem": problem,
                "current_position": current_position,
                "target_position": target_position,
                "pulls": validated_pulls,
                "resists": validated_resists,
            }
        )

    return validated


def build_editorial_atlas_data(source: dict[str, Any] | None = None) -> dict[str, Any]:
    source = source or load_rubric_assessments()
    archive_index = build_public_archive_index()

    essays = source.get("essays")
    if not isinstance(essays, list) or not essays:
        raise SystemExit("Editorial atlas rubric source must contain a non-empty 'essays' list")

    validate_corpus_coverage(source, essays, archive_index)
    derived_essays = [derive_essay_record(entry, archive_index[entry["title"]]) for entry in essays]
    scored_titles = {essay["title"] for essay in derived_essays}

    return {
        "version": source.get("version", 1),
        "corpus_source": source.get("corpus_source", "publication_strategy_and_archive/substack_archive"),
        "score_scale": source.get("score_scale", "1-10 qualitative manual scoring"),
        "dimensions": DIMENSIONS,
        "essays": derived_essays,
        "drafts": validate_drafts(source.get("drafts"), scored_titles),
    }


def render_json(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def diff_generated_vs_checked_in(expected: dict[str, Any], current: dict[str, Any]) -> str:
    expected_lines = render_json(expected).splitlines()
    current_lines = render_json(current).splitlines()
    diff = difflib.unified_diff(
        current_lines,
        expected_lines,
        fromfile=str(ATLAS_DATA_PATH),
        tofile="generated-from-rubric",
        lineterm="",
    )
    return "\n".join(diff)


def ensure_checked_in_atlas_matches_generated() -> dict[str, Any]:
    generated = build_editorial_atlas_data()
    current = load_atlas_data()
    if current != generated:
        diff = diff_generated_vs_checked_in(generated, current)
        raise SystemExit(
            "Editorial atlas data is out of date with rubric_assessments.yaml. "
            "Run `.venv/bin/python scripts/generate_editorial_atlas.py`.\n"
            f"{diff}"
        )
    return generated
