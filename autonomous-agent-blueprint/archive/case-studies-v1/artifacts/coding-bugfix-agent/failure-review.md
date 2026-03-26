# Failure Review: Coding Bugfix Agent

## Failure

The patch fixed the target serializer test but would have missed a neighboring invoice-export regression if the broader discount test subset had not been run.

## Why it is plausible

Coding agents often look correct when a single failing test turns green. The real risk is verification scope that is too narrow for the changed surface.

## Taxonomy mapping

- [`../../../../implementation/evaluation/failure-mode-catalog.md`](../../../../implementation/evaluation/failure-mode-catalog.md): `Irreversible action without enough evidence`
- [`../../../../implementation/evaluation/failure-mode-catalog.md`](../../../../implementation/evaluation/failure-mode-catalog.md): `Prompt churn without measurement`

## Checklist controls that should catch it

- [`../../../../implementation/evaluation/architecture-review-checklist.md`](../../../../implementation/evaluation/architecture-review-checklist.md): `Can failed actions be observed and recovered from?`
- [`../../../../implementation/evaluation/architecture-review-checklist.md`](../../../../implementation/evaluation/architecture-review-checklist.md): `Is verification stronger than a single first-pass answer?`
- [`../../../../implementation/evaluation/architecture-review-checklist.md`](../../../../implementation/evaluation/architecture-review-checklist.md): `Does the team have a stable evaluation set?`

## What would reduce the failure

- define a minimum regression suite for each patch category
- attach diff-risk labels that force broader checks on serializer changes
- keep merge approval contingent on both target and neighboring tests

## Decision

Keep the coding default architecture. Tighten verification coverage rather than making the control loop more complex.
