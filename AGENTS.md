# AGENTS.md

## Repo Map

Use the root [README.md](./README.md) for the current package map. For package-specific context, treat each package `README.md` as the source of truth:

- [ai_agents_enterprise_state/README.md](./ai_agents_enterprise_state/README.md)
- [autonomous-agent-blueprint/README.md](./autonomous-agent-blueprint/README.md)
- [hardware_compatibility_architecture_2023_2025/README.md](./hardware_compatibility_architecture_2023_2025/README.md)

## Python Environment Policy

This repository now keeps a root-level virtual environment at `./.venv/` for shared local tooling.

- Use `./.venv/` for root-level automation and one-off content workflows.
- Do not create additional root-level virtual environments such as `venv/` or alternate `.venv-*` folders unless there is a project-specific reason.
- Package-specific virtual environments may still exist inside subprojects when they are already established there.

Bootstrap or refresh the root environment with:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/playwright install chromium
```

## Tooling In This Repo

### PDF to Markdown

Use `markitdown` from the repo-local environment for PDF to Markdown conversion:

```bash
.venv/bin/markitdown input.pdf -o output.md
```

Example:

```bash
.venv/bin/markitdown path/to/paper.pdf -o path/to/paper.md
```

### NotebookLM

Use `notebooklm-py` from the repo-local environment to communicate with NotebookLM:

```bash
.venv/bin/notebooklm --help
```

First-time authentication is interactive:

```bash
.venv/bin/notebooklm login
```

Common commands:

```bash
.venv/bin/notebooklm list
.venv/bin/notebooklm create "Notebook Name"
.venv/bin/notebooklm use <notebook-id>
.venv/bin/notebooklm ask "Question"
```

Notes:

- `notebooklm-py` uses browser-based session authentication, not an API key.
- The default auth storage path is outside the repo under `~/.notebooklm/storage_state.json`.
- If auth storage is ever redirected into the repo, keep it under a gitignored path such as `./.notebooklm/`.
- Treat NotebookLM auth files as credentials.

### Substack Downloader

Use the `substack-downloader` submodule to fetch and archive Substack posts:

```bash
cd substack-downloader
.venv/bin/python scraper.py --url https://lambpetros.substack.com/
```
The downloaded markdown archives and JSON metadata are saved into `substack-downloader/archive/lambpetros.substack.com/`. For this repository, the canonical archive for the publication has been moved to the root `publication_strategy_and_archive/` folder.

### Substack Publishing (Python Interface)

Use the `python-substack` module from the root virtual environment to programmatically authenticate and publish posts. 

```bash
# To find help or usage examples:
.venv/bin/python -c "import substack; help(substack)"
# Origin documentation: https://github.com/ma2za/python-substack
```

### Substack APIs (TypeScript Interface)

Use the `substack-api` npm package installed in the root directory for TypeScript/JavaScript node scripting.

```bash
# To find help on classes and usage:
cat node_modules/substack-api/README.md
# Origin documentation: https://github.com/jakub-k-slys/substack-api
```

## Dependency Source

The direct root-level tooling dependencies are tracked in [requirements.txt](./requirements.txt).
