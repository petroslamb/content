# Raw Artifact: Task Brief

Fix a regression in the invoice serializer. Invoices with a `0%` discount should preserve the `"0%"` label while keeping `payable_cents` unchanged.

Constraints:

- inspect before editing
- keep the patch minimal
- rerun the targeted regression and then the full test suite
- stop before merge
