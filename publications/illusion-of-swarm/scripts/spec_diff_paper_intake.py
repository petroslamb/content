#!/usr/bin/env python3
"""Package-local spec-diff checker for illusion-of-swarm evidence orientation."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


SCRIPT_PATH = Path(__file__).resolve()
PACKAGE_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = SCRIPT_PATH.parents[3]
PACKAGE_KEY = "illusion-of-swarm"
STAGE = "paper_intake"

PAPERS_DIR = PACKAGE_ROOT / "papers"
INDEX_PATH = PAPERS_DIR / "index.md"
STATUS_PATH = PACKAGE_ROOT / "status.yaml"
ARTIFACTS_DIR = PACKAGE_ROOT / "artifacts"

ARXIV_LINK_RE = re.compile(r"arxiv\.org/abs/(?P<id>[0-9]{4}\.[0-9]{5})(?:v[0-9]+)?")
ARXIV_ID_RE = re.compile(r"(?P<id>[0-9]{4}\.[0-9]{5})(?:v[0-9]+)?")


@dataclass(frozen=True)
class EvidenceFile:
    path: Path
    rel_to_papers: str
    kind: str
    arxiv_ids: tuple[str, ...]


def repo_rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def package_rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(PACKAGE_ROOT).as_posix()
    except ValueError:
        return str(path)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def read_status() -> dict[str, Any]:
    if not STATUS_PATH.exists():
        return {}
    return yaml.safe_load(STATUS_PATH.read_text(encoding="utf-8")) or {}


def draft_path(status: dict[str, Any]) -> Path:
    configured = status.get("config", {}).get("markdown_path")
    if configured:
        path = Path(configured)
        if not path.is_absolute():
            path = REPO_ROOT / path
        return path
    return PACKAGE_ROOT / "the-illusion-of-the-swarm.md"


def text_sample(path: Path, limit: int = 4_000) -> str:
    try:
        return path.read_bytes()[:limit].decode("utf-8", errors="ignore")
    except OSError:
        return ""


def arxiv_ids_in_text(text: str) -> set[str]:
    return {match.group("id") for match in ARXIV_ID_RE.finditer(text)}


def classify_evidence_file(path: Path) -> str:
    if path.suffix == ".pdf":
        return "source_pdf"
    if path.parent.name == "markdown" and path.suffix == ".md":
        return "converted_markdown"
    if path.suffix == ".md":
        return "root_markdown"
    if path.suffix == ".txt":
        return "captured_text"
    return "other"


def discover_evidence_files() -> list[EvidenceFile]:
    files: list[EvidenceFile] = []
    for path in sorted(PAPERS_DIR.rglob("*")):
        if not path.is_file():
            continue
        if path == INDEX_PATH:
            continue
        if path.relative_to(PAPERS_DIR).as_posix() == "markdown/README.md":
            continue
        rel = path.relative_to(PAPERS_DIR).as_posix()
        ids = arxiv_ids_in_text(path.name) | arxiv_ids_in_text(text_sample(path))
        files.append(
            EvidenceFile(
                path=path,
                rel_to_papers=rel,
                kind=classify_evidence_file(path),
                arxiv_ids=tuple(sorted(ids)),
            )
        )
    return files


def cited_arxiv_ids(draft_text: str) -> set[str]:
    return {match.group("id") for match in ARXIV_LINK_RE.finditer(draft_text)}


def artifact_supported_ids() -> set[str]:
    ids: set[str] = set()
    if not ARTIFACTS_DIR.exists():
        return ids
    for path in ARTIFACTS_DIR.rglob("*"):
        if not path.is_file():
            continue
        ids.update(arxiv_ids_in_text(path.name))
    return ids


def section_after_heading(text: str, heading: str) -> str:
    start = text.find(heading)
    if start == -1:
        return ""
    tail = text[start + len(heading) :]
    match = re.search(r"\n## ", tail)
    return tail[: match.start()] if match else tail


def classified_gap_ids(index_text: str) -> set[str]:
    gap_section = section_after_heading(index_text, "## Cited In Draft But Not Yet Local Evidence")
    return arxiv_ids_in_text(gap_section)


def index_has_path(index_text: str, evidence: EvidenceFile) -> bool:
    return evidence.rel_to_papers in index_text or evidence.path.name in index_text


def finding(
    findings: list[dict[str, Any]],
    kind: str,
    severity: str,
    source_clause: str,
    expected: str,
    observed: str,
    notes: str | None = None,
) -> None:
    item: dict[str, Any] = {
        "finding": kind,
        "severity": severity,
        "source_clause": source_clause,
        "expected": expected,
        "observed": observed,
    }
    if notes:
        item["notes"] = notes
    findings.append(item)


def check_status(status: dict[str, Any], findings: list[dict[str, Any]]) -> None:
    paper_state = status.get("stages", {}).get(STAGE, {})
    if not paper_state.get("done"):
        finding(
            findings,
            "paper_intake_not_done",
            "blocking",
            f"{repo_rel(STATUS_PATH)}:stages.{STAGE}.done",
            "true",
            repr(paper_state.get("done")),
        )


def check_index_orientation(index_text: str, evidence_files: list[EvidenceFile], findings: list[dict[str, Any]]) -> None:
    nonempty_lines = [line for line in index_text.splitlines() if line.strip()]
    if len(nonempty_lines) < 20 or "## Locally Represented Papers" not in index_text:
        finding(
            findings,
            "paper_index_orientation_thin",
            "warning",
            repo_rel(INDEX_PATH),
            "substantive paper index with local evidence and gap sections",
            f"{len(nonempty_lines)} nonempty lines",
            "The package is marked paper_intake.done, so the index should orient reviewers to the evidence surface.",
        )

    kinds = {item.kind for item in evidence_files}
    mixed_storage = len(kinds & {"source_pdf", "root_markdown", "captured_text", "converted_markdown"}) > 1
    lowered = index_text.lower()
    calls_out_mixed_storage = (
        "mixed local evidence" in lowered
        or "root-level" in lowered
        or "source captures" in lowered
        or "older package" in lowered
    )
    if mixed_storage and not calls_out_mixed_storage:
        finding(
            findings,
            "mixed_storage_convention_not_called_out",
            "warning",
            repo_rel(INDEX_PATH),
            "index explicitly classifies mixed PDFs, root markdown, root text captures, and artifacts",
            "mixed files exist without an orientation note",
        )


def check_local_evidence_representation(
    index_text: str,
    evidence_files: list[EvidenceFile],
    findings: list[dict[str, Any]],
) -> None:
    for evidence in evidence_files:
        if index_has_path(index_text, evidence):
            continue
        finding(
            findings,
            "local_evidence_not_indexed",
            "warning",
            repo_rel(evidence.path),
            f"{evidence.rel_to_papers} represented or explicitly classified in papers/index.md",
            "not found in index",
        )


def check_draft_citations(
    draft: Path,
    draft_text: str,
    index_text: str,
    evidence_files: list[EvidenceFile],
    findings: list[dict[str, Any]],
) -> None:
    cited_ids = cited_arxiv_ids(draft_text)
    supported_by_artifact = artifact_supported_ids()
    supported_by_local = {arxiv_id for evidence in evidence_files for arxiv_id in evidence.arxiv_ids}
    classified_gaps = classified_gap_ids(index_text)
    supported = supported_by_artifact | supported_by_local

    for arxiv_id in sorted(cited_ids):
        if arxiv_id in supported or arxiv_id in classified_gaps:
            continue
        match = re.search(rf"arxiv\.org/abs/{re.escape(arxiv_id)}(?:v[0-9]+)?", draft_text)
        source = repo_rel(draft)
        if match:
            source = f"{source}:{line_number(draft_text, match.start())}"
        finding(
            findings,
            "cited_arxiv_without_local_evidence",
            "warning",
            source,
            f"{arxiv_id} has local paper evidence, alphaXiv artifact records, or an explicit gap classification",
            "citation exists only in the canonical draft",
            "This pass validates the evidence surface and index; it does not alter the published essay or download missing papers.",
        )


def build_report() -> dict[str, Any]:
    status = read_status()
    draft = draft_path(status)
    index_text = INDEX_PATH.read_text(encoding="utf-8") if INDEX_PATH.exists() else ""
    draft_text = draft.read_text(encoding="utf-8") if draft.exists() else ""
    evidence_files = discover_evidence_files() if PAPERS_DIR.exists() else []

    findings: list[dict[str, Any]] = []
    check_status(status, findings)

    if not INDEX_PATH.exists():
        finding(findings, "paper_index_missing", "blocking", repo_rel(INDEX_PATH), "papers/index.md", "missing")
    else:
        check_index_orientation(index_text, evidence_files, findings)
        check_local_evidence_representation(index_text, evidence_files, findings)

    if not draft.exists():
        finding(
            findings,
            "canonical_draft_missing",
            "blocking",
            f"{repo_rel(STATUS_PATH)}:config.markdown_path",
            repo_rel(draft),
            "missing",
        )
    elif INDEX_PATH.exists():
        check_draft_citations(draft, draft_text, index_text, evidence_files, findings)

    blocking_count = sum(1 for item in findings if item["severity"] == "blocking")
    warning_count = sum(1 for item in findings if item["severity"] == "warning")
    local_supported_ids = sorted({arxiv_id for evidence in evidence_files for arxiv_id in evidence.arxiv_ids})
    artifact_ids = sorted(artifact_supported_ids())
    cited_ids = sorted(cited_arxiv_ids(draft_text))
    gap_ids = sorted(classified_gap_ids(index_text))

    return {
        "kind": "spec_diff_report",
        "version": 1,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "package": PACKAGE_KEY,
        "stage": STAGE,
        "source": {
            "package_status": repo_rel(STATUS_PATH),
            "paper_index": repo_rel(INDEX_PATH),
            "canonical_draft": repo_rel(draft),
            "evidence_surface": repo_rel(PAPERS_DIR),
            "artifact_surface": repo_rel(ARTIFACTS_DIR),
        },
        "expected_state": {
            "paper_intake_done": bool(status.get("stages", {}).get(STAGE, {}).get("done")),
            "local_evidence_file_count": len(evidence_files),
            "local_evidence_kinds": sorted({evidence.kind for evidence in evidence_files}),
            "cited_arxiv_count": len(cited_ids),
            "local_supported_arxiv_ids": local_supported_ids,
            "artifact_supported_arxiv_ids": artifact_ids,
            "classified_gap_arxiv_ids": gap_ids,
            "evidence_files": [
                {
                    "path": evidence.rel_to_papers,
                    "kind": evidence.kind,
                    "arxiv_ids": list(evidence.arxiv_ids),
                }
                for evidence in evidence_files
            ],
        },
        "findings": findings,
        "summary": {
            "blocking": blocking_count,
            "warnings": warning_count,
            "status": "fail" if blocking_count else "pass_with_warnings" if warning_count else "pass",
        },
    }


def print_text(report: dict[str, Any]) -> None:
    summary = report["summary"]
    expected = report["expected_state"]
    print(f"Spec-diff: {report['package']} / {report['stage']}")
    print(f"Status: {summary['status']} ({summary['blocking']} blocking, {summary['warnings']} warning)")
    print(
        "Evidence/citation counts: "
        f"{expected['local_evidence_file_count']} local evidence files, "
        f"{expected['cited_arxiv_count']} cited arXiv IDs, "
        f"{len(expected['artifact_supported_arxiv_ids'])} artifact-supported IDs, "
        f"{len(expected['classified_gap_arxiv_ids'])} classified gaps"
    )
    if not report["findings"]:
        print("No drift findings.")
        return
    print()
    for item in report["findings"]:
        print(f"[{item['severity']}] {item['finding']}")
        print(f"  source:   {item['source_clause']}")
        print(f"  expected: {item['expected']}")
        print(f"  observed: {item['observed']}")
        if item.get("notes"):
            print(f"  notes:    {item['notes']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--write-report", help="Write the full JSON report to this path.")
    parser.add_argument("--fail-on-warning", action="store_true", help="Exit non-zero when warning findings exist.")
    args = parser.parse_args()

    report = build_report()

    if args.write_report:
        report_path = Path(args.write_report)
        if not report_path.is_absolute():
            report_path = REPO_ROOT / report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    if args.format == "json":
        print(json.dumps(report, indent=2))
    else:
        print_text(report)

    has_blocking = report["summary"]["blocking"] > 0
    has_warning = report["summary"]["warnings"] > 0
    return 1 if has_blocking or (args.fail_on_warning and has_warning) else 0


if __name__ == "__main__":
    raise SystemExit(main())
