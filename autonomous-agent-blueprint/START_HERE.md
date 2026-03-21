# Start Here

This repo is most useful when treated as an architecture decision system, not as a pile of notes. The right reading path depends on what you are trying to do.

## Fastest Useful Path

If you only read seven things, read these:

1. `README.md`
2. `agentic-architectures-blueprint.md`
3. `practical-chapter-blueprints/README.md`
4. the chapter blueprint that matches your current bottleneck
5. the closest file in `use-cases/`
6. `reviewable-runs.md`
7. the closest dossier in `case-studies/`

Then use `evaluation/architecture-review-checklist.md` to pressure-test the result.

## Builder Path

Use this path if your question is: what should I build, what is the default, and when should I escalate?

1. `agentic-architectures-blueprint.md`
2. `practical-chapter-blueprints/README.md`
3. one or more chapter blueprints
4. `use-cases/enterprise-agent.md`, `use-cases/coding-agent.md`, or `use-cases/web-agent.md`
5. `reviewable-runs.md`
6. `case-studies/enterprise-policy-memo/README.md`, `case-studies/coding-bugfix-agent/README.md`, or `case-studies/web-form-agent/README.md`
7. `evaluation/architecture-review-checklist.md`
8. `evaluation/failure-mode-catalog.md`

Stop here when you can answer:

- what is the control loop
- what memory layers exist
- what action surface is used
- where verification happens
- where human approval happens
- what the main failure modes are

## Writer Path

Use this path if your question is: what is the argument, where do the claims come from, and how should the literature be framed?

1. `agentic-architectures-blueprint.md`
2. `foundation-agents-practical-chapters-guide.md`
3. `source-index.md`
4. `literature-quality.md`
5. the relevant chapter blueprint

Stop here when you can name the default method, the main alternatives, and the source support for each.

## Researcher Path

Use this path if your question is: what is in the corpus, how strong is it, and where are the gaps?

1. `source-index.md`
2. `literature-quality.md`
3. `papers/`
4. `notes/`

Stop here when you can identify:

- the core sources
- the cross-chapter papers
- the benchmark-heavy sources
- whether any local file needs a confidence warning or quarantine

## Recommended Reading By Problem

### If memory is the bottleneck

Read `practical-chapter-blueprints/01-memory-blueprint.md`, then `use-cases/enterprise-agent.md`.

### If reasoning or planning is the bottleneck

Read `practical-chapter-blueprints/02-reasoning-planning-blueprint.md`, then `use-cases/web-agent.md`.

### If tool use or action reliability is the bottleneck

Read `practical-chapter-blueprints/03-action-tool-use-blueprint.md`, then `use-cases/coding-agent.md` or `use-cases/web-agent.md`.

### If workflow quality is the bottleneck

Read `practical-chapter-blueprints/04-optimization-self-improvement-blueprint.md`, then `evaluation/architecture-review-checklist.md`.

### If you think you need multiple agents

Read `practical-chapter-blueprints/05-multi-agent-design-blueprint.md` before adding a second agent.

### If safety is blocking deployment

Read `practical-chapter-blueprints/06-safety-blueprint.md`, then `evaluation/failure-mode-catalog.md`.

## Document Roles

- `agentic-architectures-blueprint.md` gives the overall architecture spine.
- `practical-chapter-blueprints/` turns survey chapters into decision guides.
- `use-cases/` composes chapter defaults into end-to-end systems.
- `reviewable-runs.md` explains what a serious system must surface to make a run reviewable.
- `case-studies/` shows what those systems look like when applied to a concrete task through one linear dossier backed by runtime records and governance records.
- `evaluation/` tells you how to review and attack those systems on paper before implementation.
- `source-index.md` and `literature-quality.md` keep the repo auditable.
- `notes/` keeps exploratory material available without letting it dominate the main path.

## Completion Standard

You are using the repo correctly if you leave with:

- one candidate architecture
- one reasoned alternative
- a clear escalation rule
- a short failure checklist
- a named source trail for the key decisions
