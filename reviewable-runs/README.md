# Reviewable Runs

This package is a standalone framework for making important agent runs inspectable, reviewable, and governable.

It did not originate as a literature distillation. It emerged from a gap in the `autonomous-agent-blueprint` package: the blueprints explain what a serious system should do, but they do not by themselves define what a serious run should expose or reconstruct for human review.

Use this package when your question is not only "how should the agent be built?" but also "after the agent acts, what should a reviewer be able to inspect?"

## Start Here

1. `START_HERE.md`
2. `ORIGIN_AND_GAP.md`
3. `reviewable-runs.md`
4. `dossiers/README.md`
5. `evaluation/README.md`
6. `templates/README.md`
7. `MATURITY_AND_VALIDATION.md`

## Package Map

- `reviewable-runs.md`: canonical model and six review questions
- `dossiers/`: worked examples that answer those questions for concrete runs
- `evaluation/`: review instruments for architectures and runs
- `templates/`: direct record templates plus adjacent support patterns
- `history/`: the older packet-oriented lineage kept for reference
- `ORIGIN_AND_GAP.md`: why this package exists and how it emerged
- `MATURITY_AND_VALIDATION.md`: what is strong, what is synthetic, and what still needs proof

## What This Is

- a run reviewability framework
- a practical standard for reconstructing meaningful runs
- a bridge between architecture, oversight, debugging, and postmortem review

## What This Is Not

- not a literature-first research package
- not a model interpretability framework
- not a generic logging manifesto
- not a requirement that every trivial run emit a heavy dossier

## Reading Paths

### If you want the concept

Read `ORIGIN_AND_GAP.md`, then `reviewable-runs.md`, then `MATURITY_AND_VALIDATION.md`.

### If you want concrete examples

Read `reviewable-runs.md`, then `dossiers/comparison-matrix.md`, then the closest dossier.

### If you want to implement it

Read `reviewable-runs.md`, then `evaluation/README.md`, then `templates/README.md`.

### If you want the upstream architecture basis

Read `../autonomous-agent-blueprint/core/agentic-architectures-blueprint.md`, then `../autonomous-agent-blueprint/core/practical-chapter-blueprints/README.md`, then the closest use case under `../autonomous-agent-blueprint/implementation/use-cases/`.
