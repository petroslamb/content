#!/usr/bin/env python3
"""Generate a bounded Phase 2.6 editorial automation report."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lifecycle import REPO_ROOT, load_status_ref


SCHEMA_VERSION = 1
VOICE_GUIDE_PATH = REPO_ROOT / "voice_consistency_guide.md"
DEFAULT_BANNED_PHRASES = [
    "Furthermore",
    "Moreover",
    "In conclusion",
    "To summarize",
    "It is important to note",
    "delve",
    "navigate",
    "unlock",
    "leverage",
    "testament",
    "crucial",
    "rich tapestry",
]
AUTHORITY_CLAIM_PATTERNS = [
    r"\bfirst\b",
    r"\balways\b",
    r"\bnever\b",
    r"\bproves?\b",
    r"\bguarantees?\b",
    r"\bundeniabl(?:e|y)\b",
    r"\bobviously\b",
]
MAX_PARAGRAPH_WORDS = 220
MAX_BULLET_LINES = 8


@dataclass(frozen=True)
class SourceLine:
    number: int
    text: str


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def repo_relpath(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def markdown_path_for_package(package_arg: str) -> tuple[str, Path, dict[str, Any], Any]:
    manifest_ref, status_data = load_status_ref(package_arg)
    config = status_data.get("config", {})
    if not isinstance(config, dict):
        raise ValueError(f"{repo_relpath(manifest_ref.status_path)} config must be a mapping.")
    markdown_path = config.get("markdown_path")
    if not isinstance(markdown_path, str) or not markdown_path.strip():
        raise ValueError(f"{repo_relpath(manifest_ref.status_path)} is missing config.markdown_path.")
    path = Path(markdown_path)
    if not path.is_absolute():
        path = REPO_ROOT / path
    path = path.resolve()
    try:
        path.relative_to(REPO_ROOT)
    except ValueError as exc:
        raise ValueError("config.markdown_path must stay inside the repository.") from exc
    if not path.exists():
        raise FileNotFoundError(f"Live draft does not exist: {repo_relpath(path)}")
    return manifest_ref.package_key, path, status_data, manifest_ref


def report_output_path(manifest_ref: Any, status_data: dict[str, Any], supplied_output: str | None) -> Path | None:
    if supplied_output == "-":
        return None
    if supplied_output:
        output = Path(supplied_output).expanduser()
        if not output.is_absolute():
            output = REPO_ROOT / output
        return output.resolve()
    revision = status_data.get("revision", 1)
    return manifest_ref.package_path / "artifacts" / f"editorial-report-r{revision}.json"


def source_lines(text: str) -> list[SourceLine]:
    return [SourceLine(index, line) for index, line in enumerate(text.splitlines(), start=1)]


def excerpt(text: str, limit: int = 180) -> str:
    cleaned = " ".join(text.strip().split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 3].rstrip() + "..."


def make_finding(
    *,
    check_id: str,
    severity: str,
    path: Path,
    message: str,
    line: int | None = None,
    snippet: str | None = None,
    suggestion: str | None = None,
) -> dict[str, Any]:
    finding: dict[str, Any] = {
        "check_id": check_id,
        "severity": severity,
        "path": repo_relpath(path),
        "message": message,
    }
    if line is not None:
        finding["line"] = line
    if snippet:
        finding["excerpt"] = excerpt(snippet)
    if suggestion:
        finding["suggestion"] = suggestion
    return finding


def banned_phrase_findings(path: Path, text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    lines = source_lines(text)
    for phrase in DEFAULT_BANNED_PHRASES:
        pattern = re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE)
        for line in lines:
            if pattern.search(line.text):
                findings.append(
                    make_finding(
                        check_id="voice_ban_list",
                        severity="warning",
                        path=path,
                        line=line.number,
                        message=f"Voice-guide banned phrase detected: {phrase}.",
                        snippet=line.text,
                        suggestion="Replace with direct, specific phrasing.",
                    )
                )
    for line in lines:
        if "\u2014" in line.text:
            findings.append(
                make_finding(
                    check_id="voice_ban_list",
                    severity="warning",
                    path=path,
                    line=line.number,
                    message="Voice guide bans em dashes.",
                    snippet=line.text,
                    suggestion="Rewrite with a period, comma, colon, or parenthetical structure.",
                )
            )
    return findings


def paragraph_rhythm_findings(path: Path, text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    paragraph_start = 1
    buffer: list[str] = []
    bullet_count = 0
    for index, line in enumerate(text.splitlines(), start=1):
        if re.match(r"\s*[-*]\s+", line):
            bullet_count += 1
        if line.strip():
            if not buffer:
                paragraph_start = index
            buffer.append(line)
            continue
        findings.extend(paragraph_findings_for_buffer(path, paragraph_start, buffer))
        buffer = []
    findings.extend(paragraph_findings_for_buffer(path, paragraph_start, buffer))
    if bullet_count > MAX_BULLET_LINES:
        findings.append(
            make_finding(
                check_id="paragraph_rhythm",
                severity="advisory",
                path=path,
                message=f"Draft contains {bullet_count} bullet lines; voice guide prefers prose unless linear contrast is essential.",
                suggestion="Collapse non-essential lists into narrative paragraphs.",
            )
        )
    return findings


def paragraph_findings_for_buffer(path: Path, start_line: int, lines: list[str]) -> list[dict[str, Any]]:
    if not lines:
        return []
    paragraph = " ".join(line.strip() for line in lines)
    if paragraph.startswith("#"):
        return []
    words = re.findall(r"\b[\w'-]+\b", paragraph)
    if len(words) <= MAX_PARAGRAPH_WORDS:
        return []
    return [
        make_finding(
            check_id="paragraph_rhythm",
            severity="advisory",
            path=path,
            line=start_line,
            message=f"Paragraph is {len(words)} words; voice guide prefers dense but controlled medium-length paragraphs.",
            snippet=paragraph,
            suggestion="Split only if the paragraph contains more than one conceptual turn.",
        )
    ]


def contrast_rhythm_findings(path: Path, text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    pattern = re.compile(r"\b(?:it|this|the problem|the point)\s+is\s+not\b", re.IGNORECASE)
    for line in source_lines(text):
        if pattern.search(line.text):
            findings.append(
                make_finding(
                    check_id="contrast_rhythm",
                    severity="advisory",
                    path=path,
                    line=line.number,
                    message="Potential repetitive contrast construction.",
                    snippet=line.text,
                    suggestion="Keep this only if the contrast is doing rare, high-value conceptual work.",
                )
            )
    return findings


def authority_claim_findings(path: Path, text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    combined = re.compile("|".join(AUTHORITY_CLAIM_PATTERNS), re.IGNORECASE)
    for line in source_lines(text):
        if combined.search(line.text) and not has_nearby_evidence_marker(line.text):
            findings.append(
                make_finding(
                    check_id="claim_evidence_trace",
                    severity="advisory",
                    path=path,
                    line=line.number,
                    message="Authority or superlative claim may need visible evidence support.",
                    snippet=line.text,
                    suggestion="Add a source, narrow the claim, or make the evidentiary basis explicit.",
                )
            )
    return findings


def has_nearby_evidence_marker(line: str) -> bool:
    return bool(re.search(r"\[[^\]]+\]\([^)]+\)|arxiv|paper|study|report|evidence", line, re.IGNORECASE))


def local_link_findings(path: Path, text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for line in source_lines(text):
        for match in link_pattern.finditer(line.text):
            target = match.group(1).strip()
            if not target or re.match(r"^[a-z]+://", target) or target.startswith("#"):
                continue
            target_path = target.split("#", 1)[0]
            if not target_path:
                continue
            candidate = (path.parent / target_path).resolve()
            try:
                candidate.relative_to(REPO_ROOT)
            except ValueError:
                findings.append(
                    make_finding(
                        check_id="local_link_integrity",
                        severity="warning",
                        path=path,
                        line=line.number,
                        message=f"Local link points outside the repository: {target}.",
                        snippet=line.text,
                    )
                )
                continue
            if not candidate.exists():
                findings.append(
                    make_finding(
                        check_id="local_link_integrity",
                        severity="warning",
                        path=path,
                        line=line.number,
                        message=f"Local link target is missing: {target}.",
                        snippet=line.text,
                    )
                )
    return findings


def check_summary(check_id: str, findings: list[dict[str, Any]], input_paths: list[str]) -> dict[str, Any]:
    scoped = [finding for finding in findings if finding.get("check_id") == check_id]
    counts = Counter(str(finding.get("severity", "advisory")) for finding in scoped)
    return {
        "id": check_id,
        "status": "passed" if not scoped else "findings",
        "input_paths": input_paths,
        "severity_counts": {
            "error": counts.get("error", 0),
            "warning": counts.get("warning", 0),
            "advisory": counts.get("advisory", 0),
        },
        "blocking_policy": "advisory_until_workflow_contract_marks_blocking",
    }


def source_improvement_suggestions(findings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts = Counter(str(finding.get("check_id")) for finding in findings)
    suggestions = []
    if counts["voice_ban_list"] >= 3:
        suggestions.append({
            "id": "tighten_voice_preflight",
            "source": "voice_ban_list",
            "suggestion": "Run the voice-guide banned-phrase scan before final article-polish handoff.",
        })
    if counts["claim_evidence_trace"] >= 5:
        suggestions.append({
            "id": "add_claim_support_pass",
            "source": "claim_evidence_trace",
            "suggestion": "Add a claim-support pass before release readiness for authority-heavy drafts.",
        })
    if counts["local_link_integrity"]:
        suggestions.append({
            "id": "repair_local_links",
            "source": "local_link_integrity",
            "suggestion": "Repair local markdown links before release-readiness review.",
        })
    return suggestions


def build_report(package_arg: str) -> dict[str, Any]:
    package_key, markdown_path, status_data, manifest_ref = markdown_path_for_package(package_arg)
    draft_text = markdown_path.read_text()
    voice_guide_text = VOICE_GUIDE_PATH.read_text()
    findings = [
        *banned_phrase_findings(markdown_path, draft_text),
        *paragraph_rhythm_findings(markdown_path, draft_text),
        *contrast_rhythm_findings(markdown_path, draft_text),
        *authority_claim_findings(markdown_path, draft_text),
        *local_link_findings(markdown_path, draft_text),
    ]
    for index, finding in enumerate(findings, start=1):
        finding["id"] = f"editorial-finding-{index:03d}"

    input_paths = [repo_relpath(markdown_path), repo_relpath(VOICE_GUIDE_PATH)]
    severity_counts = Counter(str(finding.get("severity", "advisory")) for finding in findings)
    return {
        "kind": "editorial_automation_report",
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "package": {
            "key": package_key,
            "path": repo_relpath(manifest_ref.package_path),
            "status_path": repo_relpath(manifest_ref.status_path),
            "revision": status_data.get("revision", 1),
            "live_draft_path": repo_relpath(markdown_path),
        },
        "authority": {
            "voice_guide_path": repo_relpath(VOICE_GUIDE_PATH),
            "voice_guide_loaded": bool(voice_guide_text.strip()),
        },
        "checks": [
            check_summary("voice_ban_list", findings, input_paths),
            check_summary("paragraph_rhythm", findings, input_paths),
            check_summary("contrast_rhythm", findings, input_paths),
            check_summary("claim_evidence_trace", findings, input_paths),
            check_summary("local_link_integrity", findings, input_paths),
        ],
        "severity_counts": {
            "error": severity_counts.get("error", 0),
            "warning": severity_counts.get("warning", 0),
            "advisory": severity_counts.get("advisory", 0),
        },
        "findings": findings,
        "source_improvement_suggestions": source_improvement_suggestions(findings),
        "state_effects": {
            "draft_rewritten": False,
            "package_status_changed": False,
            "lifecycle_moved": False,
            "published": False,
            "promoted": False,
        },
    }


def write_report(report: dict[str, Any], output_path: Path | None) -> None:
    rendered = json.dumps(report, indent=2, ensure_ascii=True) + "\n"
    if output_path is None:
        print(rendered, end="")
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered)
    print(repo_relpath(output_path))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a structured editorial automation report.")
    parser.add_argument("--package", required=True, help="Package key or path under publications/.")
    parser.add_argument("--output", help="Report output path. Use '-' for stdout.")
    parser.add_argument("--stdout", action="store_true", help="Write report JSON to stdout.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    report = build_report(args.package)
    output = "-" if args.stdout else args.output
    _, _, status_data, manifest_ref = markdown_path_for_package(args.package)
    write_report(report, report_output_path(manifest_ref, status_data, output))


if __name__ == "__main__":
    main()
