# Framework Evaluation

This doc explains how to judge whether reviewable runs are worth using.

The question is not whether the package reads well. The question is whether reviewable runs improve inspection, approval, debugging, and failure analysis compared with raw logs alone.

## Core Evaluation Question

Does the reviewable-runs surface help a reviewer answer the six questions faster and with less guesswork than raw traces, raw logs, or a plain transcript?

## Primary Metrics

- time to reconstruct a run
- time to approve or reject a run
- time to diagnose a failure or near miss
- number of unanswered review questions after inspection
- reviewer confidence after inspection
- difference between raw-log review quality and review-packet review quality

## Minimum Pilot Method

Use one meaningful run and compare two review modes:

1. raw artifacts only
2. reconstructed review packet

For each mode, record:

- time spent
- which review questions remain weak or unanswered
- confidence score from 1 to 5
- approve, reject, or escalate decision

## Synthetic Evaluation Harness

Use `validation-lab/VALIDATION_MATRIX.md` as the controlled synthetic harness.

That matrix is not proof. Its job is different:

- validate that the framework can recognize clean cases
- invalidate runs that only look reviewable on the surface
- expose edge conditions where reviewability becomes partial or contested

The lab should be used to pressure the framework before or alongside real pilots, not instead of them.

## Suggested Review Worksheet

For each reviewer:

| Mode | Time to first coherent summary | Unanswered questions | Confidence 1-5 | Decision |
| --- | --- | --- | --- | --- |
| Raw artifacts | <time> | <count> | <score> | approve \| reject \| escalate |
| Review packet | <time> | <count> | <score> | approve \| reject \| escalate |

## Success Signals

The framework is earning its cost when:

- the review packet reduces unanswered questions
- the review packet shortens time to coherent review
- reviewers identify verification gaps faster
- approval or rejection decisions become more defensible
- postmortem analysis is less dependent on scattered logs

## Failure Signals

The framework is not earning its cost when:

- the packet merely repeats raw logs
- reviewers still cannot identify evidence or verification clearly
- approval context remains vague
- dossier creation costs more than the review value it adds
- teams cannot tell when to use the framework

## First Pilot Target

Use `proofs/coding-real-run/` as the first pilot.

This is the right first target because:

- the task is bounded
- the evidence surface is concrete
- verification is cheap
- the approval gate is clear

## Combined Evaluation Path

Use both surfaces together:

1. `proofs/coding-real-run/` for real-world value comparison against raw artifacts
2. `validation-lab/VALIDATION_MATRIX.md` for synthetic coverage across good, bad, and edge cases

That combination is the current evaluation harness for this package.

## Evaluation Standard

Treat the first results as pilot evidence, not benchmark proof.

This framework becomes stronger when it can show:

- one real run that is easier to review with the packet than without it
- one negative contrast where raw logs leave important questions unanswered

That is enough for a practical framework claim. It is not yet enough for a broad scientific claim.
