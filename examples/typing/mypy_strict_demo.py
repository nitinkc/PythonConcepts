"""Hands-on strict-typing practice file.

Run it:    python -m examples.typing.mypy_strict_demo
Check it:  mypy --strict examples/typing/mypy_strict_demo.py

The file is strict-clean as written. The drills at the bottom are
commented-out mistakes: uncomment one at a time, re-run mypy, read the
error code, then fix the annotation or the code (not the message).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol


class Closable(Protocol):
    """Structural interface: any class with close() satisfies this."""

    def close(self) -> None: ...


def shutdown(resource: Closable) -> None:
    resource.close()


def total_length(parts: Iterable[str]) -> int:
    return sum(len(part) for part in parts)


def describe(value: object) -> str:
    if isinstance(value, str):
        return f"text of {len(value)} chars"
    if isinstance(value, int):
        return f"number {value}"
    return f"{type(value).__name__} instance"


def parse_port(raw: str | None) -> int:
    if raw is None:
        return 0
    return int(raw)  # raw is narrowed to str by the check above


def drills() -> None:
    """Uncomment one block at a time, then run `mypy --strict` on this file."""
    # 1. total_length(["a", "bb", 3])
    #    error: List item 2 has incompatible type "int"; expected "str"  [list-item]

    # 2. def untyped(x):
    #        return x
    #    error: Function is missing a type annotation  [no-untyped-def]
    #    Fix: def untyped(x: int) -> int: ...

    # 3. def g() -> int:
    #        return "nope"
    #    error: Incompatible return value type (got "str", expected "int")  [return-value]

    # 4. port: int = parse_port("8080")
    #    port += parse_port(None) + 0.5
    #    error: Incompatible types in assignment (expression has type "float",
    #           variable has type "int")  [assignment]


if __name__ == "__main__":
    print(total_length(["alpha", "beta"]))
    print(describe("hello"))
    print(describe(7))
    print(describe(3.14))
    print(parse_port("8080"), parse_port(None))
