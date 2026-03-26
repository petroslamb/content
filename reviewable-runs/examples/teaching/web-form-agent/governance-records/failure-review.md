# Governance Record: Failure Review

## Failure

The reimbursement form auto-refreshed after attachment upload and silently reset the claim category, leaving the page apparently complete but prepared for the wrong reimbursement type.

## Why It Is Plausible

This is a standard web-agent miss: the environment changes under the agent, and visual completeness does not guarantee semantic correctness.

## Taxonomy Mapping

- [`../../../../evaluation/failure-mode-catalog.md`](../../../../evaluation/failure-mode-catalog.md): `Observation-action confusion`
- [`../../../../evaluation/failure-mode-catalog.md`](../../../../evaluation/failure-mode-catalog.md): `Indirect prompt injection`

## Checklist Controls

- [`../../../../evaluation/architecture-readiness-checklist.md`](../../../../evaluation/architecture-readiness-checklist.md): `Can the system reconstruct what happened across the control loop?`
- [`../../../../evaluation/architecture-readiness-checklist.md`](../../../../evaluation/architecture-readiness-checklist.md): `Can the system show what evidence, provenance, or state supported the run?`
- [`../../../../evaluation/architecture-readiness-checklist.md`](../../../../evaluation/architecture-readiness-checklist.md): `Are irreversible actions guarded by deterministic checks and human approval?`

## What Would Reduce The Failure

- require a final DOM-state diff before opening the approval gate
- make category confirmation a separate verification item after every refresh
- keep the approval packet focused on the exact visible submission state

## Decision

Keep the web default architecture. Strengthen final page-state verification rather than switching to a less observable control mode.
