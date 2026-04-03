from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parents[1]
OLD_PACKAGE_PATHS = (
    "agent_revolution",
    "ai_agents_enterprise_state",
    "autonomous-agent-blueprint",
    "binding-and-recoverability",
    "ethereum_llm_governance",
    "hardware_compatibility_architecture_2023_2025",
    "multi_agent_compiler_workaround",
    "neural_architectures",
    "rlm_jupyter",
    "the-moltbook-phenomenon",
)
TEXT_EXTS = {".md", ".html", ".py", ".js", ".yaml", ".yml", ".json", ".txt", ".cff"}
EXCLUDED_FILES = {
    "publication_strategy_and_archive/link_migration_manifest.yaml",
    ".gitmodules",
}
ROOT_ABS_PREFIX = "/Users/petros/Projects/content/"

MD_LINK_PATTERN = re.compile(r"(?P<prefix>!?\[[^\]]*\]\()(?P<target><[^>\n]+>|[^)\n]+)(?P<suffix>\))")
HTML_ATTR_PATTERN = re.compile(r'(?P<prefix>(?:href|src)=\")(?P<target>[^\"]+)(?P<suffix>\")')
FENCED_CODE_PATTERN = re.compile(r"```.*?```", re.DOTALL)
OLD_GITHUB_PATTERN = re.compile(
    r"https?://github\.com/petroslamb/content/(?:blob|tree)/main/"
    r"(agent_revolution|ai_agents_enterprise_state|autonomous-agent-blueprint|binding-and-recoverability|"
    r"ethereum_llm_governance|hardware_compatibility_architecture_2023_2025|multi_agent_compiler_workaround|"
    r"neural_architectures|rlm_jupyter|the-moltbook-phenomenon)"
)


def tracked_files() -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=False,
    )
    files: list[Path] = []
    for item in proc.stdout.split(b"\x00"):
        if not item:
            continue
        rel = item.decode("utf-8")
        if rel in EXCLUDED_FILES:
            continue
        path = REPO_ROOT / rel
        if path.suffix.lower() in TEXT_EXTS and path.is_file():
            files.append(path)
    return files


def normalize_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
        if ' "' in target and not target.startswith("http"):
            target = target.split(" ", 1)[0]
    return target


def strip_fragment_and_query(target: str) -> str:
    return target.split("#", 1)[0].split("?", 1)[0]


def is_external(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:", "tel:", "data:"))


def check_relative_target(file_path: Path, raw_target: str) -> str | None:
    target = normalize_target(raw_target)
    if not target or target.startswith("#"):
        return None
    if "{{" in target or "}}" in target:
        return None
    if target.startswith(("cid:", "cci:", "javascript:")):
        return None
    if target.startswith(ROOT_ABS_PREFIX):
        return f"absolute local path remains: {raw_target}"
    parsed = urlparse(target)
    if parsed.scheme or is_external(target):
        return None
    if ":0:0-0:0" in target:
        return None
    if all(marker not in target for marker in ("/", ".")):
        return None
    if target.startswith(("artifacts/", "assets/", "slides/")) or any(
        marker in target for marker in ("/artifacts/", "/assets/", "/slides/")
    ):
        return None
    if Path(target).suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".m4a", ".mp3", ".pdf", ".txt", ".srt"}:
        return None
    target = strip_fragment_and_query(target)
    if not target:
        return None
    resolved = (file_path.parent / target).resolve()
    if not resolved.exists():
        return f"broken relative link: {raw_target}"
    return None


def validate_links(file_path: Path, text: str) -> list[str]:
    errors: list[str] = []
    rel = file_path.relative_to(REPO_ROOT).as_posix()
    if file_path.suffix.lower() != ".md":
        return errors
    if not (
        rel == "README.md"
        or rel.endswith("/README.md")
        or rel.startswith("workflows/")
        or rel.startswith("publication_strategy_and_archive/substack_archive/")
    ):
        return errors
    text = FENCED_CODE_PATTERN.sub("", text)
    for match in MD_LINK_PATTERN.finditer(text):
        maybe_error = check_relative_target(file_path, match.group("target"))
        if maybe_error:
            errors.append(maybe_error)
    return errors


def validate_text(file_path: Path, text: str) -> list[str]:
    errors: list[str] = []
    rel = file_path.relative_to(REPO_ROOT).as_posix()

    if ROOT_ABS_PREFIX in text and rel != "scripts/check_repo_links.py":
        errors.append("contains absolute local repo path")

    if OLD_GITHUB_PATTERN.search(text):
        errors.append("contains stale github.com/petroslamb/content old-package URL")

    if "github.com/petroslamb/autonomy-tax-enterprise-agents" in text and rel != "scripts/check_repo_links.py":
        errors.append("contains legacy autonomy-tax repo URL")

    if "github.com/petroslamb/content/blob/main/publications/" not in text:
        pass

    return errors + validate_links(file_path, text)


def main() -> int:
    failures: list[tuple[str, str]] = []
    for file_path in tracked_files():
        text = file_path.read_text(encoding="utf-8", errors="ignore")
        for error in validate_text(file_path, text):
            failures.append((file_path.relative_to(REPO_ROOT).as_posix(), error))

    if failures:
        for rel, error in failures:
            print(f"{rel}: {error}")
        return 1

    print("repo links OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
