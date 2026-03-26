# Validation Lab

This folder contains explicitly synthetic validation artifacts for the Reviewable Runs framework.

**Status:** `synthetic validation artifact`

This is an advanced surface.

- it is not the first thing to read
- it is not proof
- it is not the primary teaching surface
- it is the synthetic harness for pressure-testing the framework

Use this surface to test three things:

- where the framework works
- where the framework should reject weak runs
- where the framework reaches its limits under ambiguity, overload, or partial reconstruction

## Folder Roles

- `agents/`: reusable synthetic agent cards
- `validate/`: cases that should score well under the framework
- `invalidate/`: cases that should fail or look weak under the framework
- `stress-test/`: cases that pressure the framework limits without collapsing into random noise
- `VALIDATION_MATRIX.md`: one-row view of the whole first wave
- `RUN_RESULTS.md`: first-pass framework judgments against the whole first wave
- `AGENT_CARDS.md`: index of the reusable synthetic agents

## Required Case Shape

Every case in this lab uses the same structure:

- `README.md`
- `scenario.md`
- `agent-card.md`
- `raw-trace.md`
- `raw-artifacts/`
- `review-surface/`
- `expected-judgment.md`

The review-surface folder uses the six-record model, but invalidation and stress-test cases may contain intentionally weak or incomplete records.

## How To Use This Folder

Read in this order:

1. `../README.md`
2. `VALIDATION_MATRIX.md`
3. `RUN_RESULTS.md`
4. `AGENT_CARDS.md`
5. one validate case
6. one invalidate case
7. one stress-test case

This is not a proof layer and not a teaching dossier layer. It is a synthetic harness for testing the framework itself.

If you want these synthetic results interpreted alongside the real proofs, use `../investigation/README.md`.
