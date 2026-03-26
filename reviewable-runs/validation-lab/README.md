# Validation Lab

This folder contains explicitly synthetic validation artifacts for the reviewable-runs framework.

**Status:** `synthetic validation artifact`

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

1. `../reviewable-runs.md`
2. `VALIDATION_MATRIX.md`
3. `AGENT_CARDS.md`
4. one validate case
5. one invalidate case
6. one stress-test case

This is not a proof layer and not a teaching dossier layer. It is a synthetic harness for testing the framework itself.
