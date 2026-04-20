# Essays: Operating Agents

This folder is the live essay package for *Operating Agents*. It is the public course-chapter layer inside the broader [`publications/autonomous-agents/`](../README.md) umbrella package.

## Package Role

- Archetype: Umbrella subpackage
- Status: Active course package
- Live draft surface: one canonical essay plus one canonical companion per topic, with a local `archive/` and `artifacts/` inside each topic folder
- Canonical workflow docs: [`../../workflows/essay-iteration/README.md`](../../../workflows/essay-iteration/README.md), [`../../workflows/notebooklm-artifacts/README.md`](../../../workflows/notebooklm-artifacts/README.md), [`../../workflows/substack-publishing/README.md`](../../../workflows/substack-publishing/README.md)

## Course Goal

The purpose of *Operating Agents* is to teach how modern agent systems are designed, evaluated, and constrained in practice. These essays should read as course chapters for builders, not as internal notes and not as slogan-first opinion pieces.

## Folder Map

- [`launch-note/`](launch-note/) holds the live course framing and preface.
- [`action/`](action/) holds the action and tool-use chapter.
- [`memory/`](memory/) holds the memory and lifecycle chapter.
- [`reasoning/`](reasoning/) holds the reasoning and planning chapter.
- [`multi-agent/`](multi-agent/) holds the handoffs and boundary-design chapter.
- [`safety/`](safety/) holds the trust-boundary and attack-surface chapter.
- [`optimization/`](optimization/) holds the optimization and evaluation bonus chapter.
- Topic-level NotebookLM notebook mappings live in each topic `status.yaml` and are indexed in [`../../notebooklm-notebooks.md`](../../notebooklm-notebooks.md).

## Canonical Topic Layout

Each topic folder should contain:

- one canonical live essay file
- one canonical live `companion.md`
- `artifacts/` when presentation media exists
- a local `archive/` for prior drafts, retired companions, and historical support files
- `status.yaml` with NotebookLM fields when the topic has a notebook

The package standard is stable live chapter plus local archive history, not version-only sprawl.

## Reading Order

- [`launch-note/preface.md`](launch-note/preface.md)
- [`action/01-action-tool-use.md`](action/01-action-tool-use.md)
- [`action/companion.md`](action/companion.md)
- [`memory/02-memory-systems-and-authority.md`](memory/02-memory-systems-and-authority.md)
- [`memory/companion.md`](memory/companion.md)
- [`reasoning/03-reasoning-scaffolds-and-planning.md`](reasoning/03-reasoning-scaffolds-and-planning.md)
- [`reasoning/companion.md`](reasoning/companion.md)
- [`multi-agent/04-multi-agent-boundaries-and-handoffs.md`](multi-agent/04-multi-agent-boundaries-and-handoffs.md)
- [`multi-agent/companion.md`](multi-agent/companion.md)
- [`safety/05-trust-boundaries-and-agent-safety.md`](safety/05-trust-boundaries-and-agent-safety.md)
- [`safety/companion.md`](safety/companion.md)
- [`optimization/06-workflow-optimization-and-evaluation.md`](optimization/06-workflow-optimization-and-evaluation.md)
- [`optimization/companion.md`](optimization/companion.md)

## Relationship To Other Surfaces

- [`../core/`](../core/) contains the builder-facing defaults and chapter blueprints.
- [`../reference/`](../reference/) contains the paper notes, source index, and literature-quality layer.
- [`../implementation/`](../implementation/) contains practical use cases and evaluation-adjacent material.
