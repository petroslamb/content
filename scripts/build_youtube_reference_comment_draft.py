#!/usr/bin/env python3
"""Build a curated YouTube reference-comment draft from a local synced essay."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REFERENCE_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+.*(references|bibliography)", re.IGNORECASE)
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^\s*-\s+(.*)$")
ITALIC_TITLE_RE = re.compile(r"\*([^*]+)\*")
BOLD_LABEL_RE = re.compile(r"^\s*\*\*([^*]+)\*\*\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a draft YouTube references comment from a local synced essay.")
    parser.add_argument("--markdown-file", required=True, type=Path, help="Local synced essay markdown file.")
    parser.add_argument("--video-title", required=True, help="Video title for the draft header.")
    parser.add_argument("--essay-url", help="Canonical essay URL for the final full-references link.")
    parser.add_argument("--max-refs", type=int, default=5, help="Maximum references to keep in the draft. Default: 5.")
    parser.add_argument("--output-markdown", type=Path, help="Optional markdown output path.")
    parser.add_argument("--output-json", type=Path, help="Optional JSON output path.")
    return parser.parse_args()


def find_reference_section(lines: list[str]) -> tuple[int, int] | None:
    start = None
    start_level = None
    for idx, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        if REFERENCE_HEADING_RE.match(line):
            start = idx + 1
            start_level = len(match.group(1))
            break
    if start is None or start_level is None:
        return None
    for idx in range(start, len(lines)):
        match = HEADING_RE.match(lines[idx])
        if match and len(match.group(1)) <= start_level:
            return start, idx
    return start, len(lines)


def squash_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_reference_items(lines: list[str]) -> list[dict[str, str]]:
    section = find_reference_section(lines)
    if section is None:
        return []
    start, end = section
    items: list[dict[str, str]] = []
    current_heading = "References"
    current_item: list[str] = []
    for raw_line in lines[start:end]:
        heading = HEADING_RE.match(raw_line)
        if heading:
            if current_item:
                items.append(build_item(current_heading, current_item))
                current_item = []
            current_heading = squash_whitespace(heading.group(2))
            continue
        bold_label = BOLD_LABEL_RE.match(raw_line)
        if bold_label:
            if current_item:
                items.append(build_item(current_heading, current_item))
                current_item = []
            current_heading = squash_whitespace(bold_label.group(1))
            continue
        bullet = BULLET_RE.match(raw_line)
        if bullet:
            if current_item:
                items.append(build_item(current_heading, current_item))
            current_item = [bullet.group(1).strip()]
            continue
        if current_item and raw_line.strip():
            current_item.append(raw_line.strip())
    if current_item:
        items.append(build_item(current_heading, current_item))
    return [item for item in items if item.get("title")]


def last_sentence(text: str) -> str:
    parts = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
    return parts[-1] if parts else text.strip()


def derive_title(text: str) -> str:
    italic = ITALIC_TITLE_RE.search(text)
    if italic:
        return squash_whitespace(italic.group(1))
    parts = [part.strip() for part in text.split(".") if part.strip()]
    return parts[0] if parts else squash_whitespace(text)


def build_item(section_heading: str, raw_parts: list[str]) -> dict[str, str]:
    citation = squash_whitespace(" ".join(raw_parts))
    title = derive_title(citation)
    guidance = last_sentence(citation)
    if guidance == citation:
        guidance = ""
    return {
        "section": section_heading,
        "title": title,
        "guidance": guidance,
        "citation": citation,
    }


def build_markdown(video_title: str, refs: list[dict[str, str]], essay_url: str | None) -> str:
    lines = [
        f"Draft references comment for: {video_title}",
        "",
        "This brief leans most heavily on these sources:",
        "",
    ]
    for ref in refs:
        if ref["guidance"]:
            lines.append(f"- **{ref['title']}** — {ref['guidance']}")
        else:
            lines.append(f"- **{ref['title']}**")
    if essay_url:
        lines.extend(["", f"Full essay + full references: {essay_url}"])
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    lines = args.markdown_file.read_text(encoding="utf-8").splitlines()
    refs = parse_reference_items(lines)[: args.max_refs]
    payload: dict[str, Any] = {
        "markdown_file": str(args.markdown_file),
        "video_title": args.video_title,
        "essay_url": args.essay_url,
        "max_refs": args.max_refs,
        "reference_count": len(refs),
        "references": refs,
        "comment_markdown": build_markdown(args.video_title, refs, args.essay_url),
    }

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if args.output_markdown:
        args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
        args.output_markdown.write_text(payload["comment_markdown"], encoding="utf-8")
    if not args.output_json and not args.output_markdown:
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
