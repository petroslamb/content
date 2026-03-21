# Runtime Record: Execution Trace

## Control Loop

1. Observe the current portal state and confirm the dashboard path.
2. Gather amount, dates, and receipt references from booking pages.
3. Enter the draft reimbursement claim through DOM-aware form actions.
4. Re-check the category, amount, and attachments after the upload-triggered refresh.
5. Hold at the review step for approval instead of clicking `Submit`.

## Notable Events

- the portal auto-refreshed after receipt upload
- a tooltip suggested `Miscellaneous Expense`, but that was treated as untrusted page guidance
- no irreversible submission action was taken
