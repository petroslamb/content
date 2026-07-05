#!/usr/bin/env python3
"""Fail if public Git refs track private operational material."""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
ALLOWED_HIDDEN = {".github", ".gitignore", ".gitattributes", ".gitmodules"}

NOTEBOOK_URL_RE = re.compile(
    r"https://notebooklm\.google\.com/notebook/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    re.IGNORECASE,
)
NOTEBOOK_ID_FIELD_RE = re.compile(
    r"(?m)^\s*(?:notebooklm_notebook_id|id):\s+[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\s*$",
    re.IGNORECASE,
)
PRIVATE_YOUTUBE_STATE_RE = re.compile(
    r'(?:"privacy_status"|"privacyStatus")\s*:\s*"private"|(?:"publish_at"|"scheduled_at"|"scheduled_publish_at")\s*:\s*"20\d{2}-',
    re.IGNORECASE,
)

SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("private key block", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[psuor]_[A-Za-z0-9_]{36,}\b")),
    ("OpenAI API key", re.compile(r"\b(?:sk-(?:proj|svcacct|admin)-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9]{32,})\b")),
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_-]{32,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{20,}\b")),
    ("Stripe secret key", re.compile(r"\b(?:sk|rk)_(?:live|test)_[0-9A-Za-z]{24,}\b")),
)

SENSITIVE_EXACT_PATHS = {
    "publication_strategy_and_archive/future_publication_strategy.md",
    "publication_strategy_and_archive/publication_analysis_results.md",
}


@dataclass(frozen=True)
class Finding:
    path: str
    reason: str


def git_ls_files(repo: Path) -> list[str]:
    output = subprocess.check_output(["git", "-C", str(repo), "ls-files"], text=True)
    return [line for line in output.splitlines() if line]


def tracked_repositories() -> list[tuple[Path, str]]:
    repos = [(REPO_ROOT, "")]
    autonomy_tax = REPO_ROOT / "publications" / "autonomy-tax"
    if (autonomy_tax / ".git").exists():
        repos.append((autonomy_tax, "publications/autonomy-tax/"))
    return repos


def is_text(path: Path) -> bool:
    try:
        data = path.read_bytes()
    except FileNotFoundError:
        return False
    return b"\0" not in data[:4096]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def has_hidden_component(path: str) -> bool:
    parts = Path(path).parts
    return any(part.startswith(".") and part not in ALLOWED_HIDDEN for part in parts)


