#!/usr/bin/env python3
"""
Shared helpers for essay-iteration packet discovery, scaffolding, and validation.
"""

from __future__ import annotations

from pathlib import Path
import re

from lifecycle import PUBLICATIONS_DIR, REPO_ROOT


PACKET_SCHEMA_VERSION = 4
NORTH_STAR_ESCALATION_SCHEMA_VERSION = 2

BLUEPRINT_PATTERNS = ("*blueprint*.md", "*plan*.md")
REVIEW_PATTERNS = ("*review*.md", "*scorecard*.md", "*claims*.md", "*rubric*.md")

BLUEPRINT_HEADINGS = [
    "## Promise",
    "## Spine",
    "## Paragraph burden",
    "## Evidence burden",
    "## Cut order",
    "## Failure triggers",
]

PREWRITE_FRONTMATTER_FIELDS = [
    "kind",
    "package",
    "revision",
    "judgment_policy",
    "live_draft_path",
    "candidate_path",
    "writability_verdict",
    "candidate_authorized",
    "dominant_blocker_slug",
    "supporting_artifact_paths",
]

PREWRITE_BODY_HEADINGS = [
    "## Promise",
    "## Spine",
    "## Paragraph burden",
    "## Evidence burden",
    "## Cut order",
    "## Failure triggers",
    "## Claim-State Gate",
    "## Writability Verdict",
    "## Required Follow-Through",
]

PREWRITE_WRITABILITY_VERDICTS = {
    "pending",
    "writable",
    "not_yet_writable",
}

CEILING_REPORT_FRONTMATTER_FIELDS = [
    "kind",
    "package",
    "revision",
    "live_draft_path",
    "terminal_candidate_path",
    "terminal_replacement_review_path",
    "terminal_decision_path",
    "dominant_blocker_slug",
    "ceiling_verdict",
    "effort_verdict",
    "next_route",
]

CEILING_REPORT_BODY_HEADINGS = [
    "## Verdict",
    "## Iteration Chronology",
    "## Blocker Timeline",
    "## Effort Audit",
    "## What Survived",
    "## What Did Not Survive",
    "## Lessons Learned",
    "## Next Route",
]

CEILING_REPORT_VERDICTS = {
    "pending",
    "object_ceiling",
    "not_ceiling",
}

CEILING_REPORT_EFFORT_VERDICTS = {
    "pending",
    "hard_enough",
    "not_hard_enough",
    "inconclusive",
}

CEILING_REPORT_NEXT_ROUTES = {
    "pending",
    "post_ceiling_pivot",
    "publish_non_flagship",
    "shelve",
}

ESCALATION_BLUEPRINT_HEADINGS = [
    "## Opening Lab",
    "## Object Decision",
    "## Body / Support / Footnote Ledger",
    "## Second-Pass Bet",
]

REVIEW_FRONTMATTER_FIELDS = [
    "kind",
    "package",
    "revision",
    "judgment_policy",
    "live_draft_path",
    "candidate_path",
    "replacement_verdict",
    "north_star_verdict",
]

ESCALATION_REVIEW_FRONTMATTER_FIELDS = [
    "dominant_blocker_slug",
    "continue_iteration",
]

REVIEW_BODY_HEADINGS = [
    "## Findings",
    "## Prioritized Issues",
    "## Scorecard",
    "## Replacement Verdict",
    "## North-Star Verdict",
    "## Main Blockers",
]

ESCALATION_REVIEW_BODY_HEADINGS = [
    "## Dominant Blocker",
    "## North-Star Delta",
    "## Continue Or Stop",
    "## If Continue, What Gets Cut",
]

SCORECARD_FRONTMATTER_FIELDS = [
    "kind",
    "package",
    "revision",
    "judgment_policy",
    "candidate_path",
    "opening_anchor",
    "middle_anchor",
    "ending_anchor",
    "nearby_archive_anchor",
    "stronger_archive_anchor",
    "weaker_archive_anchor",
    "traction",
    "craft",
    "publication_power",
    "next_score_blocker",
]

SCORECARD_BODY_HEADINGS = [
    "## Whole-Draft Rationale",
    "## Opening Anchor",
    "## Middle Anchor",
    "## Ending Anchor",
    "## Archive Anchors",
    "## Direct Dimensions",
    "## Traction",
    "## Craft",
    "## Publication Power",
    "## Next-score Blocker",
]

