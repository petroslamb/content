# Runtime Record: Evidence Record

## Evidence Table

| Evidence item | Source page | Captured value |
| --- | --- | --- |
| Booking total | booking confirmation | `EUR 428.40` |
| Trip dates | itinerary page | `2026-02-12` to `2026-02-15` |
| Receipt package | receipt upload page | `hotel_invoice.pdf`, `train_receipt.pdf` |
| Claim category | reimbursement draft form | `Business Travel - Domestic` |

## Current State Snapshot

- current page: reimbursement review step
- visible amount: `EUR 428.40`
- visible category after refresh: `Business Travel - Domestic`
- visible attachments: 2
- submit button present but not clicked

## Risk Notes

- the page refreshed after upload
- category reset is a known risk on this form
- page recommendations were treated as observations, not policy
