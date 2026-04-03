# Rooted Layers — Research Repository

This is the source material, research corpus, and companion reference for [Rooted Layers](https://lambpetros.substack.com), a publication on AI engineering, architecture economics, and production systems.

Each article on Substack links to the corresponding folder here for readers who want to go deeper: primary sources, evidence tables, scorecard datasets, architecture audits, and working drafts that did not make it into the final piece.

**What you will find here:**
- Research packages for published articles, each with their own README
- Evidence layers: source manifests, annotated bibliographies, and scoring rubrics
- A local archive of published articles in markdown and HTML snapshots
- Working notes and in-progress research that may become future articles

This is a living repository. Folders without a README are either legacy material or works in progress.

---

## Repository Organization

Organized by topic. Each top-level folder corresponds to a research area or multi-part publication.

### Substack Metadata & Archiving
The canonical record of published articles, along with publication analysis and future strategy drafts, is maintained in the `publication_strategy_and_archive/` directory. Archive refreshes run through `scripts/sync_substack_archive.py`, which pulls the public publication feed, refreshes normalized markdown and HTML snapshots, localizes assets, and updates the tracked manifest in `publication_strategy_and_archive/substack_archive/`.

For orientation across the tracked root-level automation scripts, start with [`scripts/README.md`](./scripts/README.md).

For the public mirror pipeline, use:

- `npm run sync:substack` to refresh the tracked archive
- `npm run build:mirror` to generate the GitHub Pages mirror
- `npm run dev:mirror` to work on the mirror locally
- `npm run check:mirror` to verify the archive, generated mapping table, and built site

The public mirror is published at [https://petroslamb.github.io/content/](https://petroslamb.github.io/content/).

Implementation docs live in:

- [`publication_strategy_and_archive/README.md`](./publication_strategy_and_archive/README.md)
- [`publication_strategy_and_archive/mirror/README.md`](./publication_strategy_and_archive/mirror/README.md)
- [`scripts/README.md`](./scripts/README.md)

### Publication to Folder Mapping

The following table maps published Substack articles to their corresponding source folders in this repository:

<!-- GENERATED_PUBLICATION_MAP:START -->
| Substack Publication | Repository Folder |
| :--- | :--- |
| **The Illusion of the Swarm** | `multi_agent_compiler_workaround/` |
| **The Moltbook Phenomenon** | `the-moltbook-phenomenon/` |
| **The Autonomy Tax** | `ai_agents_enterprise_state/` |
| **The Transformer Attractor** | `neural_architectures/` |
| **When the LLM Programs Its Own Thinking** | `rlm_jupyter/` |
| **The Orchestration Paradigm: Issue 4 - The Reality** | `agent_revolution/` |
| **The Orchestration Paradigm: Issue 3 - The Behavior** | `agent_revolution/` |
| **The Orchestration Paradigm: Issue 2 - The Factory** | `agent_revolution/` |
| **The Orchestration Paradigm Series** | `agent_revolution/` |
| **The Hardware Friction Map** | `hardware_compatibility_architecture_2023_2025/` |
| **What Actually Works: The Hardware Compatibility Filter in Neural Architecture (2023–2025)** | `hardware_compatibility_architecture_2023_2025/` |
| **Autonomous AI Agents: Core Foundations and Recent Breakthroughs** | `autonomous-agent-blueprint/` |
| **Neural Architecture Design as a Compositional Language** | `neural_architectures/` |
| **Welcome** | *(N/A / Root)* |
<!-- GENERATED_PUBLICATION_MAP:END -->

## Current Packages

### [`ai_agents_enterprise_state/`](./ai_agents_enterprise_state/)

Research and writing package for **The Autonomy Tax**, a three-piece publication series on why enterprise agents fail on control rather than intelligence.

- Implemented publication package: `v8A`, `v8B`, `v8C`
- Evidence layer: `sources/`, including a source manifest and derived casebook
- Scoring assets: `assets/` with scorecard templates and rubric material

Start with: `ai_agents_enterprise_state/README.md`

### [`autonomous-agent-blueprint/`](./autonomous-agent-blueprint/)

Local research corpus on foundation agents organized into a practical architecture guide and chapter-specific blueprints.

- Main synthesis: `agentic-architectures-blueprint.md`
- Chapter mapping: `foundation-agents-practical-chapters-guide.md`
- Supporting material: `practical-chapter-blueprints/` and `papers/`

Start with: `autonomous-agent-blueprint/README.md`

### [`reviewable-runs/`](./reviewable-runs/)

Standalone framework package for making important agent runs inspectable, reviewable, and governable after execution.

- Public front door: `README.md`
- Operator guide: `USE_IT.md`
- Examples and proof: `examples/`
- Review instruments and templates: `evaluation/`, `templates/`

Start with: `reviewable-runs/README.md`

### [`hardware_compatibility_architecture_2023_2025/`](./hardware_compatibility_architecture_2023_2025/)

Published research project: **What Actually Works: The Hardware Compatibility Filter in Neural Architecture (2023-2025)**. This package studies why GPU-friendly architectures dominate production and includes the associated hardware friction methodology and dataset.

- Canonical article and publication drafts
- Quantitative scorecard and research artifacts
- Supporting evidence on MoE adoption, FlashAttention, and SSM limits
- Links to the public hardware friction scorecard dataset repository

Start with: `hardware_compatibility_architecture_2023_2025/README.md`

### [`publication_strategy_and_archive/`](./publication_strategy_and_archive/)

Centralized corpus for the Substack publication, containing the complete downloaded archive of published articles alongside detailed qualitative analysis and future strategic planning artifacts.

- Publication qualitative analysis and review matrix
- Future strategic blueprints and options
- Canonical downloaded article markdown and metadata
- Curated post-to-folder mapping for published essays
- 11ty GitHub Pages mirror and deployment workflow

Start with: `publication_strategy_and_archive/README.md`

## Tooling

This repository uses local tools for content workflows, tracked in `requirements.txt` and documented in `AGENTS.md`. Key tools include:
- `markitdown` for PDF conversion
- `notebooklm-py` for NotebookLM integration
- the official Google Python client stack for YouTube Data API workflows
- `scripts/sync_substack_archive.py` for Substack archive sync and manifest refresh

For the repo-level script map and workflow grouping, use [`scripts/README.md`](./scripts/README.md).

Additionally, the repository incorporates two programmatic APIs for Substack publishing and posting workflows:
- **Python Substack Interface**: `python-substack` (Origin: [ma2za/python-substack](https://github.com/ma2za/python-substack))
- **TypeScript Substack Interface**: `substack-api` (Origin: [jakub-k-slys/substack-api](https://github.com/jakub-k-slys/substack-api))

## Other Top-Level Directories

These directories exist at the repository root but do not currently expose a package-level `README.md`:

- `agent_revolution/`
- `neural_architectures/`
- `paper_reviews/`
- `reference/`
- `rooted layers/`
- `security_research/`

Treat them as supporting or legacy material unless they are documented separately.

## Notes

- This root README summarizes the packages that currently define their own root-level documentation.
- For current status, entry points, and working rules, use each package README as the source of truth.
