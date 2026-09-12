# Errors, files, testing, and typing

Reliable Python code validates assumptions at boundaries, raises meaningful exceptions, cleans up resources, and has automated tests for observable behavior.

## Exceptions

Catch only exceptions you can handle. Keep the protected block narrow and preserve the original traceback when translating errors.

```python { .python-runner title="Input validation experiment" }
def parse_port(text: str) -> int:
    try:
        port = int(text)
    except ValueError as error:
        raise ValueError(f"invalid port: {text!r}") from error

    if not 1 <= port <= 65_535:
        raise ValueError("port must be between 1 and 65535")
    return port
```

The complete structure is `try`, one or more `except` blocks, optional `else`, and optional `finally`. `else` runs after a successful `try`; `finally` runs regardless of outcome.

Avoid `except Exception: pass`. It hides failures and makes debugging harder. Define a custom exception when callers need to distinguish a domain failure.

## File and path handling

Use `pathlib.Path` and specify text encoding.

```python
from pathlib import Path

config_path = Path("config") / "settings.txt"
text = config_path.read_text(encoding="utf-8")
config_path.write_text(text.upper(), encoding="utf-8")
```

For large files, iterate over an open stream rather than loading the entire file. Use a context manager for resources requiring cleanup.

## Unit testing

Tests should arrange state, perform one behavior, and assert the result. Test public behavior rather than implementation details.

```python
import unittest

class ParsePortTests(unittest.TestCase):
    def test_accepts_valid_port(self):
        self.assertEqual(parse_port("8080"), 8080)

    def test_rejects_non_numeric_port(self):
        with self.assertRaises(ValueError):
            parse_port("http")

if __name__ == "__main__":
    unittest.main()
```

Keep tests deterministic. Replace real clocks, networks, randomness, and external systems at the boundary. Prefer small fakes or targeted mocks over mocking every internal call.

## Debugging

1. Reproduce the failure with the smallest reliable input.
2. Read the complete traceback from the final exception backward.
3. Inspect assumptions at the failure boundary.
4. Add a regression test.
5. Fix the root cause and rerun the relevant suite.

Use `breakpoint()` for interactive inspection and `logging` for runtime diagnostics. Do not leave sensitive values in logs.

## Type hints

Type hints communicate contracts and enable tools to detect mistakes before execution.

```python { .python-runner title="Type contract experiment" }
from collections.abc import Iterable, Mapping
from typing import TypeAlias

UserId: TypeAlias = int

def active_names(users: Iterable[Mapping[str, object]]) -> list[str]:
    return [str(user["name"]) for user in users if user.get("active")]
```

Modern forms include `str | None`, `list[str]`, and `tuple[int, ...]`. Use `Protocol` for behavior-based interfaces and `TypedDict` for dictionaries with known keys. Avoid `Any` unless crossing an untyped boundary.

Type hints do not validate runtime input. Use explicit checks or a validation library at external boundaries.

## Code quality habits

- Format consistently and follow project lint rules.
- Keep functions focused and names descriptive.
- Avoid hidden global state.
- Inject I/O dependencies so logic remains testable.
- Document why behavior exists, not what obvious syntax does.

## Experiment: validation and exception chaining

Try valid, nonnumeric, and out-of-range values. Modify the domain exception to preserve more context.

```python { .python-runner title="Validation and exception chaining experiment" }
class ConfigurationError(Exception):
    pass


def parse_port(text):
    try:
        port = int(text)
    except ValueError as error:
        raise ConfigurationError(f"invalid port: {text!r}") from error
    if not 1 <= port <= 65_535:
        raise ConfigurationError("port must be between 1 and 65535")
    return port

for value in ["8080", "http", "70000"]:
    try:
        print(value, "->", parse_port(value))
    except ConfigurationError as error:
        print(value, "->", type(error).__name__, error)
        print("  cause:", repr(error.__cause__))
```

## Checkpoint

- Raise, catch, chain, and define exceptions intentionally.
- Handle files with explicit paths, encodings, and cleanup.
- Write deterministic behavior-focused tests.
- Debug from a reproducible failure and retain a regression test.
- Use type hints to make contracts clear.

**Next:** [Concurrency and performance](06_concurrency_and_performance.md)
