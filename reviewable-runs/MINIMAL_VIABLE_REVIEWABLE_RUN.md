# Minimal Viable Reviewable Run

This doc defines the minimum operational standard for adopting reviewable runs.

The goal is not to require a six-file packet for every low-value action. The goal is to make sure meaningful runs can be reviewed without guesswork.

## Core Default

Every meaningful run should make these questions answerable:

1. What was the task?
2. What happened?
3. What did it rely on?
4. How was it checked?
5. Who approved impact, or why was approval not required?
6. What failed or could fail?

The adoption question is not "did the system emit all six files?" The adoption question is "what is the lightest record surface that answers the right questions for the risk level?"

## Low Risk

Use lightweight reconstruction.

Minimum:

- reconstructable task boundary
- reconstructable action or event history
- basic verification or completion signal
- explicit reason approval was not required

Defaults:

- no persisted six-record packet required
- ordinary logs and runtime outputs are acceptable if a reviewer can recover task, actions, and basic checking without guesswork
- failure review is optional for clean low-risk runs

Typical examples:

- low-impact retrieval
- internal drafts with no external side effect
- non-destructive repo inspection

## Medium Risk

Use explicit runtime records.

Minimum:

- task spec
- execution trace
- evidence record
- verification report

Defaults:

- these runtime records should be explicit and easy to inspect
- approval may be unnecessary, but the reason should be visible
- failure review is recommended after near misses and required after incidents

Typical examples:

- bounded coding fixes held before merge
- governed internal artifacts
- draft browser actions before final submit

## High Risk

Use the full review surface.

Minimum:

- task spec
- execution trace
- evidence record
- verification report
- approval decision
- failure review capability

Defaults:

- governance records are required when actions are external, destructive, expensive to roll back, policy sensitive, or meaningfully irreversible
- approval should be explicit rather than inferred
- failure review is mandatory after incidents and strongly recommended after near misses

Typical examples:

- code merge or release approval
- financial, legal, or policy-sensitive outputs
- external submissions or account changes

## Mandatory Rules

- Low risk does not require a persisted six-record packet.
- Medium risk requires explicit runtime records.
- High risk requires governance records when side effects or rollback cost justify them.
- Failure review is mandatory after incidents, strongly recommended after near misses, and optional for clean low-risk runs.

## Adoption Standard

Use this as the operator rule:

- if the run matters, make the runtime surface explicit
- if the run can hurt something, make the governance surface explicit
- if the run fails, make the failure surface explicit

That is the minimum viable reviewable run.
