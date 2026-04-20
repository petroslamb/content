#!/usr/bin/env python3
"""Validate package-local alphaXiv assistant discussion tracking."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLICATIONS_DIR = REPO_ROOT / "publications"
DISCUSSION_INDEX = Path("research-notes") / "alphaxiv-discussions" / "index.md"
SESSION_ID_RE = re.compile(
    r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    re.IGNORECASE,
)
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\n]+)\)")


def package_roots(selected_package: str | None = None) -> list[Path]:
    if selected_package:
        root = PUBLICATIONS_DIR / selected_package
        if not root.exists():
            raise FileNotFoundError(f"Package not found: publications/{selected_package}")
        return [root]
    return sorted(
        [path.parent for path in PUBLICATIONS_DIR.rglob("status.yaml")],
        key=lambda path: len(path.parts),
        reverse=True,
    )


def deepest_package_for(path: Path, roots: list[Path]) -> Path | None:
    for root in roots:
        try:
            path.relative_to(root)
        except ValueError:
            continue
        return root
    return None


def should_skip_markdown(package_root: Path, path: Path) -> bool:
    rel = path.relative_to(package_root)
    parts = rel.parts
    if len(parts) >= 2 and parts[0] == "papers" and parts[1] == "markdown":
        return True
    if len(parts) >= 2 and parts[0] == "sources" and parts[1] == "raw":
        return True
    return False


def markdown_by_package(roots: list[Path]) -> dict[Path, list[Path]]:
    assigned: dict[Path, list[Path]] = {root: [] for root in roots}
    for path in PUBLICATIONS_DIR.rglob("*.md"):
        root = deepest_package_for(path, roots)
        if root is None or should_skip_markdown(root, path):
            continue
        assigned[root].append(path)
    return assigned


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def extract_session_refs(path: Path) -> list[tuple[str, int]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lower = text.lower()
    if "alphaxiv" not in lower or ("assistant" not in lower and "session" not in lower):
        return []
    return [(match.group(0), line_number(text, match.start())) for match in SESSION_ID_RE.finditer(text)]


def is_relative_markdown_link(raw_target: str) -> bool:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return False
    return target.split("#", 1)[0].endswith(".md")


def check_index_links(index_path: Path) -> list[str]:
    errors: list[str] = []
    text = index_path.read_text(encoding="utf-8", errors="ignore")
    for match in MD_LINK_RE.finditer(text):
        raw_target = match.group(1)
        if not is_relative_markdown_link(raw_target):
            continue
        target = raw_target.strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        target = target.split("#", 1)[0]
        resolved = (index_path.parent / target).resolve()
        if not resolved.exists():
            rel = index_path.relative_to(REPO_ROOT).as_posix()
            errors.append(f"{rel}: linked extraction note is missing: {raw_target}")
    return errors


def check_package(package_root: Path, markdown_files: list[Path]) -> list[str]:
    errors: list[str] = []
    refs: dict[str, list[tuple[Path, int]]] = {}
    for path in markdown_files:
        for session_id, lineno in extract_session_refs(path):
            refs.setdefault(session_id, []).append((path, lineno))

    if not refs:
        return errors

    index_path = package_root / DISCUSSION_INDEX
    package_label = package_root.relative_to(PUBLICATIONS_DIR).as_posix()
    if not index_path.exists():
        sessions = ", ".join(sorted(refs))
        errors.append(
            f"publications/{package_label}: alphaXiv assistant session refs found but "
            f"{DISCUSSION_INDEX.as_posix()} is missing ({sessions})"
        )
        return errors

    index_text = index_path.read_text(encoding="utf-8", errors="ignore")
    for session_id, locations in sorted(refs.items()):
        if session_id in index_text:
            continue
        location = locations[0][0].relative_to(REPO_ROOT).as_posix()
        lineno = locations[0][1]
        errors.append(
            f"{location}:{lineno}: alphaXiv assistant session {session_id} "
            f"is not listed in {index_path.relative_to(REPO_ROOT).as_posix()}"
        )

    errors.extend(check_index_links(index_path))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", help="Package path relative to publications/")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    roots = package_roots(args.package)
    assignments = markdown_by_package(roots)
    errors: list[str] = []
    for root in sorted(assignments):
        errors.extend(check_package(root, assignments[root]))

    payload = {
        "success": not errors,
        "checked_packages": [root.relative_to(PUBLICATIONS_DIR).as_posix() for root in sorted(assignments)],
        "errors": errors,
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    elif errors:
        for error in errors:
            print(error)
    else:
        print("alphaXiv discussions OK")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