def path_reason(path: str) -> str | None:
    lower = path.lower()
    name = Path(path).name.lower()
    if path in SENSITIVE_EXACT_PATHS:
        return "private internal strategy document is tracked"
    if has_hidden_component(path):
        return "hidden local file or directory is tracked"
    if name == "notebooklm_metadata.json":
        return "NotebookLM metadata belongs in the private overlay"
    if "upload_report" in name or name == "upload_manifest.json":
        return "YouTube upload report/manifest belongs in the private overlay"
    if "shorts_manifest" in name:
        return "YouTube Shorts manifest belongs in the private overlay"
    if name == "candidate_report.json":
        return "generated YouTube candidate report belongs in the private overlay"
    if name in {"youtube_final_readback.json", "youtube_mutation_report.json", "caption_recovery_upload.json"}:
        return "YouTube channel readback/mutation state belongs in the private overlay"
    if "youtube_bundle_report" in name or "link_update_report" in name:
        return "YouTube channel bundle/readback state belongs in the private overlay"
    if "studio_verification" in name:
        return "Studio verification state belongs in the private overlay"
    if lower.startswith("experiments/youtube-cinematic-rollout/") and name in {"backlog_manifest.yaml", "release_ledger.md"}:
        return "YouTube rollout schedule state belongs in the private overlay"
    if lower.startswith("experiments/youtube-cinematic-rollout/") and name.endswith("_manifest.yaml"):
        return "YouTube rollout operational manifest belongs in the private overlay"
    if lower.startswith("experiments/youtube-cinematic-pilot/") and (
        "/metrics/" in lower or name.endswith("_manifest.yaml") or name in {"release_calendar.yaml", "notes.md"}
    ):
        return "YouTube pilot metrics/manifests/schedules belong in the private overlay"
    if lower.startswith("experiments/youtube-explainer-shorts/") and "/metrics/" in lower:
        return "YouTube explainer metrics belong in the private overlay"
    if lower.startswith("experiments/youtube-reference-comments/") and name.endswith("_manifest.yaml"):
        return "YouTube reference-comment mutation manifest belongs in the private overlay"
    if lower.startswith("experiments/youtube-insight-authority/") and name in {
        "cohort.yaml",
        "emit_plan.json",
        "insight_authority_plan.json",
        "manifest.yaml",
        "publish_plan.json",
        "release_ledger.md",
        "studio_verification.yaml",
    }:
        return "YouTube insight authority execution state belongs in the private overlay"
    if lower.startswith("experiments/youtube-insight-authority/") and name.startswith("draft_repair_packets_"):
        return "YouTube insight authority draft repair state belongs in the private overlay"
    if lower.startswith("publications/") and (
        name in {"linkedin-outreach-tracker.md", "expert-feedback-outreach.md", "outreach_candidates_top20.md", "cold_outreach_email.md"}
        or "/promoting_ideas/outreach" in lower
        or "/promoting_ideas/cold_outreach" in lower
    ):
        return "outreach targets/contact routes belong in the private overlay"
    if lower.startswith("reviewable-runs/") and "expert-feedback-outreach" in lower:
        return "outreach run records belong in the private overlay"
    if lower.startswith("reviewable-runs/logs/") and "media-distribution-retrospective" in name:
        return "YouTube media distribution retrospective belongs in the private overlay"
    if lower.startswith("experiments/youtube-analytics/") and name in {
        "experiment_registry.yaml",
        "reporting_jobs.json",
    }:
        return "YouTube analytics registry/job state belongs in the private overlay"
    if lower.startswith("experiments/youtube-analytics/channel_recovery_plan_"):
        return "YouTube channel recovery plan belongs in the private overlay"
    if lower.startswith("experiments/youtube-analytics/") and (
        "/reporting_downloads/" in lower
        or "/snapshots/" in lower
        or "/weekly_reports/" in lower
        or "/dashboard/" in lower
        or name in {"metrics_ledger.json", "content_rubric.json"}
    ):
        return "generated YouTube analytics state belongs in the private overlay"
    return None


def text_reasons(path: str, text: str) -> list[str]:
    reasons: list[str] = []
    lower = path.lower()
    if NOTEBOOK_URL_RE.search(text):
        reasons.append("restricted NotebookLM owner URL is tracked")
    if "notebooklm" in text.lower() and NOTEBOOK_ID_FIELD_RE.search(text):
        reasons.append("restricted NotebookLM UUID is tracked")
    if (lower.startswith("publications/") or lower.startswith("experiments/")) and PRIVATE_YOUTUBE_STATE_RE.search(text):
        if lower.endswith((".json", ".yaml", ".yml")) or "/artifacts/video/" in lower:
            reasons.append("private/scheduled YouTube state is tracked")
    if any(token in lower for token in ("outreach", "tracker", "promoting_ideas")) and "linkedin.com/in/" in text:
        reasons.append("LinkedIn profile/contact route is tracked in outreach material")
    for label, pattern in SECRET_PATTERNS:
        if pattern.search(text):
            reasons.append(f"{label} pattern is tracked")
    return reasons


def scan_repo(repo: Path, prefix: str) -> list[Finding]:
    findings: list[Finding] = []
    for relpath in git_ls_files(repo):
        public_path = f"{prefix}{relpath}"
        reason = path_reason(public_path)
        if reason:
            findings.append(Finding(public_path, reason))
        path = repo / relpath
        if not path.is_file() or not is_text(path):
            continue
        text = read_text(path)
        for text_reason in text_reasons(public_path, text):
            findings.append(Finding(public_path, text_reason))
    return findings


def main() -> int:
    findings: list[Finding] = []
    for repo, prefix in tracked_repositories():
        findings.extend(scan_repo(repo, prefix))

    if findings:
        print("Public hygiene check failed:", file=sys.stderr)
        for finding in findings:
            print(f"ERROR: {finding.path}: {finding.reason}", file=sys.stderr)
        return 1

    print("Public hygiene OK: tracked files contain no blocked private operational material.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
