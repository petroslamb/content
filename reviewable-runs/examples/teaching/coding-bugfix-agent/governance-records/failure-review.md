# Governance Record: Failure Review

## Failure

The patch fixed the target serializer test but would have missed a neighboring regression if the broader discount test subset had not been run.

## Why It Is Plausible

Coding agents often look correct as soon as the red test turns green. The real risk is verification scope that is too narrow for the changed surface.

## Taxonomy Mapping

- [`../../../../evaluation/failure-mode-catalog.md`](../../../../evaluation/failure-mode-catalog.md): `Irreversible action without enough evidence`
- [`../../../../evaluation/failure-mode-catalog.md`](../../../../evaluation/failure-mode-catalog.md): `Prompt churn without measurement`

## Checklist Controls

- [`../../../../evaluation/architecture-readiness-checklist.md`](../../../../evaluation/architecture-readiness-checklist.md): `Can the system show how the result or action was verified?`
- [`../../../../evaluation/architecture-readiness-checklist.md`](../../../../evaluation/architecture-readiness-checklist.md): `Can the system reconstruct what happened across the control loop?`
- [`../../../../evaluation/architecture-readiness-checklist.md`](../../../../evaluation/architecture-readiness-checklist.md): `Does the team have a stable evaluation set?`

## What Would Reduce The Failure

- define a minimum regression suite for each patch category
- attach diff-risk labels that force broader checks on serializer changes
- keep merge approval contingent on both target and neighboring tests

## Decision

Keep the coding default architecture. Tighten verification coverage rather than complicating the loop.
