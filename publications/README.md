# Publications

This directory is the canonical home for Rooted Layers essay and publication packages.

Most content work should start here. The package `README.md` files under this directory are the local source of truth for:

- the live draft surface
- companions, blueprints, and review artifacts
- paper intake and source layers
- artifacts and archive history
- publication mapping back to Substack

## Package Classes

Two content-package classes live here:

- **Single-publication package**: one primary essay line with a stable live draft and local archive
- **Umbrella package**: several related publications or a course/series sharing source layers, artifacts, or supporting material

Workflow/framework packages stay at the repository root and are documented elsewhere.

## Current Package Map

| Folder | Archetype | Status | Notes |
| :--- | :--- | :--- | :--- |
| [`autonomy-tax/`](autonomy-tax/README.md) | Single-publication | Published | Three-piece publication package; nested git repo with its own history |
| [`binding-gap/`](binding-gap/README.md) | Single-publication | Active | Canonical live binding-gap essay plus companion and artifact pipeline |
| [`evidence-governance/`](evidence-governance/README.md) | Single-publication | Active / unpublished in Rooted Layers archive | Main essay plus governance-pattern companion and external proof repo |
| [`illusion-of-swarm/`](illusion-of-swarm/README.md) | Single-publication | Published | alphaXiv-driven research package behind *The Illusion of the Swarm* |
| [`moltbook-phenomenon/`](moltbook-phenomenon/README.md) | Single-publication | Published | Essay, background analysis, slides, and distribution assets |
| [`programmable-thinking/`](programmable-thinking/README.md) | Single-publication | Published | RLM/Jupyter publication package with companion paper and visuals |
| [`autonomous-agents/`](autonomous-agents/README.md) | Umbrella | Published umbrella / active course | Foundation-agent manual plus the Operating Agents course |
| [`hardware-friction/`](hardware-friction/README.md) | Umbrella | Published umbrella | Hardware-friction map, scorecard, long-form article, and dataset |
| [`neural-architectures/`](neural-architectures/README.md) | Umbrella | Published umbrella | Architecture-language essay line including *The Transformer Attractor* |
| [`orchestration-paradigm/`](orchestration-paradigm/README.md) | Umbrella | Published umbrella | The Orchestration Paradigm series and ToolOrchestra research package |

## Canonical Single-Publication Contract

When a package is single-publication, the default target shape is:

- package `README.md`
- one explicit live draft surface
- optional companion surface
- `papers/`
- `papers/markdown/`
- `papers/index.md`
- `artifacts/`
- `archive/`
- optional `distribution/`, `socials/`, or local `scripts/`

Packages do not need to become identical. Stronger local variants such as `sources/`, `visuals/`, or topic-specific evidence trees can stay when they are more meaningful than the generic layout. The package README must map those variants back to the canonical vocabulary.

## Canonical Umbrella Contract

When a package is an umbrella, it should expose:

- a strong root `README.md`
- one clear subpackage map
- the live publication surfaces or nested subpackage READMEs
- the shared source or paper layer where relevant

Umbrella packages should not pretend to be single-publication packages when their real structure is course-, series-, or dataset-shaped.

## Working Rule

If you are unsure where an essay belongs:

1. start with the package README in this directory
2. if the package is unclear, consult the archive map in [`../publication_strategy_and_archive/post_map.yaml`](../publication_strategy_and_archive/post_map.yaml)
3. if the task is procedural, move to the tracked workflow layer in [`../workflows/README.md`](../workflows/README.md)
