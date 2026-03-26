# Raw Trace

```text
$ pytest -q
F..
$ rg "discount|serialize" src tests
$ sed -n '1,160p' src/billing/invoice.py
$ sed -n '1,200p' tests/test_invoice.py
$ apply patch
$ pytest -q tests/test_invoice.py::test_invoice_discount
.
$ pytest -q
...
```
