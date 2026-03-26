# Essays: Operating Agents

This folder contains the public *Operating Agents* essay package. Each topic folder keeps the current `v7` essay, the archived `v6` baseline, the current companion, its local README, and any presentation artifacts together.

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

`v7` is the live publication candidate. `v6` remains the archived comparison baseline.

## Folder Map

- `launch-note/` - series framing
- `action/` - action and tool use
- `reasoning/` - reasoning and planning
- `memory/` - memory and lifecycle
- `multi-agent/` - multi-agent design
- `safety/` - safety and attack surfaces
- `optimization/` - optimization bonus post
- `operating-agents-coverage-map-v7.md` - bridge from the live essays to companions, blueprints, source notes, and the wider survey

## What Lives In A Topic Folder

Each topic folder contains the current `v7` essay, the archived `v6` essay baseline, the current `companion-v7.md`, the earlier companion baseline, the local `README.md`, and `artifacts/` when presentation material exists.

The companion is intentionally local now. It is not a short appendix or a bare reference list. It is a substantial second-pass essay for the interested reader: broader chapter terrain, booklet context, omitted method surface, and fuller source interpretation that would have overcomplicated the public post.

## Reading Order

### Current narrative order

1. `launch-note/00-launch-note-v7.md`
2. `action/01-action-tool-use-v7.md`
3. `memory/03-memory-v7.md`
4. `reasoning/02-reasoning-planning-v7.md`
5. `multi-agent/04-multi-agent-v7.md`
6. `safety/05-safety-v7.md`
7. `optimization/06-optimization-v7.md`

### Topic-to-blueprint mapping

- Action essay `01` -> `../core/practical-chapter-blueprints/03-action-tool-use-blueprint.md`
- Reasoning essay `02` -> `../core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md`
- Memory essay `03` -> `../core/practical-chapter-blueprints/01-memory-blueprint.md`
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
