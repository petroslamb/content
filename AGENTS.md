# AGENTS.md

## Purpose

This file is the local operator-facing orientation layer for `/Users/petros/Projects/content`.

Use it together with:

1. root [`README.md`](README.md) for the repo model
2. root [`AUTHORITY.md`](AUTHORITY.md) for the source-of-truth map and Phase 2 operator boundary
3. [`publications/README.md`](publications/README.md) for the canonical publication-package map
4. package `README.md` files for local structure
5. tracked [`workflows/README.md`](workflows/README.md) for canonical playbooks
6. [`scripts/README.md`](scripts/README.md) for tracked repo automation
7. tracked [`workflows/skills/README.md`](workflows/skills/README.md), with local `.agents/skills/` symlinked for Codex discovery

## Repo Model

The repo has three package classes:

- **Single-publication package**: one active essay project with a stable live draft plus local `archive/`
- **Umbrella package**: several related publications or a course/series sharing source layers, papers, or artifacts
- **Workflow/framework package**: tracked operational or conceptual infrastructure, not forced into the essay-package layout

Canonical content vocabulary:

- **live draft**
- **companion**
- **blueprint / plan**
- **claims / review artifacts**
- **artifacts**
- **archive**
- **papers**
- **distribution / socials**

For single-publication packages, prefer this paper-intake structure unless the package already has a stronger established variant:

- `papers/`
- `papers/markdown/`
- `papers/index.md`

## Where To Start By Task

| If you need to… | Start here | Then use |
| :--- | :--- | :--- |
| orient in the repo | [`README.md`](README.md) | [`publications/README.md`](publications/README.md) or the relevant support-package README |
| understand a package | that package’s `README.md` | the relevant workflow doc |
| intake or convert papers | [`workflows/paper-intake/README.md`](workflows/paper-intake/README.md) | [`workflows/skills/markitdown-paper-intake/`](workflows/skills/markitdown-paper-intake/) |
| research papers and discuss them | [`workflows/alphaxiv-research/README.md`](workflows/alphaxiv-research/README.md) | [`workflows/skills/alphaxiv/`](workflows/skills/alphaxiv/) |
| iterate an essay | [`workflows/essay-iteration/README.md`](workflows/essay-iteration/README.md) | package README and local review artifacts |
| generate NotebookLM artifacts | [`workflows/notebooklm-artifacts/README.md`](workflows/notebooklm-artifacts/README.md) | [`workflows/skills/notebooklm-artifact-bundle/`](workflows/skills/notebooklm-artifact-bundle/) and [`workflows/skills/pdf-slides-to-substack-images/`](workflows/skills/pdf-slides-to-substack-images/) |
| place images, use transcript round-trips, or do final editorial polish | [`workflows/article-polish/README.md`](workflows/article-polish/README.md) | package README plus the NotebookLM and PDF helper skills |
| publish to Substack | [`workflows/substack-publishing/README.md`](workflows/substack-publishing/README.md) | package README, `python-substack`, and series-specific helpers if they exist |
| sync the public archive or mirror | [`workflows/substack-archive-sync/README.md`](workflows/substack-archive-sync/README.md) | [`scripts/README.md`](scripts/README.md) and [`workflows/skills/substack-archive-sync/`](workflows/skills/substack-archive-sync/) |
| produce a narrated YouTube video from slides and audio | [`workflows/youtube-production/README.md`](workflows/youtube-production/README.md) | [`scripts/README.md`](scripts/README.md) and [`workflows/skills/youtube-slide-video-pipeline/`](workflows/skills/youtube-slide-video-pipeline/) |
| inspect auth, captions, playlists, or Shorts on YouTube | [`workflows/youtube-channel-ops/README.md`](workflows/youtube-channel-ops/README.md) | [`workflows/skills/youtube-data-api/`](workflows/skills/youtube-data-api/) or [`workflows/skills/youtube-shorts-maintenance/`](workflows/skills/youtube-shorts-maintenance/) |
| manage the Operating Agents YouTube series | [`workflows/youtube-series-operating-agents/README.md`](workflows/youtube-series-operating-agents/README.md) | [`workflows/skills/youtube-operating-agents/`](workflows/skills/youtube-operating-agents/) and [`workflows/skills/youtube-data-api/`](workflows/skills/youtube-data-api/) |
| inspect tracked automation | [`scripts/README.md`](scripts/README.md) | the specific script or workflow doc |
| perform security research or red-teaming survey | [`publications/security-research/README.md`](publications/security-research/README.md) | its local research papers and surveys |

## Authority And Operator Surface

For governed repo work, use [`AUTHORITY.md`](AUTHORITY.md) as the source-of-truth map.

The highest machine-authority layer is:

- per-workflow `workflow.yaml`
- package `status.yaml`
- [`harness_policy.yaml`](harness_policy.yaml)
- [`gate_contracts.yaml`](gate_contracts.yaml)
- [`pipeline_profiles.yaml`](pipeline_profiles.yaml)

The preferred governed operator entrypoint is `./content-agent`:

