# Runtime Record: Task Spec

## Task

Investigate a failing regression involving invoice serialization when `discount_percent = 0`.

## Objective

- reproduce the failure
- inspect the relevant serializer and pricing logic
- apply the smallest safe patch
- rerun targeted and nearby regression tests
- stop before merge

## Constraints

- inspection before editing
- repository scope only
- no destructive git operations
- no dependency upgrades
- merge requires approval

## Stop Condition

Produce a reviewable diff, a verification report, and a merge-ready approval packet without auto-merging.
