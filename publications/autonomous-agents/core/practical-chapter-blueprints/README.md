# Practical Chapter Blueprints

This folder contains the six builder-facing decision guides. It is the stable core of the repo.

## Inputs

These blueprints are grounded in:

- `../../reference/chapters-guide.md`
- `../../reference/practical-distillation.md`
- `../../reference/source-index.md`
- `../../reference/papers/`

## How To Use This Folder

Read in build order:

1. `01-memory-blueprint.md`
2. `02-reasoning-planning-blueprint.md`
3. `03-action-tool-use-blueprint.md`
4. `04-optimization-self-improvement-blueprint.md`
5. `05-multi-agent-design-blueprint.md`
6. `06-safety-blueprint.md`

That order mirrors the engineering dependency chain:

- memory determines what the system can persist
- reasoning determines how it works through tasks
- action determines what it can do in software
- optimization determines how it improves
- multi-agent design determines when one agent should become many
- safety determines how the whole stack remains deployable

## What Each Blueprint Should Answer

- what is the default method here
- what are the main alternatives
- when should I escalate
- what should I avoid
- how should I evaluate the choice

## Shared Interpretation

Across the six guides, one common position is maintained:

- the practical center of agentic architecture is not human-like intelligence
- the practical center is a bounded workflow that can reason, act, remember, verify, and operate safely
- most teams should start with one well-designed workflow and only then add dynamic routing, long-lived memory, specialist agents, or self-optimization
