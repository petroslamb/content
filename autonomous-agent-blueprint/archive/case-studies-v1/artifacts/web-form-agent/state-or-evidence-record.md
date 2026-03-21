# State Or Evidence Record: Web Form Agent

## Evidence table

| Evidence item | Source page | Captured value |
| --- | --- | --- |
| Booking total | booking confirmation | `EUR 428.40` |
| Trip dates | itinerary page | `2026-02-12` to `2026-02-15` |
| Receipt package | receipt upload page | `hotel_invoice.pdf`, `train_receipt.pdf` |
| Claim category | reimbursement draft form | `Business Travel - Domestic` |

## Current page-state summary

- current page: reimbursement review step
- claim amount visible: `EUR 428.40`
- category visible after refresh: `Business Travel - Domestic`
- attachments visible: 2
- submit button present but not clicked

## Risk notes

- the page refreshed after upload
- a tooltip recommended `Miscellaneous Expense`, but that text was treated as untrusted guidance rather than control policy
