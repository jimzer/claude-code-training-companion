"""Sample app for hooks demo."""


def greet(name: str) -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"


def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    result = a + b
    return result


def process_items(items: list[str]) -> dict:
    """Process a list of items and return stats."""
    return {
        "count": len(items),
        "first": items[0] if items else None,
        "last": items[-1] if items else None,
    }


if __name__ == "__main__":
    print(greet("World"))
    print(add_numbers(2, 3))
    print(process_items(["a", "b", "c"]))
