# Runtime Record: Task Spec

## Task

Fix the invoice serializer so a `0%` discount keeps the `"0%"` label while leaving the payable amount unchanged.

## Objective

- remove the regression without widening scope
- keep the patch minimal
- rerun the targeted regression and full suite
- stop before merge

## Inputs

- failing pytest run
- `src/billing/invoice.py`
- `tests/test_invoice.py`

## Constraints

- inspect before editing
- use the smallest sensible patch
- verify with executable feedback

## Stop Condition

The targeted regression passes, the full suite passes, and the patch is held for human merge review.