DECISION_FRONTMATTER_FIELDS = [
    "kind",
    "package",
    "revision",
    "judgment_policy",
    "live_draft_path",
    "candidate_path",
    "recommendation",
    "promotion_allowed",
    "requires_human_approval",
]

ESCALATION_DECISION_FRONTMATTER_FIELDS = [
    "rewrite_mode",
    "stop_gate_status",
]

DECISION_BODY_HEADINGS = [
    "## Recommendation",
    "## Promotion Gate",
    "## Required Follow-Through",
]

ESCALATION_DECISION_BODY_HEADINGS = [
    "## Escalation Decision",
    "## Rewrite Mode",
    "## Stop Gate For Next Pass",
]

ARCHIVE_ANCHOR_FIELDS = [
    "nearby_archive_anchor",
    "stronger_archive_anchor",
    "weaker_archive_anchor",
]

PASSAGE_ANCHOR_FIELDS = [
    "opening_anchor",
    "middle_anchor",
    "ending_anchor",
]

CANDIDATE_LIMITS_HEADINGS = [
    "## Limits",
    "## Borders",
    "## What This Will Not Fix",
    "## What This Essay Will Not Claim",
]

CANDIDATE_REFERENCES_HEADINGS = [
    "## References",
    "## Endmatter",
    "## Sources",
    "## Further Reading",
]

PACKET_TEMPLATE_TARGETS = {
    "hardened_blueprint_template.md": "blueprint",
    "prewrite_gate_template.md": "prewrite_gate",
    "candidate_template.md": "candidate",
    "cold_replacement_review_template.md": "replacement_review",
    "atlas_live_draft_scorecard_template.md": "atlas_scorecard",
    "promotion_decision_template.md": "decision",
    "ceiling_report_template.md": "ceiling_report",
}

ESCALATION_STOP_GATE_STATUSES = {
    "inactive",
    "armed",
    "fired",
}

DOMINANT_BLOCKER_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

CANDIDATE_SCAFFOLD_MARKERS = [
    "# Working Title",
    "Write the candidate here.",
    "## Limits",
    "State the boundaries, counterpressure, or what the essay will not claim.",
    "## References",
    "Include real endmatter or references, not just a companion pointer.",
]

DECISION_REQUIRED_FOLLOW_THROUGH_PLACEHOLDER = (
    "List the next concrete actions required before the stage can be marked done."
)


def repo_relpath(path: Path | None) -> str | None:
    if path is None:
        return None
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def resolve_config_path(status_data: dict, key: str) -> Path | None:
    value = status_data.get("config", {}).get(key)
    if not isinstance(value, str) or not value.strip():
        return None
    candidate = (REPO_ROOT / value).resolve()
    if candidate.exists():
        return candidate
    return None


def packet_schema_version(packet: dict) -> int:
    version = packet.get("packet_schema_version", 1)
    if not isinstance(version, int):
        raise ValueError("Packet manifest field 'packet_schema_version' must be an integer.")
    return version


def escalation_mode_active(
    packet: dict,
    review_frontmatter: dict,
    decision_frontmatter: dict,
) -> bool:
    return (
        packet_schema_version(packet) >= NORTH_STAR_ESCALATION_SCHEMA_VERSION
        and review_frontmatter.get("north_star_verdict") == "below_north_star"
        and decision_frontmatter.get("recommendation") == "revise_candidate"
    )


def valid_dominant_blocker_slug(value: object) -> bool:
    return isinstance(value, str) and bool(DOMINANT_BLOCKER_SLUG_RE.fullmatch(value))


def candidate_text_looks_scaffold(text: str) -> bool:
    return all(marker in text for marker in CANDIDATE_SCAFFOLD_MARKERS)


def resolve_live_draft(package_path: Path, status_data: dict) -> Path | None:
    markdown_path = resolve_config_path(status_data, "markdown_path")
    if markdown_path and markdown_path.exists():
        return markdown_path
    return None


def resolve_leaf_readme(package_path: Path) -> Path | None:
    candidate = package_path / "README.md"
    if candidate.exists():
        return candidate
    return None


