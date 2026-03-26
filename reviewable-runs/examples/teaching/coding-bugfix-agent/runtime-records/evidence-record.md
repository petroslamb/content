# Runtime Record: Evidence Record

## Relevant Files

| File | Why it matters |
| --- | --- |
| `billing/invoice_serializer.py` | emits the serialized discount block |
| `billing/pricing.py` | computes invoice discount metadata upstream |
| `tests/test_invoice_serializer.py` | contains the failing regression and nearby scenarios |

## Observed Evidence

- the failing test confirmed that `discount_percent: 0` still emitted a visible discount block
- the serializer guard checked `discount_percent is not None`
- nearby tests already distinguished between `None` and positive discount values

## Working State

- hypothesis status: confirmed by file inspection
- patch scope: serializer guard only
- durable write policy: store the fix pattern only if it remains useful across similar issues
