#!/usr/bin/env python3
"""
Shared helpers for essay-iteration packet discovery, scaffolding, and validation.
"""

from __future__ import annotations

from pathlib import Path
import re

from lifecycle import PUBLICATIONS_DIR, REPO_ROOT


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

REVIEW_BODY_HEADINGS = [
    "## Findings",
    "## Prioritized Issues",
    "## Scorecard",
    "## Replacement Verdict",
    "## North-Star Verdict",
    "## Main Blockers",
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

DECISION_BODY_HEADINGS = [
    "## Recommendation",
    "## Promotion Gate",
    "## Required Follow-Through",
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
    "candidate_template.md": "candidate",
    "cold_replacement_review_template.md": "replacement_review",
    "atlas_live_draft_scorecard_template.md": "atlas_scorecard",
    "promotion_decision_template.md": "decision",
}


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
        "candidate": root / f"{draft_stem}-candidate-r{revision}.md",
        "replacement_review": root / f"{draft_stem}-replacement-review-r{revision}.md",
        "atlas_scorecard": root / f"{draft_stem}-atlas-scorecard-r{revision}.md",
        "decision": root / f"{draft_stem}-decision-r{revision}.md",
    }


def describe_packet_paths(live_draft_path: Path | None, revision: int | None) -> dict[str, str]:
    if live_draft_path is None or revision is None:
        return {}
    return {
        name: repo_relpath(path)
        for name, path in build_packet_paths(live_draft_path, revision).items()
    }