def resolve_parent_package_path(package_path: Path, status_data: dict) -> Path | None:
    candidates: list[Path] = []
    parent_package = status_data.get("parent_package")
    if isinstance(parent_package, str) and parent_package.strip():
        candidates.append((PUBLICATIONS_DIR / parent_package.strip()).resolve())

    parent_dir = package_path.resolve().parent
    if parent_dir != PUBLICATIONS_DIR:
        candidates.append(parent_dir)

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if candidate.exists() and candidate != package_path.resolve():
            return candidate
    return None


def resolve_parent_package_readme(package_path: Path, status_data: dict) -> Path | None:
    parent_path = resolve_parent_package_path(package_path, status_data)
    if not parent_path:
        return None
    candidate = parent_path / "README.md"
    if candidate.exists():
        return candidate
    return None


def resolve_companion_path(package_path: Path) -> Path | None:
    candidate = package_path / "companion.md"
    if candidate.exists():
        return candidate
    return None


def resolve_evidence_surface(package_path: Path, status_data: dict) -> Path | None:
    configured = resolve_config_path(status_data, "evidence_path")
    if configured:
        return configured

    candidates = [
        package_path / "papers" / "index.md",
        package_path / "papers",
    ]

    parent_path = resolve_parent_package_path(package_path, status_data)
    if parent_path:
        candidates.extend(
            [
                parent_path / "papers" / "index.md",
                parent_path / "papers",
            ]
        )

    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _glob_direct_files(root: Path, patterns: tuple[str, ...]) -> list[Path]:
    if not root.exists():
        return []
    matches: list[Path] = []
    seen: set[Path] = set()
    for pattern in patterns:
        for candidate in sorted(root.glob(pattern)):
            if not candidate.is_file() or candidate in seen:
                continue
            seen.add(candidate)
            matches.append(candidate)
    return matches


def _revision_sort_key(path: Path) -> tuple[int, str]:
    match = re.search(r"-r(\d+)\.md$", path.name)
    if match:
        return (int(match.group(1)), path.name)
    return (0, path.name)


def resolve_nearest_blueprint_path(package_path: Path, status_data: dict) -> Path | None:
    for root in filter(None, [package_path, resolve_parent_package_path(package_path, status_data)]):
        matches = _glob_direct_files(root, BLUEPRINT_PATTERNS)
        if matches:
            return max(matches, key=_revision_sort_key)
    return None


def resolve_governing_brief_path(package_path: Path, status_data: dict) -> Path | None:
    config = status_data.get("config", {})
    configured = config.get("blueprint_path")
    if isinstance(configured, str) and configured.strip():
        candidate = (package_path / configured.strip()).resolve()
        try:
            candidate.relative_to(package_path.resolve())
        except ValueError:
            candidate = None
        if candidate is not None and candidate.exists():
            return candidate
    return resolve_nearest_blueprint_path(package_path, status_data)


def resolve_review_artifact_paths(package_path: Path, status_data: dict) -> list[Path]:
    matches: list[Path] = []
    seen: set[Path] = set()
    for root in filter(None, [package_path, resolve_parent_package_path(package_path, status_data)]):
        for candidate in _glob_direct_files(root, REVIEW_PATTERNS):
            if candidate in seen:
                continue
            seen.add(candidate)
            matches.append(candidate)
    return sorted(matches, key=_revision_sort_key, reverse=True)


def build_packet_paths(live_draft_path: Path, revision: int) -> dict[str, Path]:
    draft_stem = live_draft_path.stem
    root = live_draft_path.parent
    return {
        "manifest": root / f"{draft_stem}-essay-iteration-packet-r{revision}.json",
        "blueprint": root / f"{draft_stem}-blueprint-r{revision}.md",
        "prewrite_gate": root / f"{draft_stem}-prewrite-gate-r{revision}.md",
        "candidate": root / f"{draft_stem}-candidate-r{revision}.md",
        "replacement_review": root / f"{draft_stem}-replacement-review-r{revision}.md",
        "atlas_scorecard": root / f"{draft_stem}-atlas-scorecard-r{revision}.md",
        "decision": root / f"{draft_stem}-decision-r{revision}.md",
        "ceiling_report": root / f"{draft_stem}-ceiling-report-r{revision}.md",
    }


def describe_packet_paths(live_draft_path: Path | None, revision: int | None) -> dict[str, str]:
    if live_draft_path is None or revision is None:
        return {}
    return {
        name: repo_relpath(path)
        for name, path in build_packet_paths(live_draft_path, revision).items()
    }
