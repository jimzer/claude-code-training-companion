"""Small pricing module used to demonstrate the safety net.

Everything here passes `make check` (format, lint, types, tests). The point of
this station is the *gate*, not the code: ask Claude to extend this module and
watch the Stop hook refuse to finish until format + lint + types + tests are all
green again.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LineItem:
    name: str
    unit_price_cents: int
    quantity: int


def subtotal_cents(items: list[LineItem]) -> int:
    """Sum of every line (unit price * quantity), in cents."""
    return sum(item.unit_price_cents * item.quantity for item in items)


def apply_discount(amount_cents: int, percent: float) -> int:
    """Apply a percentage discount, rounding to the nearest cent.

    `percent` is a value in the range [0, 100].
    """
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(amount_cents * (1 - percent / 100))
