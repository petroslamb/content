# Raw Artifact: Terminal Transcript

```text
$ pytest -q
..F                                                                      [100%]
=================================== FAILURES ===================================
____________ test_serialize_invoice_with_zero_discount_keeps_label _____________

    def test_serialize_invoice_with_zero_discount_keeps_label():
        invoice = serialize_invoice(10000, 0)

>       assert invoice == {
            "amount_cents": 10000,
            "discount_percent": 0,
            "discount_label": "0%",
            "payable_cents": 10000,
        }
E       AssertionError: assert {'amount_cent...cents': 10000} == {'amount_cent...cents': 10000}
E
E         Omitting 3 identical items, use -vv to show
E         Differing items:
E         {'discount_label': None} != {'discount_label': '0%'}
E         Use -v to get more diff

tests/test_invoice.py:29: AssertionError
=========================== short test summary info ============================
FAILED tests/test_invoice.py::test_serialize_invoice_with_zero_discount_keeps_label
1 failed, 2 passed in 0.03s

$ nl -ba src/billing/invoice.py
     1  def serialize_invoice(amount_cents: int, discount_percent: int | None) -> dict:
     2      if discount_percent:
     3          discount_cents = round(amount_cents * (discount_percent / 100))
     4          payable_cents = amount_cents - discount_cents
     5          discount_label = f"{discount_percent}%"
     6      else:
     7          payable_cents = amount_cents
     8          discount_label = None
     9
    10      return {
    11          "amount_cents": amount_cents,
    12          "discount_percent": discount_percent,
    13          "discount_label": discount_label,
    14          "payable_cents": payable_cents,
    15      }

$ nl -ba tests/test_invoice.py
     1  from billing import serialize_invoice
     2
     3
     4  def test_serialize_invoice_without_discount():
     5      invoice = serialize_invoice(10000, None)
     6
     7      assert invoice == {
     8          "amount_cents": 10000,
     9          "discount_percent": None,
    10          "discount_label": None,
    11          "payable_cents": 10000,
    12      }
    13
    14
    15  def test_serialize_invoice_with_discount():
    16      invoice = serialize_invoice(10000, 15)
    17
    18      assert invoice == {
    19          "amount_cents": 10000,
    20          "discount_percent": 15,
    21          "discount_label": "15%",
    22          "payable_cents": 8500,
    23      }
    24
    25
    26  def test_serialize_invoice_with_zero_discount_keeps_label():
    27      invoice = serialize_invoice(10000, 0)
    28
    29      assert invoice == {
    30          "amount_cents": 10000,
    31          "discount_percent": 0,
    32          "discount_label": "0%",
    33          "payable_cents": 10000,
    34      }

$ pytest -q tests/test_invoice.py::test_serialize_invoice_with_zero_discount_keeps_label
.                                                                        [100%]
1 passed in 0.00s

$ pytest -q
...                                                                      [100%]
3 passed in 0.01s
```
