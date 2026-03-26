# Raw Trace

```text
$ pytest -q
..F
$ inspect src/billing/invoice.py tests/test_invoice.py
$ apply one-line conditional fix
$ pytest -q tests/test_invoice.py::test_zero_discount
.
$ pytest -q
...
$ stop before merge
```
