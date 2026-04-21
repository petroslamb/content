#!/usr/bin/env python3
"""
Install or refresh the repo-local .codex Stop-hook mirror.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[1]
TRACKED_HOOKS_DIR = REPO_ROOT / "scripts" / "codex_hooks"
LOCAL_CODEX_DIR = REPO_ROOT / ".codex"
LOCAL_HOOKS_DIR = LOCAL_CODEX_DIR / "hooks"
GLOBAL_CONFIG_PATH = Path.home() / ".codex" / "config.toml"
LOCAL_CONFIG_PATH = LOCAL_CODEX_DIR / "config.toml"
TRACKED_HOOKS_JSON = TRACKED_HOOKS_DIR / "hooks.json"
TRACKED_STOP_HOOK = TRACKED_HOOKS_DIR / "stop_lifecycle_check.py"
HOOKS_ENABLED_RE = re.compile(r"^\s*codex_hooks\s*=\s*true\s*$", re.MULTILINE)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def hooks_enabled(path: Path) -> bool:
    if not path.exists():
        return False
    return bool(HOOKS_ENABLED_RE.search(path.read_text()))


def ensure_local_config() -> tuple[str, str | None]:
    if hooks_enabled(LOCAL_CONFIG_PATH):
        return "ready", None
    if LOCAL_CONFIG_PATH.exists():
        if hooks_enabled(GLOBAL_CONFIG_PATH):
            return "global", None
        return "manual", (
            "Local .codex/config.toml already exists and does not enable codex_hooks. "
            "Enable hooks manually or remove the file and rerun the installer."
        )

    ensure_dir(LOCAL_CODEX_DIR)
    LOCAL_CONFIG_PATH.write_text("[features]\ncodex_hooks = true\n")
    return "created", None


def install_symlink(source: Path, target: Path) -> tuple[str, str | None]:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() or target.is_symlink():
        if target.is_symlink():
            try:
                if target.resolve() == source.resolve():
                    return "kept", None
            except FileNotFoundError:
                pass
            target.unlink()
        else:
            return "skipped", f"Refusing to overwrite non-symlink local file: {target.relative_to(REPO_ROOT)}"
    target.symlink_to(source)
    return "linked", None


def main() -> None:
    parser = argparse.ArgumentParser(description="Install the repo-local Codex Stop-hook mirror.")
    parser.add_argument(
        "--package",
        default="literate-workflow-programming",
        help="Package used in the suggested verification command.",
    )
    args = parser.parse_args()

    ensure_dir(LOCAL_HOOKS_DIR)
    config_status, config_warning = ensure_local_config()
    hook_status, hook_warning = install_symlink(TRACKED_HOOKS_JSON, LOCAL_CODEX_DIR / "hooks.json")
    script_status, script_warning = install_symlink(TRACKED_STOP_HOOK, LOCAL_HOOKS_DIR / "stop_lifecycle_check.py")

    print("Repo-local Codex Stop hook mirror")
    print(f"  config.toml: {config_status}")
    print(f"  hooks.json: {hook_status}")
    print(f"  stop hook: {script_status}")
    for warning in [config_warning, hook_warning, script_warning]:
        if warning:
            print(f"WARNING: {warning}")

    print("\nNext verification commands:")
    print("  ls -l .codex/hooks.json .codex/hooks/stop_lifecycle_check.py")
    print(f"  npm run check:package-lifecycle -- --package {args.package}")


if __name__ == "__main__":
    main()
