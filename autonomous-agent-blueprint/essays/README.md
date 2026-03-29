# Essays: Operating Agents

This folder contains the live *Operating Agents* essay package. Each topic folder now holds one canonical live essay, one root-level `companion-v7.md`, presentation artifacts when they exist, and a local `archive/` folder for historical drafts, prior companions, local READMEs, and older publication candidates.

## Course Goal

The purpose of *Operating Agents* is to teach how modern agent systems are designed, evaluated, and constrained in practice. The essays should read as course chapters, not as internal notes and not as slogan-first opinion pieces.

That goal changes the quality bar. A strong chapter should help a reader understand the mechanism, learn a usable build methodology, and know which references deserve deeper study.

## A+++ Standard

For this package, `A+++` means course-quality public writing:

- each core essay can stand on its own without depending on lecture notes or internal source language
- each essay defines the core concepts before using the specialized vocabulary
- each essay teaches a practical methodology from baseline design to justified escalation
- each essay explains why the cited papers matter instead of listing them as badges
- the literature supports the lesson, while companions and blueprints carry the wider taxonomy

If a serious builder cannot read a chapter, understand the operating problem, and apply its method to a real workflow review next week, the essay is not finished.

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
