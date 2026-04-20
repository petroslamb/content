# Rooted Layers

This repository is the canonical working tree behind [Rooted Layers](https://lambpetros.substack.com). Most tracked content lives under [`publications/`](publications/README.md): essay packages, umbrella publication packages, supporting artifacts, and local research surfaces.

The root is meant to stay navigable. Root docs orient you. Package `README.md` files explain local structure. Tracked workflow docs explain repeatable processes. Tracked repo-local skills live under [`workflows/skills/`](workflows/skills/README.md) and are mirrored into local `.agents/skills/` for Codex discovery.

## North Star

The repo is organized around one main lifecycle:

0. discover and clear potential essay topics before package initialization when the topic is not yet settled
1. intake papers and convert them into usable markdown
2. research and shortlist sources
3. draft and iterate essays with review artifacts
4. generate NotebookLM artifacts
5. polish the article with images, transcript insights, and references
6. run the release gate before external publication or sync
7. publish to Substack
8. sync the public archive and mirror

That lifecycle does not force one rigid folder shape on every package. The repo uses three package classes:

- **Single-publication package**: one live essay surface plus local `archive/`
- **Umbrella package**: several related publications or a course/series sharing papers, artifacts, or source layers
- **Workflow/framework package**: tracked operational infrastructure, not forced into the essay-package layout

## Start Here

| Surface | Role | Start Here |
| :--- | :--- | :--- |
| `publications/` | Canonical essay and publication packages | [`publications/README.md`](publications/README.md) |
| `phased-strategy/` | Phase roadmap, closure gates, and productization strategy | [`phased-strategy/README.md`](phased-strategy/README.md) |
| `workflows/` | Canonical tracked playbooks | [`workflows/README.md`](workflows/README.md) |
| `scripts/` | Tracked repo automation | [`scripts/README.md`](scripts/README.md) |
| `publication_strategy_and_archive/` | Substack archive, mirror, publication map, and editorial atlas | [`publication_strategy_and_archive/README.md`](publication_strategy_and_archive/README.md) |
| `reviewable-runs/` | Reviewable execution framework and examples | [`reviewable-runs/README.md`](reviewable-runs/README.md) |
| `publications/security-research/` | Research bucket, not yet normalized into publication packages | [`publications/security-research/README.md`](publications/security-research/README.md) |

Use these layers in order:

1. root README
2. [`publications/README.md`](publications/README.md) or the relevant workflow/support README
3. the specific package `README.md`
4. the matching workflow doc in [`workflows/`](workflows/README.md)
5. tracked scripts and tracked skills if execution help is needed

## Harness Surface

The repo now exposes a tracked harness-facing surface for Codex-style operation:

- [`harness_contract.yaml`](harness_contract.yaml): machine-readable repo contract
- [`harness_policy.yaml`](harness_policy.yaml): local-first autonomy and approval boundaries

Stable entrypoints:

- `npm run stage:next -- --package <package> --format json`
- `npm run stage:resolve -- --package <package> --stage <stage> --format json`
- `npm run stage:run -- --package <package> --stage <stage> --format json`
- `npm run package:init -- --idea "..." --format json`
- `npm run check:harness`
- `npm run check:reviewable-runs`

These surfaces do not replace the workflow docs. They make the existing lifecycle legible to an external harness without relying on a long custom prompt.

When the essay object itself is still undecided, use [`workflows/topic-discovery/README.md`](workflows/topic-discovery/README.md) before `package:init`. Topic discovery is a pre-package decision layer, not a `status.yaml` lifecycle stage yet.

## Canonical Vocabulary

Across content packages, use these terms consistently:

- **live draft**
- **companion**
- **blueprint / plan**
- **claims / review artifacts**
- **artifacts**
- **archive**
- **papers**
- **distribution / socials**

For single-publication packages, the default paper-intake convention is:

- `papers/`
- `papers/markdown/`
- `papers/index.md`

Umbrella packages may preserve stronger established variants when those structures already carry more meaning than the generic layout.

## Publications Layer

Essay and publication packages now live under [`publications/`](publications/README.md). That directory is the canonical package index and the right place to understand:

- which folders are single-publication packages vs umbrellas
- which publication packages map to published Substack essays
- where live drafts, companions, papers, artifacts, and archives live for each package
- which packages are still transitional or structurally uneven

Root keeps only the cross-package orientation. Package-level detail belongs in `publications/README.md` and the local package READMEs.

## Publication To Package Mapping

The published archive is tracked centrally in `publication_strategy_and_archive/substack_archive/`. The generated table below maps published Substack posts to their canonical package or umbrella package in this repo.

<!-- GENERATED_PUBLICATION_MAP:START -->
| Substack Publication | Repository Folder |
| :--- | :--- |
| **Confidence Debt** | `publications/confidence-debt/` |
| **The Binding Gap** | `publications/binding-gap/` |
| **The Illusion of the Swarm** | `publications/illusion-of-swarm/` |
| **The Moltbook Phenomenon** | `publications/moltbook-phenomenon/` |
| **The Autonomy Tax** | `publications/autonomy-tax/` |
| **The Transformer Attractor** | `publications/neural-architectures/` |
| **When the LLM Programs Its Own Thinking** | `publications/programmable-thinking/` |
| **The Orchestration Paradigm: Issue 4 - The Reality** | `publications/orchestration-paradigm/` |
| **The Orchestration Paradigm: Issue 3 - The Behavior** | `publications/orchestration-paradigm/` |
| **The Orchestration Paradigm: Issue 2 - The Factory** | `publications/orchestration-paradigm/` |
| **The Orchestration Paradigm Series** | `publications/orchestration-paradigm/` |
| **The Hardware Friction Map** | `publications/hardware-friction/` |
| **What Actually Works: The Hardware Compatibility Filter in Neural Architecture (2023–2025)** | `publications/hardware-friction/` |
| **Autonomous AI Agents: Core Foundations and Recent Breakthroughs** | `publications/autonomous-agents/` |
| **Neural Architecture Design as a Compositional Language** | `publications/neural-architectures/neural-architecture-design-as-a-compositional-32e/` |
| **Operating Agents: Preface** | `publications/autonomous-agents/essays/launch-note/` |
| **Operating Agents I: Action Systems and Tool Use** | `publications/autonomous-agents/essays/action/` |
| **Operating Agents II: Memory Systems and Authority** | `publications/autonomous-agents/essays/memory/` |
| **Operating Agents III: Reasoning Scaffolds and Planning** | `publications/autonomous-agents/essays/reasoning/` |
| **Operating Agents IV: Multi-Agent Boundaries and Handoffs** | `publications/autonomous-agents/essays/multi-agent/` |
| **Operating Agents V: Trust Boundaries and Agent Safety** | `publications/autonomous-agents/essays/safety/` |
| **Operating Agents Bonus: Workflow Optimization and Evaluation** | `publications/autonomous-agents/essays/optimization/` |
| **Measuring Trust: The Gap Between AI Auditing and Correctness** | `publications/evidence-governance/archive/measuring-trust-the-gap-between-ai/` |
| **The Five-Component Pattern for AI Evidence Governance** | `publications/evidence-governance/archive/the-five-component-pattern-for-ai/` |
| **Your AI Is Confidently Wrong — And You Have No Rule for What to Do About It** | `publications/evidence-governance/your-ai-is-confidently-wrong-and/` |
| **Welcome** | *(N/A / Root)* |
<!-- GENERATED_PUBLICATION_MAP:END -->

Published posts may map to umbrella packages or nested subpackages rather than one folder per post. That is intentional.

## Workflow Layer

Tracked workflow docs live in [`workflows/`](workflows/README.md). The current article-development canon is:

- [`workflows/topic-discovery/README.md`](workflows/topic-discovery/README.md)
- [`workflows/package-normalization/README.md`](workflows/package-normalization/README.md)
- [`workflows/paper-intake/README.md`](workflows/paper-intake/README.md)
- [`workflows/alphaxiv-research/README.md`](workflows/alphaxiv-research/README.md)
- [`workflows/essay-iteration/README.md`](workflows/essay-iteration/README.md)
- [`workflows/notebooklm-artifacts/README.md`](workflows/notebooklm-artifacts/README.md)
- [`workflows/article-polish/README.md`](workflows/article-polish/README.md)
- [`workflows/release-gate/README.md`](workflows/release-gate/README.md)
- [`workflows/substack-publishing/README.md`](workflows/substack-publishing/README.md)
- [`workflows/substack-archive-sync/README.md`](workflows/substack-archive-sync/README.md)

Adjacent YouTube and channel operations live in the same tracked layer:

- [`workflows/youtube-production/README.md`](workflows/youtube-production/README.md)
- [`workflows/youtube-channel-ops/README.md`](workflows/youtube-channel-ops/README.md)
- [`workflows/youtube-series-operating-agents/README.md`](workflows/youtube-series-operating-agents/README.md)

## Toolchain

The canonical root toolchain is tracked in [`requirements.txt`](requirements.txt) and explained operationally in local [`AGENTS.md`](AGENTS.md).

Core tools:

- `markitdown[pdf]`
- `alphaxiv-py`
- `notebooklm-py[browser]`
- `python-substack`

Adjacent publishing automation:

- tracked scripts under [`scripts/`](scripts/README.md)
- tracked skill bundles under [`workflows/skills/`](workflows/skills/README.md)

## Skills

Tracked repo-local skills live under [`workflows/skills/`](workflows/skills/README.md). The local `.agents/skills/` tree is a discovery mirror for Codex, not the canonical documentation layer.

Use workflow docs to understand the process. Use skill bundles to execute that process efficiently.
