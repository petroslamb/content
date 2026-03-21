# State Or Evidence Record: Coding Bugfix Agent

## Relevant files

| File | Why it matters |
| --- | --- |
| `billing/invoice_serializer.py` | emits the serialized discount block |
| `billing/pricing.py` | computes invoice discount metadata upstream |
| `tests/test_invoice_serializer.py` | contains the failing regression and nearby scenarios |

## Observed evidence

- failing test confirms `discount_percent: 0` still emits a visible discount block
- serializer currently checks `discount_percent is not None` instead of checking for a meaningful non-zero value
- nearby tests already distinguish between `None` and positive discount values

## Working state snapshot

- hypothesis status: confirmed by file inspection
- patch scope: serializer guard only
- memory write decision: store the final fix pattern as procedural memory only if the regression remains representative across future issues
