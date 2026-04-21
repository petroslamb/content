#!/usr/bin/env python3
"""Prototype spec-diff checker for this package's paper_intake stage."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


SCRIPT_PATH = Path(__file__).resolve()
PACKAGE_ROOT = SCRIPT_PATH.parents[1]
REPO_ROOT = SCRIPT_PATH.parents[3]
PACKAGE_KEY = "literate-workflow-programming"
STAGE = "paper_intake"

PAPERS_DIR = PACKAGE_ROOT / "papers"
INDEX_PATH = PAPERS_DIR / "index.md"
MARKDOWN_DIR = PAPERS_DIR / "markdown"
METADATA_DIR = PAPERS_DIR / "metadata"
STATUS_PATH = PACKAGE_ROOT / "status.yaml"
WORKFLOW_DOC = REPO_ROOT / "workflows" / "paper-intake" / "README.md"
LOGS_DIR = REPO_ROOT / "reviewable-runs" / "logs"

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\n]+)\)")
LOCAL_FIELD_RE = re.compile(r"^- (?P<label>Local PDF|Local markdown|Metadata): .*\]\((?P<target>[^)\n]+)\)", re.MULTILINE)
HEADING_RE = re.compile(r"^### (?P<title>.+)$", re.MULTILINE)
ARXIV_RE = re.compile(r"\[`(?P<id>[0-9]{4}\.[0-9]{5}(?:v[0-9]+)?)`\]")
VERSION_SUFFIX_RE = re.compile(r"v[0-9]+$")


@dataclass(frozen=True)
class IndexedPaper:
    title: str
    heading_line: int
    block: str
    local_pdf: str | None
    local_markdown: str | None
    metadata: str | None
    arxiv_id: str | None


def repo_rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def section(text: str, start_heading: str, end_headings: tuple[str, ...]) -> str:
    start = text.find(start_heading)
    if start == -1:
        return ""
    end_candidates = [text.find(heading, start + len(start_heading)) for heading in end_headings]
    end_candidates = [pos for pos in end_candidates if pos != -1]
    end = min(end_candidates) if end_candidates else len(text)
    return text[start:end]


def target_path(raw_target: str) -> Path:
    return (PAPERS_DIR / raw_target).resolve()


def normalize_arxiv_id(arxiv_id: str) -> str:
    return VERSION_SUFFIX_RE.sub("", arxiv_id)


def parse_indexed_papers(index_text: str) -> list[IndexedPaper]:
    local_section = section(index_text, "## Locally Intaken", ("## Conversion Notes", "## Intake Queue"))
    matches = list(HEADING_RE.finditer(local_section))
    papers: list[IndexedPaper] = []
    for idx, match in enumerate(matches):
        block_start = match.end()
        block_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(local_section)
        block = local_section[block_start:block_end]
        fields = {field.group("label"): field.group("target") for field in LOCAL_FIELD_RE.finditer(block)}
        arxiv_match = ARXIV_RE.search(block)
        heading_offset = index_text.find(match.group(0))
        papers.append(
            IndexedPaper(
                title=match.group("title").strip(),
                heading_line=line_number(index_text, heading_offset),
                block=block,
                local_pdf=fields.get("Local PDF"),
                local_markdown=fields.get("Local markdown"),
                metadata=fields.get("Metadata"),
                arxiv_id=arxiv_match.group("id") if arxiv_match else None,
            )
        )
    return papers


def queued_ids(index_text: str) -> set[str]:
    queue = section(index_text, "## Intake Queue", ("## Current Reading Order",))
    return {normalize_arxiv_id(match.group("id")) for match in ARXIV_RE.finditer(queue)}


def is_ignored(path: Path) -> bool:
    proc = subprocess.run(
        ["git", "check-ignore", "-q", repo_rel(path)],
        cwd=REPO_ROOT,
        check=False,
    )
    return proc.returncode == 0


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


def check_index_links(index_text: str, findings: list[dict[str, Any]]) -> None:
    for match in LINK_RE.finditer(index_text):
        target = match.group(1)
        if target.startswith(("http://", "https://", "#")):
            continue
        path = target_path(target)
        if not path.exists():
            finding(
                findings,
                "paper_index_link_missing",
                "blocking",
                f"{repo_rel(INDEX_PATH)}:{line_number(index_text, match.start())}",
                repo_rel(path),
                "missing",
                "A local paper-index link should resolve inside the package evidence surface.",
            )


def check_indexed_papers(index_text: str, papers: list[IndexedPaper], findings: list[dict[str, Any]]) -> None:
    for paper in papers:
        source = f"{repo_rel(INDEX_PATH)}:{paper.heading_line} ({paper.title})"
        if not paper.local_pdf:
            finding(findings, "indexed_paper_missing_pdf_field", "blocking", source, "Local PDF field", "missing")
        if not paper.local_markdown:
            finding(findings, "indexed_paper_missing_markdown_field", "blocking", source, "Local markdown field", "missing")
        for field_name, rel_target in [
            ("local_pdf", paper.local_pdf),
            ("local_markdown", paper.local_markdown),
            ("metadata", paper.metadata),
        ]:
            if rel_target is None:
                continue
            path = target_path(rel_target)
            if not path.exists():
                finding(
                    findings,
                    f"indexed_{field_name}_missing",
                    "blocking",
                    source,
                    repo_rel(path),
                    "missing",
                )


def check_directory_consistency(
    papers: list[IndexedPaper],
    queued: set[str],
    findings: list[dict[str, Any]],
) -> None:
    indexed_pdf_targets = {paper.local_pdf for paper in papers if paper.local_pdf}
    indexed_markdown_targets = {paper.local_markdown for paper in papers if paper.local_markdown}
    indexed_metadata_targets = {paper.metadata for paper in papers if paper.metadata}

    for pdf_path in sorted(PAPERS_DIR.glob("*.pdf")):
        rel_target = pdf_path.relative_to(PAPERS_DIR).as_posix()
        if rel_target not in indexed_pdf_targets:
            finding(
                findings,
                "local_pdf_not_indexed",
                "warning",
                f"{repo_rel(PAPERS_DIR)}/*.pdf",
                f"{rel_target} listed under Locally Intaken",
                "local PDF exists without an index entry",
            )
        expected_md = f"markdown/{pdf_path.stem}.md"
        if not (PAPERS_DIR / expected_md).exists():
            finding(
                findings,
                "local_pdf_without_markdown",
                "blocking",
                repo_rel(pdf_path),
                repo_rel(PAPERS_DIR / expected_md),
                "missing",
            )

    for md_path in sorted(MARKDOWN_DIR.glob("*.md")):
        rel_target = md_path.relative_to(PAPERS_DIR).as_posix()
        if rel_target not in indexed_markdown_targets:
            finding(
                findings,
                "local_markdown_not_indexed",
                "warning",
                f"{repo_rel(MARKDOWN_DIR)}/*.md",
                f"{rel_target} listed under Locally Intaken",
                "local markdown exists without an index entry",
            )

    for metadata_path in sorted(METADATA_DIR.glob("*.json")):
        rel_target = metadata_path.relative_to(PAPERS_DIR).as_posix()
        if rel_target not in indexed_metadata_targets:
            finding(
                findings,
                "local_metadata_not_indexed",
                "warning",
                f"{repo_rel(METADATA_DIR)}/*.json",
                f"{rel_target} linked from Locally Intaken",
                "local metadata exists without an index entry",
            )

    local_ids = {normalize_arxiv_id(path.stem) for path in PAPERS_DIR.glob("*.pdf")}
    accidental = sorted(local_ids & queued)
    for arxiv_id in accidental:
        finding(
            findings,
            "queued_paper_has_local_pdf",
            "warning",
            f"{repo_rel(INDEX_PATH)}: Intake Queue",
            f"{arxiv_id} either queued or locally intaken, not both",
            "local PDF exists while paper remains queued",
        )


def check_ignored_pdf_note(index_text: str, findings: list[dict[str, Any]]) -> None:
    ignored_pdfs = sorted(path for path in PAPERS_DIR.glob("*.pdf") if is_ignored(path))
    if not ignored_pdfs:
        return
    lowered = index_text.lower()
    if "ignored" in lowered or "gitignore" in lowered:
        return
    finding(
        findings,
        "ignored_pdf_evidence_not_called_out",
        "warning",
        f"{repo_rel(INDEX_PATH)}: Conversion Notes",
        "index notes that local PDFs are intentionally gitignored evidence",
        "no gitignore/ignored note found in papers/index.md",
        "Reviewers should not confuse a clean git status with missing local paper evidence.",
    )


def check_status_and_logs(papers: list[IndexedPaper], findings: list[dict[str, Any]]) -> None:
    status = yaml.safe_load(STATUS_PATH.read_text(encoding="utf-8")) or {}
    paper_state = status.get("stages", {}).get(STAGE, {})
    done = bool(paper_state.get("done"))
    if done and not papers:
        finding(
            findings,
            "paper_intake_done_without_indexed_papers",
            "blocking",
            f"{repo_rel(STATUS_PATH)}:stages.paper_intake.done",
            "at least one locally intaken paper",
            "no Locally Intaken entries found",
        )

    if done:
        launch_logs = sorted(LOGS_DIR.glob(f"*_literate-workflow-programming_{STAGE}_launch-pack.json"))
        mark_done_logs = sorted(LOGS_DIR.glob(f"*_literate-workflow-programming_{STAGE}_mark-done.json"))
        if not launch_logs:
            finding(
                findings,
                "paper_intake_done_without_launch_log",
                "warning",
                f"{repo_rel(STATUS_PATH)}:stages.paper_intake.done",
                f"reviewable-runs/logs/*_{PACKAGE_KEY}_{STAGE}_launch-pack.json",
                "missing",
            )
        if not mark_done_logs:
            finding(
                findings,
                "paper_intake_done_without_mark_done_log",
                "blocking",
                f"{repo_rel(STATUS_PATH)}:stages.paper_intake.done",
                f"reviewable-runs/logs/*_{PACKAGE_KEY}_{STAGE}_mark-done.json",
                "missing",
            )

    next_stage_is_research = done and not bool(status.get("stages", {}).get("research", {}).get("done"))
    if done and not next_stage_is_research:
        finding(
            findings,
            "unexpected_next_stage_state",
            "warning",
            repo_rel(STATUS_PATH),
            "paper_intake done and research open",
            "research is already marked done or missing",
        )


def build_report() -> dict[str, Any]:
    index_text = INDEX_PATH.read_text(encoding="utf-8")
    papers = parse_indexed_papers(index_text)
    queue = queued_ids(index_text)
    findings: list[dict[str, Any]] = []

    check_index_links(index_text, findings)
    check_indexed_papers(index_text, papers, findings)
    check_directory_consistency(papers, queue, findings)
    check_ignored_pdf_note(index_text, findings)
    check_status_and_logs(papers, findings)

    blocking_count = sum(1 for item in findings if item["severity"] == "blocking")
    warning_count = sum(1 for item in findings if item["severity"] == "warning")
    ignored_pdfs = sorted(repo_rel(path) for path in PAPERS_DIR.glob("*.pdf") if is_ignored(path))
    report = {
        "kind": "spec_diff_report",
        "version": 1,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "package": PACKAGE_KEY,
        "stage": STAGE,
        "source": {
            "workflow_doc": repo_rel(WORKFLOW_DOC),
            "package_status": repo_rel(STATUS_PATH),
            "paper_index": repo_rel(INDEX_PATH),
        },
        "expected_state": {
            "evidence_surface": repo_rel(PAPERS_DIR),
            "local_pdf_count": len(list(PAPERS_DIR.glob("*.pdf"))),
            "local_markdown_count": len(list(MARKDOWN_DIR.glob("*.md"))),
            "local_metadata_count": len(list(METADATA_DIR.glob("*.json"))),
            "indexed_local_paper_count": len(papers),
            "queued_paper_count": len(queue),
            "ignored_pdf_count": len(ignored_pdfs),
            "ignored_pdfs_are_local_evidence": True,
        },
        "findings": findings,
        "summary": {
            "blocking": blocking_count,
            "warnings": warning_count,
            "status": "fail" if blocking_count else "pass_with_warnings" if warning_count else "pass",
        },
    }
    return report


def print_text(report: dict[str, Any]) -> None:
    summary = report["summary"]
    expected = report["expected_state"]
    print(f"Spec-diff: {report['package']} / {report['stage']}")
    print(f"Status: {summary['status']} ({summary['blocking']} blocking, {summary['warnings']} warning)")
    print(
        "Indexed/local counts: "
        f"{expected['indexed_local_paper_count']} indexed, "
        f"{expected['local_pdf_count']} PDFs, "
        f"{expected['local_markdown_count']} markdown, "
        f"{expected['local_metadata_count']} metadata"
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
