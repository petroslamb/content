# Evaluation

This folder contains review instruments, not run records.

Use these files to judge a proposed architecture before implementation, during design review, or after an incident. They are meant to expose missing boundaries, weak verification, and vague autonomy claims.

- `run-review-checklist.md` is the direct six-question run review surface.
- `architecture-readiness-checklist.md` asks whether a proposed system can support that run review surface in the first place.
- `failure-mode-catalog.md` names recurring failure classes and the design responses that usually matter.
- `../FRAMEWORK_EVALUATION.md` explains how to evaluate whether the framework itself is worth using.

Only `run-review-checklist.md` maps one-to-one to the six review questions.

The other files answer adjacent but necessary questions:

- can the architecture support credible review at all
- what recurring failure classes should shape the failure review

## Alignment Matrix

| Review question | Canonical record | Direct template | Review surface |
| --- | --- | --- | --- |
| What was the task? | task spec | `../templates/task-spec-template.md` | `run-review-checklist.md` |
| What happened? | execution trace | `../templates/execution-trace-template.md` | `run-review-checklist.md` |
| What did it rely on? | evidence record | `../templates/evidence-record-template.md` | `run-review-checklist.md` |
| How was it checked? | verification report | `../templates/verification-report-template.md` | `run-review-checklist.md` |
| Who approved impact? | approval decision | `../templates/approval-decision-template.md` | `run-review-checklist.md` |
| What failed or could fail? | failure review | `../templates/failure-review-template.md` | `run-review-checklist.md` |

Read this folder after `../reviewable-runs.md` and before or alongside `../dossiers/`.
