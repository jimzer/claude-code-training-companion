import pytest

from app import LineItem, apply_discount, subtotal_cents


def test_subtotal_sums_lines() -> None:
    items = [LineItem("a", 500, 2), LineItem("b", 300, 1)]
    assert subtotal_cents(items) == 1300


def test_subtotal_empty_is_zero() -> None:
    assert subtotal_cents([]) == 0


def test_apply_discount_rounds() -> None:
    assert apply_discount(1000, 12.5) == 875


def test_apply_discount_rejects_out_of_range() -> None:
    with pytest.raises(ValueError):
        apply_discount(1000, 150)
