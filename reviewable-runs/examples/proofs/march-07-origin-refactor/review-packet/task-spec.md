# Runtime Record: Task Spec

## Task

Refactor the upstream blueprint package so it teaches reviewable runs through dossier-first case studies instead of packet-style artifact bundles.

## Objective

- introduce `reviewable-runs.md` as the conceptual source of truth
- rebuild the worked examples into dossier folders with runtime and governance records
- preserve the older packet-oriented examples as archive
- reroute the main repo surfaces without breaking historical links

## Inputs

- the user implementation prompt
- the existing `case-studies/`, `evaluation/`, and `use-cases/` docs
- archive material that still needed to remain readable after the move

## Constraints

- preserve history rather than delete it
- keep the abstract use cases aligned with the new dossier model
- patch broken archive-relative links
- stop cleanly even if the run ends before commit

## Stop Condition

The active path teaches reviewable runs through dossiers, the archive remains usable, and the work is ready for human commit or further review.

