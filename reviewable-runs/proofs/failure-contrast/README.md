# Failure Contrast

This file shows why raw logs alone are often too weak for serious review.

## Scenario

A coding agent reports:

- failing test reproduced
- file edited
- tests passed

The raw artifacts include terminal output and a patch, but nothing else.

## What The Reviewer Still Lacks

Even with a visible trace, the reviewer still has to infer:

- what exact task boundary was in scope
- why the chosen file mattered
- what evidence justified the patch instead of some other hypothesis
- whether the verification scope was proportionate
- whether merge was allowed automatically or still gated
- what plausible near miss remains

## Example Of A Thin Raw Surface

```text
$ pytest -q
..F
...
$ edit src/billing/invoice.py
$ pytest -q
...
```

This is visible. It is not reviewable enough.

## What The Six Questions Expose

The six-question model makes the missing parts obvious:

- task spec is missing
- evidence record is missing
- verification report is only implicit
- approval boundary is missing
- failure review is missing

## Why This Matters

Without those missing parts, a reviewer may still approve the patch. But the approval is weaker because it depends on private inference rather than explicit run records.

That is the core claim of the framework: ordinary logs can show activity without making the run credibly reviewable.
