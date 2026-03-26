# Reviewable Runs

Reviewable Runs is a practical framework for making important agent runs inspectable, reviewable, and governable after the fact.

Use it when the question is not just "can the agent do the task?" but "can a human later inspect what happened well enough to trust it, reject it, debug it, or learn from it?"

## What This Solves

Raw traces are usually too thin for serious review. They can show that a system did something without showing:

- what the task actually was
- what evidence or state mattered
- how the result was checked
- whether approval was required and when it happened
- what failed or could fail

This framework turns that gap into a run-level review contract.

## The Six Questions

Every meaningful run should make these questions answerable:

1. What was the task?
2. What happened?
3. What did it rely on?
4. How was it checked?
5. Who approved impact, or why was approval not required?
6. What failed or could fail?

The point is not six markdown files. The point is reconstructability.

## The Three Layers

- runtime outputs: actions, observations, tool calls, intermediate state
- system records: task spec, execution trace, evidence record, verification report
- governance records: approval decision and failure review when the run crosses a meaningful control boundary

## Risk Tiers

Meaningful review begins with a bounded run. If the task or stop boundary splits, slice the run before you apply the risk tiers below.

- low risk: lightweight reconstruction is enough if task, actions, and basic checking can be recovered without guesswork
- medium risk: make task, trace, evidence, and verification explicit
- high risk: add explicit approval and failure-review capability

The practical version of this rule lives in `USE_IT.md`.

## Default Reading Path

Read these in order:

1. `README.md`
2. `examples/proofs/real-run-index.md`
3. `examples/proofs/march-26-compact-public-package/README.md`
4. `USE_IT.md`
5. `evaluation/run-review-checklist.md`

That path is the package front door.

## Main Surfaces

- `USE_IT.md`: day-to-day operator guide
- `examples/`: what the framework looks like in practice
- `evaluation/`: how to judge runs, architectures, and the framework itself
- `templates/`: direct record templates plus a few supporting patterns
- `investigation/`: advanced findings and tuning notes for framework builders
- `validation-lab/`: advanced synthetic pressure-testing
- `archive/`: background history only

## Examples, Proof, Validation, Archive

- real proof lives under `examples/proofs/`
- synthetic teaching examples live under `examples/teaching/`
- synthetic framework stress tests live under `validation-lab/`
- historical packet-oriented lineage lives under `archive/`

Keep those separate mentally:

- `examples/proofs/` shows that the framework can help on real runs, with the current flagship set indexed in `examples/proofs/real-run-index.md`
- `examples/teaching/` shows what a clean reviewable run looks like
- `investigation/` interprets the proof and validation evidence and distills tuning guidance
- `validation-lab/` tests where the framework works, fails, and gets ambiguous
- `archive/` is background, not the default path

## Origin

This package grew out of a real gap in `autonomous-agent-blueprint`.

The blueprint package already required bounded control loops, verification, approval gates, and post-incident review. What it did not define clearly was the minimum review surface one meaningful run should expose or reconstruct for a human reviewer.

Reviewable Runs is that missing run-level contract.

## Current Maturity

The framework is strong as an operating idea and increasingly solid as a package.

- concept maturity: high enough to stand alone
- package maturity: high enough for public use
- empirical maturity: still limited

Today it has multiple real captured proofs, a clear operator model, and a synthetic validation harness. It is publishable as a practical framework. It is not yet a broad research-grade claim.

## Non-Goals

- this is not model interpretability
- this is not a generic logging manifesto
- this is not mandatory paperwork for trivial low-risk runs
- this is not a meta-system that should be heavier than the work itself

## Publishing Path

The package is already shaped for a practical public argument:

1. why traces are not enough
2. what a reviewable run must expose
3. what this looks like on real and synthetic cases

If you want the upstream architecture basis first, read `../autonomous-agent-blueprint/core/agentic-architectures-blueprint.md`, then `../autonomous-agent-blueprint/core/practical-chapter-blueprints/README.md`, then the closest use case under `../autonomous-agent-blueprint/implementation/use-cases/`.
