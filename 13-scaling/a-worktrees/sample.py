"""A tiny module to edit in parallel worktrees.

Each worktree makes a different small change here, so two Claude sessions
can work at the same time without ever touching the same lines.
"""


def greet(name: str) -> str:
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    print(greet("world"))
    print(add(2, 3))