```bash
./content-agent status --package <package>
./content-agent next --package <package>
./content-agent validate --workflow <workflow_id> --package <package>
./content-agent run --workflow <workflow_id> --package <package>
./content-agent review list
./content-agent review inspect --gate <gate_id>
./content-agent resume --gate <gate_id>
```

Use `./content-cockpit --package <package>` when a browser surface is more useful than terminal output.

Treat `npm run stage:*` and `npm run workflow:*` as compatibility adapters unless a workflow doc explicitly calls for their narrow behavior.

## Stage Decision Checklist

For package-stage decisions, use this order:

1. read the package `status.yaml` first
2. do not infer the lifecycle stage from research notes or the live brief alone
3. read the package `README.md`
4. if `kind: umbrella`, read `umbrella_route` before assuming any leaf-style stage semantics
5. load `config.blueprint_path` when the manifest names one
6. if `essay_iteration` is active, seed or refresh the packet before making strong drafting-next-step claims

For umbrella packages, expect `current_stage: null` or another compatibility-only stage shell. The operational source of truth may be the umbrella route plus `./content-agent next`, not a leaf-style downstream stage.

## Local Skills

Tracked repo-local skills live under [`workflows/skills/README.md`](workflows/skills/README.md). The local `.agents/skills/` tree is a symlink mirror for Codex discovery and remains intentionally gitignored.

Key current local skills:

- `markitdown-paper-intake`
- `alphaxiv`
- `notebooklm-artifact-bundle`
- `pdf-slides-to-substack-images`
- `substack-archive-sync`
- `operating-agents-substack-sync`
- YouTube workflow skills

Tracked docs remain canonical. Do not let the `.agents/skills/` mirror become the only place where a shared workflow is explained.

The repo-local Codex hook mirror follows the same rule. Keep tracked hook docs and scripts canonical under [`scripts/`](scripts/README.md). Keep `.codex/` only as a local activation mirror.

## Writing Voice Policy

When writing or assisting with articles for this publication, read [`voice_consistency_guide.md`](voice_consistency_guide.md) before generating content.

Pay particular attention to:

- the ban list at the bottom of the guide
- the paragraph rhythm and auditor tone sections
- the characteristic moves section for thesis-driven pieces

The guide defines voice, not format. Structure varies by article type.

## Git Ignore Policy

This repo intentionally keeps hidden folders local-only. The `.gitignore` rule should continue to ignore all dot folders and hidden files except `.github/`.

- Do not force-add hidden folders such as `.agents/`, `.venv/`, `.youtube/`, `.claude/`, or similar when asked to "commit everything".
- If a user asks for a commit, stage the tracked, non-ignored subset unless they explicitly ask to change the ignore policy itself.

## Submodule Exceptions

While most publication packages are inlined into the main repository, certain packages remain as git submodules to preserve large evidence layers or independent commit history.

- **`publications/autonomy-tax`**: A documented exception. It maintains a 136MB history including large research datasets (`sources/raw/`) that are preserved in their original nested git structure.

## Python Environment Policy

This repository keeps a root-level virtual environment at `./.venv/` for shared local tooling.

- Use `./.venv/` for root-level automation and one-off content workflows.
- Do not create alternate root-level virtual environments unless there is a project-specific reason.
- Package-specific environments may still exist inside subprojects when already established there.

Bootstrap or refresh the root environment with:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/playwright install chromium
```

## Canonical Toolchain

The root article-development toolchain is:

- `markitdown[pdf]`
- `alphaxiv-py`
- `notebooklm-py[browser]`
- `python-substack`

Adjacent publishing automation:

- YouTube Data API Python client stack
- tracked repo scripts under `scripts/`

## Tool Notes

### markitdown

Use the repo-local binary for PDF to Markdown conversion:

```bash
.venv/bin/markitdown input.pdf -o output.md
```

The canonical paper-intake process lives in [`workflows/paper-intake/README.md`](workflows/paper-intake/README.md).

### alphaXiv

Use the repo-local CLI:

```bash
.venv/bin/alphaxiv --help
```

For assistant-backed research, expect browser auth via `alphaxiv auth login-web`. The canonical research workflow lives in [`workflows/alphaxiv-research/README.md`](workflows/alphaxiv-research/README.md).

### NotebookLM

Use the repo-local CLI:

```bash
.venv/bin/notebooklm --help
```

First-time authentication is interactive:

```bash
.venv/bin/notebooklm login
```

The canonical artifact workflow lives in [`workflows/notebooklm-artifacts/README.md`](workflows/notebooklm-artifacts/README.md).

### Substack

Use the `python-substack` module from the root environment for publishing-oriented scripting:

```bash
.venv/bin/python -c "import substack; help(substack)"
```

The canonical publishing workflow lives in [`workflows/substack-publishing/README.md`](workflows/substack-publishing/README.md).

### Archive And Mirror

Refresh the tracked publication archive with:

```bash
npm run sync:substack
```

The detailed script map lives in [`scripts/README.md`](scripts/README.md). The archive itself is documented in [`publication_strategy_and_archive/README.md`](publication_strategy_and_archive/README.md).

## Dependency Source

The direct root-level tooling dependencies are tracked in [`requirements.txt`](requirements.txt).
