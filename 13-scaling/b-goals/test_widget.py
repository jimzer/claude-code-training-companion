"""Tests for widget.py. The discount_price test fails until it is implemented."""
from widget import price_with_tax, discount_price


def test_price_with_tax():
    assert price_with_tax(100.0, 0.2) == 120.0


def test_discount_price():
    # This fails today: discount_price raises NotImplementedError.
    assert discount_price(100.0, 25.0) == 75.0
    assert discount_price(50.0, 10.0) == 45.0
