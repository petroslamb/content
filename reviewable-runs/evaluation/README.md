# Evaluation

This folder contains the package's review instruments.

Use it for three different judgments:

- run review: did this specific run leave behind a credible review surface
- architecture readiness: can this system support reviewable runs at all
- framework evaluation: is Reviewable Runs earning its cost in practice

## Files

- `run-review-checklist.md` is the direct six-question instrument for one run.
- `architecture-readiness-checklist.md` is broader and asks whether a system can support reviewable runs before or after deployment.
- `failure-mode-catalog.md` names recurring failure classes that should sharpen a failure review or architecture critique.

## Alignment Matrix

| Review question | Canonical record | Direct template | Review surface |
| --- | --- | --- | --- |
| What was the task? | task spec | `../templates/task-spec-template.md` | `run-review-checklist.md` |
| What happened? | execution trace | `../templates/execution-trace-template.md` | `run-review-checklist.md` |
| What did it rely on? | evidence record | `../templates/evidence-record-template.md` | `run-review-checklist.md` |
| How was it checked? | verification report | `../templates/verification-report-template.md` | `run-review-checklist.md` |
| Who approved impact? | approval decision | `../templates/approval-decision-template.md` | `run-review-checklist.md` |
| What failed or could fail? | failure review | `../templates/failure-review-template.md` | `run-review-checklist.md` |

Only `run-review-checklist.md` maps one-to-one to the six review questions.

## Framework Evaluation

Use Reviewable Runs against two evidence surfaces:

1. a real pilot such as `../examples/proofs/coding-real-run/`
2. the synthetic harness in `../validation-lab/`

The current framework-level test is:

- does the review packet reduce unanswered questions compared with raw artifacts
- does it make approval or rejection more defensible
- does it make failure analysis less dependent on scattered logs

The package's first recorded synthetic results live in `../validation-lab/RUN_RESULTS.md`.

If you want the evidence interpreted rather than just listed, use `../investigation/README.md`.

Read this folder after `../README.md` and `../USE_IT.md`.
