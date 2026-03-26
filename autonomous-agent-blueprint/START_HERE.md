# Start Here

This repo is most useful when treated as an architecture decision system, not as a pile of notes. The path depends on what you need.

## Fastest Useful Path

If you only read seven things, read these:

1. `README.md`
2. `REPOSITORY_ANALYSIS.md`
3. `core/agentic-architectures-blueprint.md`
4. `core/practical-chapter-blueprints/README.md`
5. the chapter blueprint that matches your current bottleneck
6. the closest file in `implementation/use-cases/`
7. `core/reviewable-runs.md`

Then use `implementation/evaluation/architecture-review-checklist.md` to pressure-test the result.

## Builder Path

Use this path if your question is: what should I build, what is the default, and when should I escalate?

1. `core/agentic-architectures-blueprint.md`
2. `core/practical-chapter-blueprints/README.md`
3. one or more chapter blueprints
4. `implementation/use-cases/enterprise-agent.md`, `implementation/use-cases/coding-agent.md`, or `implementation/use-cases/web-agent.md`
5. `core/reviewable-runs.md`
6. `implementation/case-studies/enterprise-policy-memo/README.md`, `implementation/case-studies/coding-bugfix-agent/README.md`, or `implementation/case-studies/web-form-agent/README.md`
7. `implementation/evaluation/architecture-review-checklist.md`
8. `implementation/evaluation/failure-mode-catalog.md`

Stop here when you can answer:

- what is the control loop
- what memory layers exist
- what action surface is used
- where verification happens
- where human approval happens
- what the main failure modes are

## Operating Agents Path

Use this path if your question is: what is the public argument and where does the deeper material live?

1. `essays/README.md`
2. `essays/launch-note/00-launch-note-v4.md`
3. the relevant `essays/*/*-v4.md` essay
4. the local `essays/*/companion.md`
5. the matching file in `core/practical-chapter-blueprints/`
6. the matching file in `reference/papers/`

## Writer Path

Use this path if your question is: what is the argument, where do the claims come from, and how should the literature be framed?

1. `core/agentic-architectures-blueprint.md`
2. `reference/chapters-guide.md`
3. `reference/practical-distillation.md`
4. `reference/source-index.md`
5. `reference/literature-quality.md`
6. the relevant chapter blueprint

## Researcher Path

Use this path if your question is: what is in the corpus, how strong is it, and where are the gaps?

1. `reference/source-index.md`
2. `reference/literature-quality.md`
3. `reference/papers/`
4. `notes/`

## Recommended Reading By Problem

### If memory is the bottleneck

Read `core/practical-chapter-blueprints/01-memory-blueprint.md`, then `implementation/use-cases/enterprise-agent.md`.

### If reasoning or planning is the bottleneck

Read `core/practical-chapter-blueprints/02-reasoning-planning-blueprint.md`, then `implementation/use-cases/web-agent.md`.

### If tool use or action reliability is the bottleneck

Read `core/practical-chapter-blueprints/03-action-tool-use-blueprint.md`, then `implementation/use-cases/coding-agent.md` or `implementation/use-cases/web-agent.md`.

### If workflow quality is the bottleneck

Read `core/practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md`, then `implementation/evaluation/architecture-review-checklist.md`.

### If you think you need multiple agents

Read `core/practical-chapter-blueprints/05-multi-agent-design-blueprint.md` before adding a second agent.

### If safety is blocking deployment

Read `core/practical-chapter-blueprints/06-safety-blueprint.md`, then `implementation/evaluation/failure-mode-catalog.md`.

## Document Roles

- `REPOSITORY_ANALYSIS.md` explains the repo structure, layer purposes, and common confusions.
- `core/agentic-architectures-blueprint.md` gives the overall architecture spine.
- `core/practical-chapter-blueprints/` turns survey chapters into decision guides.
- `implementation/use-cases/` composes chapter defaults into end-to-end systems.
- `core/reviewable-runs.md` explains what a serious system must surface to make a run reviewable.
- `implementation/case-studies/` shows what those systems look like for concrete tasks.
- `implementation/evaluation/` tells you how to review and attack those systems on paper before implementation.
- `reference/` keeps the literature and source trail auditable.
- `essays/` is the public narrative layer.
- `notes/` keeps exploratory material available without letting it dominate the main path.

## Completion Standard

You are using the repo correctly if you leave with:

- one candidate architecture
- one reasoned alternative
- a clear escalation rule
- a short failure checklist
- a named source trail for the key decisions
