# Codex Hook Mirror

This directory is the tracked source for the repo-supported Codex hook assets.

The live activation path remains the repo-local `.codex/` folder, but that tree stays intentionally gitignored. Use [`../install_codex_stop_hook.py`](../install_codex_stop_hook.py) to create or refresh the local mirror.

Current supported hook surface:

- `hooks.json`: repo-local `Stop` hook wiring
- `stop_lifecycle_check.py`: lifecycle backstop for stage, governing-brief, and packet assertions

Working rule:

- keep canonical behavior here
- keep `.codex/` local-only
- use the installer script to mirror these assets into `.codex/`
- do not store personal Codex state, auth, history, or memories here
