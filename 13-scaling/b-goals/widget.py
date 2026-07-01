"""A tiny module with one missing piece, on purpose.

`discount_price` is not implemented yet, so the test in test_widget.py fails.
Set a goal of "all tests in this folder pass" and watch Claude converge.
"""


def price_with_tax(price: float, tax_rate: float) -> float:
    return round(price * (1 + tax_rate), 2)


def discount_price(price: float, percent_off: float) -> float:
    # TODO: return the price after applying percent_off (0-100), rounded to 2 dp.
    raise NotImplementedError
