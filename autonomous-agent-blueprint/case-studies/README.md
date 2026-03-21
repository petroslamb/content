# Reviewable Run Dossiers

This folder is the repo's primary applied layer. The abstract architectures live in `../use-cases/`. The dossiers here show what those defaults look like when one concrete run is made reviewable from end to end.

Read the dossier first. Treat the supporting records as evidence, not as the main story.

## How To Use This Folder

Read in this order:

1. the matching abstract use case in `../use-cases/`
2. `../reviewable-runs.md`
3. the matching dossier in this folder
4. the supporting `runtime-records/` only if you want to inspect how the run is grounded
5. the supporting `governance-records/` only if you want to inspect approval or failure handling
6. `../evaluation/architecture-review-checklist.md`
7. `../evaluation/failure-mode-catalog.md`

## Runtime Records vs Governance Records

- Runtime records answer the first four review questions: what was the task, what happened, what did the system rely on, and how was the result checked.
- Governance records answer the last two review questions: who approved impact and what failed or could fail.
- In real systems, governance records are conditional. In this teaching layer, every dossier includes them so the review surface is explicit.

## Canonical Dossiers

- [`enterprise-policy-memo/README.md`](enterprise-policy-memo/README.md)
  Enterprise knowledge agent that drafts a policy memo and stops at a publication approval gate.
- [`coding-bugfix-agent/README.md`](coding-bugfix-agent/README.md)
  Repository-scoped coding agent that inspects, patches, tests, and holds for merge approval.
- [`web-form-agent/README.md`](web-form-agent/README.md)
  Browser agent that gathers evidence, prepares a high-friction form, and stops before submission.

## Shared Shape

Each dossier is the default read and uses the same structure:

1. Scenario and operating constraints
2. Why this default architecture was selected
3. Runtime loop in plain language
4. What the system must surface for this run
5. Review and governance boundaries
6. Failure or near-miss analysis
7. What to copy from this example
8. What not to generalize from this example

Each case then exposes:

- `runtime-records/task-spec.md`
- `runtime-records/execution-trace.md`
- `runtime-records/evidence-record.md`
- `runtime-records/verification-report.md`
- `governance-records/approval-decision.md`
- `governance-records/failure-review.md`

## Historical Reference

The original packet-oriented worked-example layer is preserved under [`../archive/case-studies-v1/README.md`](../archive/case-studies-v1/README.md). It is archival only and is no longer part of the default reading path.
