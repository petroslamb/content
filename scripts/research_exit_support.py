#!/usr/bin/env python3
"""Shared helpers for the canonical research-exit gate artifact."""

from __future__ import annotations

from pathlib import Path
import re


RESEARCH_EXIT_FRONTMATTER_FIELDS = [
    "kind",
    "package",
    "revision",
    "governing_brief_path",
    "evidence_surface_path",
    "claim_boundary_status",
    "claim_boundary_paths",
    "research_exit_verdict",
    "dominant_blocker_slug",
    "follow_on_research_triggers",
]

RESEARCH_EXIT_BODY_HEADINGS = [
    "## Governing Blueprint",
    "## Evidence Surface",
    "## Claim Boundaries",
    "## Drafting Boundary",
    "## Verdict",
    "## Required Follow-Through",
]

RESEARCH_EXIT_VERDICTS = {
    "pending",
    "ready_for_essay_iteration",
    "not_ready",
}

CLAIM_BOUNDARY_STATUSES = {
    "not_required",
    "required_but_missing",
    "satisfied",
}

DOMINANT_BLOCKER_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def build_research_exit_gate_path(package_path: Path, revision: int) -> Path:
    return package_path / f"{package_path.name}-research-exit-gate-r{revision}.md"


def valid_blocker_slug(value: object) -> bool:
    return isinstance(value, str) and bool(DOMINANT_BLOCKER_SLUG_RE.fullmatch(value))
