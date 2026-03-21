# Input Brief: Coding Bugfix Agent

## Task

Investigate a failing regression test involving invoice serialization when `discount_percent = 0`.

## Objective

- reproduce the failure
- inspect the relevant serialization and pricing code
- apply the smallest safe patch
- rerun targeted and nearby regression tests
- produce a reviewable diff and stop before merge

## Constraints

- inspection before editing
- repo scope only
- no dependency upgrades
- no destructive git operations
- approval required before merge

## Reported failure

`tests/test_invoice_serializer.py::test_zero_discount_serializes_without_discount_block`

Current error:

`AssertionError: expected no discount block, got {'discount_percent': 0, 'discount_label': '0%'}`
