# Practical Chapter Blueprints

This folder turns the practical chapters identified in `foundation-agents-practical-chapters-guide.md` into chapter-level architecture guides.

The source guide isolates six chapters or chapter groups that matter most for builders:

1. Chapter 3: Memory
2. Chapter 2: Reasoning and Planning
3. Chapter 8: Action Systems and Tool Use
4. Chapters 9 and 11: Optimization and Self-Improvement
5. Chapter 14: Multi-Agent Design
6. Chapters 17, 18, and 19: Safety

Each file in this folder does four things:

- restates what the chapter is trying to solve
- synthesizes the local anchor papers into a practical literature view
- proposes a concrete blueprint you could actually build from
- separates stable defaults from optional or frontier escalations

## How To Use This Folder

Read these files in the same order recommended by the practical guide:

1. `01-memory-blueprint.md`
2. `02-reasoning-planning-blueprint.md`
3. `03-action-tool-use-blueprint.md`
4. `04-optimization-self-improvement-blueprint.md`
5. `05-multi-agent-design-blueprint.md`
6. `06-safety-blueprint.md`

That order mirrors the real engineering dependency chain:

- memory determines what the system can persist
- reasoning determines how it works through tasks
- action determines what it can do in software
- optimization determines how it improves
- multi-agent design determines when one agent should become many
- safety determines how the whole stack remains deployable

## Shared Interpretation

Across the six guides, one common position is maintained:

- The practical center of agentic architecture is not "human-like intelligence."
- The practical center is a bounded workflow that can reason, act, remember, verify, and operate safely.
- Most teams should start with one well-designed agentic workflow and only then add dynamic routing, long-lived memory, specialist agents, or self-optimization.

## File Map

### `01-memory-blueprint.md`
How to design short-term, semantic, episodic, and procedural memory as a managed system rather than a larger prompt.

### `02-reasoning-planning-blueprint.md`
How to pick the right reasoning scaffold, from decomposition and ReAct to verification and search.

### `03-action-tool-use-blueprint.md`
How to choose action surfaces, design tool layers, and represent actions so they are testable and replayable.

### `04-optimization-self-improvement-blueprint.md`
How to improve prompts, schemas, routing, tool policies, and workflow structure after a baseline exists.

### `05-multi-agent-design-blueprint.md`
How to decide when multiple agents are justified, what roles they should take, and how they should exchange work.

### `06-safety-blueprint.md`
How to treat prompt injection, unsafe tools, poisoned retrieval, and agent-to-agent contamination as architecture problems.

## Notes On The Local Literature

These chapter guides were built from:

- `foundation-agents-practical-chapters-guide.md`
- `foundation-agents-practical-distillation.md`
- the local paper files under `papers/`

When a local file appears mislabeled or ambiguous, the guide favors the chapter guide's interpretation and avoids making that paper a core dependency. The clearest example is the `AgentSmith` reference in the safety chapter, where the local PDF does not appear to match the expected agent paper.
