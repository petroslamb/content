# Rooted Layers — Research Repository

This repository is the canonical working tree behind [Rooted Layers](https://lambpetros.substack.com). Most top-level folders are content-development packages for essays, supporting research, publication artifacts, and related distribution material.

The repo is meant to stay readable as it grows. The root docs orient you. Package README files explain local structure. Tracked workflow docs explain repeatable processes. Tracked repo-local skills now live under [`workflows/skills/`](./workflows/skills/README.md) and are mirrored into `.agents/skills/` for Codex discovery.

## North Star

Most folders in this repo are trying to support the same broad lifecycle:

1. collect papers and convert them into usable markdown
2. research and shortlist sources
3. draft and iterate essays with supporting review artifacts
4. generate NotebookLM media artifacts
5. publish to Substack and sync the public archive

That lifecycle does not force every package into one rigid layout. The repo uses three package classes:

- **Single-publication package**: one active essay project with a stable live draft surface plus local `archive/`
- **Umbrella package**: multiple related publications or a course/series sharing papers, assets, or source layers
- **Workflow/framework package**: tracked operational or conceptual infrastructure, not forced into the essay-package layout

## How The Repo Works

Use these layers in order:

1. **Package README**: the local source of truth for a folder’s structure, live draft surface, and publication map
2. **Tracked workflows**: [`workflows/README.md`](./workflows/README.md) for canonical article-development playbooks
3. **Scripts**: [`scripts/README.md`](./scripts/README.md) for tracked repo automation code
4. **Publication archive**: [`publication_strategy_and_archive/README.md`](./publication_strategy_and_archive/README.md) for the public archive and mirror system
5. **Tracked skills**: [`workflows/skills/README.md`](./workflows/skills/README.md) for the tracked skill bundle layer, mirrored locally into `.agents/skills/`

## Canonical Vocabulary

Across content packages, the repo now uses these terms consistently:

- **live draft**: the current canonical working essay path
- **companion**: a second-pass supporting markdown that broadens or contextualizes the main essay
- **blueprint / plan**: control document that shapes the essay or package direction
- **claims / review artifacts**: scoring, critique, or evidence-control files used during iteration
- **artifacts**: visuals, podcasts, videos, slide exports, transcripts, and related media outputs
- **archive**: prior drafts, superseded companions, retired review files, and older local support material
- **papers**: source PDFs and related paper intake material
- **distribution / socials**: platform-specific posting assets or external-distribution material

For **single-publication packages**, the canonical paper-intake convention is:

- `papers/`
- `papers/markdown/`
- `papers/index.md`

Umbrella packages can preserve stronger existing variants where they already carry more structure, such as:

- [`autonomous-agent-blueprint/reference/papers/`](./autonomous-agent-blueprint/reference/papers/)
- [`autonomous-agent-blueprint/reference/source-index.md`](./autonomous-agent-blueprint/reference/source-index.md)
- hardware scorecard paper trees inside [`hardware_compatibility_architecture_2023_2025/`](./hardware_compatibility_architecture_2023_2025/)

## Canonical Package Map

The table below classifies the current top-level documented packages. Published articles may map to a shared umbrella package rather than one folder per post.

| Folder | Archetype | Status | Orientation |
| :--- | :--- | :--- | :--- |
| `agent_revolution/` | Umbrella package | Published umbrella | [`README.md`](./agent_revolution/README.md) |
| `ai_agents_enterprise_state/` | Single-publication package | Published | [`README.md`](./ai_agents_enterprise_state/README.md) |
| `autonomous-agent-blueprint/` | Umbrella package | Published umbrella / active course | [`README.md`](./autonomous-agent-blueprint/README.md) |
| `binding-and-recoverability/` | Single-publication package | Active | [`README.md`](./binding-and-recoverability/README.md) |
| `ethereum_llm_governance/` | Single-publication package | Active | [`README.md`](./ethereum_llm_governance/README.md) |
| `hardware_compatibility_architecture_2023_2025/` | Umbrella package | Published umbrella | [`README.md`](./hardware_compatibility_architecture_2023_2025/README.md) |
| `multi_agent_compiler_workaround/` | Single-publication package | Published | [`README.md`](./multi_agent_compiler_workaround/README.md) |
| `neural_architectures/` | Umbrella package | Published umbrella | [`README.md`](./neural_architectures/README.md) |
| `publication_strategy_and_archive/` | Workflow/support package | Canonical archive infrastructure | [`README.md`](./publication_strategy_and_archive/README.md) |
| `reviewable-runs/` | Workflow/framework package | Standalone framework package | [`README.md`](./reviewable-runs/README.md) |
| `rlm_jupyter/` | Single-publication package | Published | [`README.md`](./rlm_jupyter/README.md) |
| `scripts/` | Workflow/support package | Tracked repo automation | [`README.md`](./scripts/README.md) |
| `security_research/` | Research bucket | Active research bucket | [`README.md`](./security_research/README.md) |
| `the-moltbook-phenomenon/` | Single-publication package | Published | [`README.md`](./the-moltbook-phenomenon/README.md) |
| `workflows/` | Workflow/support package | Canonical tracked playbooks | [`README.md`](./workflows/README.md) |

Folders without a package README should be treated as supporting or legacy material until they are normalized.

## Publication To Package Mapping

The published archive is tracked centrally in `publication_strategy_and_archive/substack_archive/`. The generated table below maps published Substack posts to their canonical package or umbrella package in this repo.

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

## Canonical Workflow Layer

Tracked workflow docs live in [`workflows/`](./workflows/). The current article-development canon is:

- [`workflows/paper-intake/README.md`](./workflows/paper-intake/README.md)
- [`workflows/alphaxiv-research/README.md`](./workflows/alphaxiv-research/README.md)
- [`workflows/essay-iteration/README.md`](./workflows/essay-iteration/README.md)
- [`workflows/notebooklm-artifacts/README.md`](./workflows/notebooklm-artifacts/README.md)
- [`workflows/substack-publishing/README.md`](./workflows/substack-publishing/README.md)

Adjacent publishing and channel workflows live in the same tracked layer:

- [`workflows/substack-archive-sync/README.md`](./workflows/substack-archive-sync/README.md)
- [`workflows/youtube-production/README.md`](./workflows/youtube-production/README.md)
- [`workflows/youtube-channel-ops/README.md`](./workflows/youtube-channel-ops/README.md)
- [`workflows/youtube-series-operating-agents/README.md`](./workflows/youtube-series-operating-agents/README.md)

Use these as the tracked source of truth for repeatable processes. Package README files should point at them instead of duplicating long playbooks.

## Toolchain

The canonical article-development toolchain is tracked in [`requirements.txt`](./requirements.txt) and explained operationally in local [`AGENTS.md`](./AGENTS.md).

Core tools:

- `markitdown[pdf]` for paper-to-markdown conversion
- `alphaxiv-py` for paper discovery, inspection, and assistant-backed research
- `notebooklm-py[browser]` for artifact generation and transcript round-trips
- `python-substack` for publishing automation

Adjacent publishing automation:

- [`scripts/README.md`](./scripts/README.md) for tracked repo scripts
- tracked helper skills under [`workflows/skills/`](./workflows/skills/README.md), mirrored locally into `.agents/skills/`

## Skill Bundles

Tracked repo-local skills live under [`workflows/skills/`](./workflows/skills/README.md). The local `.agents/skills/` tree is now a symlink mirror used for Codex discovery.

The tracked skill bundles should stay thinner than the workflow docs in [`workflows/`](./workflows/). They exist to execute the workflows efficiently, not to become the only place where the repo process is explained.

Current skill families include:

- paper intake and PDF conversion
- alphaXiv research
- NotebookLM artifact generation
- Substack archive and series-specific publishing
- YouTube production and publishing automation

Use the root README and tracked workflow docs to understand how the repo works. Use local skills to execute that work efficiently in a Codex session.
