# Essays: Operating Agents

This folder contains the live *Operating Agents* essay package. Each topic folder now holds one canonical live essay, one root-level `companion-v7.md`, presentation artifacts when they exist, and a local `archive/` folder for historical drafts, prior companions, local READMEs, and older publication candidates.

## Doctrine Goal

The purpose of *Operating Agents* is not only to publish polished essays. The package exists to turn agent literature into an operating doctrine for builders.

That goal changes the quality bar. The series should be memorable because builders can reuse it in design reviews, postmortems, and architecture arguments, not only because the prose reads smoothly in a feed.

## A+++ Standard

For this package, `A+++` means doctrine-level public writing:

- each core essay gives builders one hard law they can carry into real decisions
- each essay names the enemy mistake it is trying to eliminate
- each essay gives a practical decision rule and an escalation rule
- each essay anchors the doctrine in one vivid failure archetype
- the literature serves the doctrine; companions and blueprints carry the wider taxonomy

If a serious builder cannot lift a sentence from a chapter and use it to clarify an architecture argument next week, the essay is not finished.

## Folder Map

- `launch-note/` - series framing
- `action/` - action and tool use
- `reasoning/` - reasoning and planning
- `memory/` - memory and lifecycle
- `multi-agent/` - multi-agent design
- `safety/` - safety and attack surfaces
- `optimization/` - optimization bonus post

## What Lives In A Topic Folder

Each topic folder contains:

- one canonical live essay file
- one root-level `companion-v7.md`
- `artifacts/` when presentation material exists
- a local `archive/` folder for earlier drafts, prior baselines, and historical support files

## Reading Order

### Live essay layer

- `action/01-action-tool-use.md`
- `memory/02-memory-systems-and-authority.md`
- `reasoning/03-reasoning-scaffolds-and-planning.md`
- `multi-agent/04-multi-agent-boundaries-and-handoffs.md`
- `safety/05-trust-boundaries-and-agent-safety.md`
- `optimization/06-workflow-optimization-and-evaluation.md`

Use the local `archive/` folder inside a topic if you need earlier drafts, prior baselines, or `with-slides` variants. The launch note and breadth-layer materials currently live under `launch-note/archive/`.

### Topic-to-blueprint mapping

- Action essay `01` -> `../core/practical-chapter-blueprints/03-action-tool-use-blueprint.md`
- Memory essay `02` -> `../core/practical-chapter-blueprints/01-memory-blueprint.md`
- Reasoning essay `03` -> `../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md`
- Multi-agent essay `04` -> `../core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md`
- Safety essay `05` -> `../core/practical-chapter-blueprints/06-safety-blueprint.md`
- Optimization essay `06` -> `../core/practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md`

## Relationship To Other Surfaces

- `../core/` contains the builder-facing defaults and reviewability contract.
- `../reference/` contains the survey guide, distillation docs, source index, quality notes, and paper notes.
- `../implementation/` contains use cases, case studies, evaluation docs, and templates.

## Drafting Support

Rewrite ledgers and planning notes live under `../notes/essay-evolution/`.

Current active rewrite target:

- `../notes/essay-evolution/essay-evolution-v6-to-v7.md` defines the doctrine-first `v7` rewrite plan.
- `../notes/essay-evolution/essay-v7-doctrine-packs.md` locks the chapter-level doctrine packs behind the live `v7` drafts.
