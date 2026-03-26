# Runtime Record: Evidence Record

## Evidence Table

| Evidence item | Source | Freshness or state | Why it mattered |
| --- | --- | --- | --- |
| failing regression output | `../raw-artifacts/failing-test-output.txt` | captured at run start | proved the bug and showed the mismatch was the missing `"0%"` label |
| serializer conditional | `src/billing/invoice.py` | live repo state during inspection | showed `discount_percent` was being treated by truthiness rather than by explicit `None` handling |
| failing test expectation | `tests/test_invoice.py` | live repo state during inspection | clarified the intended behavior for `0%` discount handling |
| one-line patch | `../raw-artifacts/raw-diff.patch` | run artifact after edit | showed the patch scope stayed minimal |

## Working State

- The bug was local to the serializer conditional rather than the test or rounding logic.
- The run did not inspect unrelated files because the failing test and serializer already formed a tight hypothesis.

## Risk Notes

- A passing target test alone would have been too weak.
- The main residual risk was insufficient nearby regression coverage, which is why the full suite rerun mattered.
