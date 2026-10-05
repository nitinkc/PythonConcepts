<div class="python-cheatsheet" markdown>

<div class="cheatsheet-hero" markdown>

# Python Quick Reference

Essential Python syntax, standard-library patterns, production practices, and interview-ready examples.

</div>

<div class="cheatsheet-nav">
  <a href="#fundamentals">Fundamentals</a>
  <a href="#collections">Collections</a>
  <a href="#functions-and-objects">Functions & objects</a>
  <a href="#errors-and-resources">Errors</a>
  <a href="#standard-library">Standard library</a>
  <a href="#typing-and-testing">Typing & testing</a>
  <a href="#async-and-concurrency">Concurrency</a>
  <a href="#interview-patterns">Interview patterns</a>
</div>

## Fundamentals

Python is dynamically typed, indentation defines blocks, and nearly every value is an object.

<div class="grid cards" markdown>

-   **Variables and values**

    ```python
    name = "Ada"
    age: int = 36
    active = True
    missing = None

    x, y = 10, 20
    x, y = y, x
    first, *middle, last = range(5)
    ```

-   **Control flow**

    ```python
    label = "adult" if age >= 18 else "minor"

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    else:
        grade = "C"
    ```

-   **Loops**

    ```python
    for index, value in enumerate(values, start=1):
        print(index, value)

    for left, right in zip(xs, ys, strict=True):
        print(left, right)

    while queue:
        process(queue.pop())
    ```

-   **Pattern matching**

    ```python
    match response:
        case {"status": 200, "data": data}:
            handle(data)
        case {"status": status} if status >= 400:
            raise RequestError(status)
        case _:
            raise ValueError("unexpected response")
    ```

</div>

### Built-in types

<span class="level level-essential">Essential</span>

| Type | Example | Mutable | Best for |
|---|---|:---:|---|
| `bool` | `True`, `False` | No | Conditions and flags |
| `int` | `42`, `0xFF` | No | Exact integers |
| `float` | `3.14`, `1e-3` | No | Approximate real numbers |
| `str` | `"Python"` | No | Unicode text |
| `list` | `[1, 2, 3]` | Yes | Ordered, changing sequences |
| `tuple` | `(1, 2, 3)` | No | Fixed records and hashable sequences |
| `dict` | `{"name": "Ada"}` | Yes | Key-value lookup |
| `set` | `{1, 2, 3}` | Yes | Membership and uniqueness |
| `frozenset` | `frozenset({1, 2})` | No | Hashable sets |
| `bytes` | `b"ABC"` | No | Binary data |
| `NoneType` | `None` | No | Absence of a value |

```python
integer = int("42")
decimal = float("3.14")
characters = list("abc")
coordinates = tuple([10, 20])
profile = dict(name="Ada", age=36)
unique = set([1, 1, 2])
```

!!! tip "Production tip"
    Use `==` for value equality and `is` for identity. Write `value is None`, not `value == None`.

## Collections

### Lists, tuples, dictionaries, and sets

<span class="level level-essential">Essential</span>

```python
items = [3, 1, 2]
items.append(4)
last = items[-1]
copy = items[:]
reversed_copy = items[::-1]
ordered = sorted(items)

point = (10, 20)
x, y = point

user = {"name": "Ada", "role": "admin"}
role = user.get("role", "guest")
for key, value in user.items():
    print(key, value)

seen = {1, 2, 3}
common = seen & {2, 3, 4}
combined = seen | {4, 5}
```

### Comprehensions

<span class="level level-common">Common</span>

```python
squares = [number**2 for number in range(10)]
evens = [number for number in values if number % 2 == 0]
lookup = {item.id: item for item in items}
initials = {name[0] for name in names}
total = sum(number**2 for number in range(1000))
```

### Complexity at a glance

| Operation | List | Dict | Set |
|---|---:|---:|---:|
| Index/key lookup | `O(1)` | `O(1)` average | — |
| Membership | `O(n)` | `O(1)` average | `O(1)` average |
| Append/add | `O(1)` amortized | `O(1)` average | `O(1)` average |
| Insert/delete near start | `O(n)` | `O(1)` average | `O(1)` average |
| Sort | `O(n log n)` | — | — |

!!! tip "Production tip"
    Prefer a set for repeated membership checks and a dictionary for keyed lookup. Use a list when order and indexing matter.

## Strings

<span class="level level-common">Common</span>

```python
text = "  Python makes intent clear  "
clean = text.strip()
words = clean.split()
slug = "-".join(word.lower() for word in words)

text.startswith("Python")
text.endswith("clear")
text.replace("intent", "code")
"python" in text.lower()

name = "Ada"
amount = 1234.5
message = f"{name}: ${amount:,.2f}"
```

Strings are immutable. Accumulate many fragments and call `"".join(parts)` instead of repeatedly concatenating in a loop.

## Functions and objects

### Functions

<span class="level level-essential">Essential</span>

```python
def format_name(
    first: str,
    last: str = "",
    /,
    *,
    uppercase: bool = False,
) -> str:
    result = f"{first} {last}".strip()
    return result.upper() if uppercase else result


def collect(*values: int, **options: object) -> tuple[int, ...]:
    return values
```

- Parameters before `/` are positional-only.
- Parameters after `*` are keyword-only.
- `*args` gathers positional arguments; `**kwargs` gathers keyword arguments.
- Avoid mutable defaults; use `None` and create the value inside the function.

### Classes and data classes

<span class="level level-common">Common</span>

```python
from dataclasses import dataclass, field

@dataclass(slots=True)
class User:
    name: str
    roles: list[str] = field(default_factory=list)

    @property
    def is_admin(self) -> bool:
        return "admin" in self.roles

    def grant(self, role: str) -> None:
        if role not in self.roles:
            self.roles.append(role)
```

!!! tip "Production tip"
    Prefer a data class for data-oriented objects. Use regular classes when invariants, lifecycle, or substantial behavior dominate.

### Iterators and generators

<span class="level level-common">Common</span>

```python
def read_chunks(stream, size: int = 8192):
    while chunk := stream.read(size):
        yield chunk

squares = (number**2 for number in range(1_000_000))
first_ten = list(itertools.islice(squares, 10))
```

Generators are lazy and usually single-use. They are ideal for streams or data too large to hold in memory.

## Errors and resources

### Exceptions

<span class="level level-critical">Critical</span>

```python
class ConfigurationError(Exception):
    pass

try:
    config = load_config(path)
except FileNotFoundError as error:
    raise ConfigurationError(f"missing config: {path}") from error
except ValueError as error:
    logger.warning("invalid config: %s", error)
else:
    start(config)
finally:
    release_temporary_resources()
```

Catch the narrowest useful exception. Add context with `raise ... from error`; never silently swallow failures.

### Context managers

<span class="level level-essential">Essential</span>

```python
from contextlib import contextmanager

with open("data.txt", encoding="utf-8") as stream:
    text = stream.read()

@contextmanager
def transaction(connection):
    try:
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()
```

## Standard library

<div class="grid cards" markdown>

-   **`collections`**

    ```python
    from collections import Counter, defaultdict, deque

    counts = Counter(words)
    groups = defaultdict(list)
    queue = deque([start])
    queue.append(next_item)
    current = queue.popleft()
    ```

-   **`itertools`**

    ```python
    from itertools import chain, combinations, groupby

    all_items = chain(left, right)
    pairs = combinations(values, 2)
    for key, group in groupby(rows, key=key_fn):
        consume(key, list(group))
    ```

-   **`pathlib`**

    ```python
    from pathlib import Path

    root = Path(__file__).resolve().parent
    config = root / "config.json"
    text = config.read_text(encoding="utf-8")
    for path in root.glob("**/*.py"):
        print(path.name)
    ```

-   **`datetime`**

    ```python
    from datetime import UTC, datetime, timedelta

    now = datetime.now(UTC)
    tomorrow = now + timedelta(days=1)
    encoded = now.isoformat()
    decoded = datetime.fromisoformat(encoded)
    ```

-   **`json`**

    ```python
    import json

    encoded = json.dumps(payload, indent=2)
    decoded = json.loads(encoded)

    with path.open("w", encoding="utf-8") as stream:
        json.dump(payload, stream)
    ```

-   **`functools`**

    ```python
    from functools import cache, partial

    @cache
    def fibonacci(number: int) -> int:
        if number < 2:
            return number
        return fibonacci(number - 1) + fibonacci(number - 2)

    parse_decimal = partial(int, base=10)
    ```

</div>

## Typing and testing

### Type hints

<span class="level level-common">Common</span>

```python
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from typing import Protocol, TypeVar

T = TypeVar("T")

class SupportsClose(Protocol):
    def close(self) -> None: ...

def first(items: Sequence[T]) -> T:
    return items[0]

def transform(values: Iterable[int], fn: Callable[[int], str]) -> Iterator[str]:
    return (fn(value) for value in values)
```

Common forms: `str | None`, `list[str]`, `tuple[int, ...]`, `dict[str, object]`, and `Callable[[int], str]`.

### Testing with `unittest`

<span class="level level-critical">Critical</span>

```python
import unittest
from unittest.mock import patch

class ServiceTests(unittest.TestCase):
    def test_formats_valid_value(self):
        self.assertEqual(format_value(1), "1")

    def test_rejects_invalid_value(self):
        with self.assertRaises(ValueError):
            format_value(-1)

    @patch("package.service.fetch")
    def test_uses_fetched_value(self, fetch):
        fetch.return_value = 42
        self.assertEqual(load_value(), 42)
```

```bash
python3 -m unittest discover -s tests -v
```

Test observable behavior, keep tests deterministic, and patch where a dependency is used rather than where it was defined.

## Async and concurrency

### Async I/O

<span class="level level-advanced">Advanced</span>

```python
import asyncio

async def fetch_all(urls: list[str]) -> list[bytes]:
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(fetch(url)) for url in urls]
    return [task.result() for task in tasks]

result = asyncio.run(fetch_all(urls))
```

### Choosing a concurrency model

| Workload | Prefer | Why |
|---|---|---|
| Many network operations | `asyncio` | Cooperative I/O concurrency |
| Blocking I/O libraries | `ThreadPoolExecutor` | Threads overlap waiting |
| CPU-bound Python work | `ProcessPoolExecutor` | Processes bypass the GIL |
| Shared-state coordination | `threading.Lock` / `asyncio.Lock` | Protect critical sections |

!!! warning "Common trap"
    `async def` does not make blocking code non-blocking. Use async-compatible libraries or move blocking calls to a thread.

## Interview patterns

### Pattern guide

| Signal | Pattern | Typical cost |
|---|---|---:|
| Fast lookup, counting, deduplication | Hash map or set | `O(n)` |
| Sorted input, pair from opposite ends | Two pointers | `O(n)` |
| Contiguous subarray or substring | Sliding window | `O(n)` |
| Sorted or monotonic search space | Binary search | `O(log n)` |
| Levels or shortest unweighted path | Breadth-first search | `O(V + E)` |
| Explore paths or connected components | Depth-first search | `O(V + E)` |
| Repeated optimal subproblems | Dynamic programming | Varies |
| Next largest/smallest boundary | Monotonic stack | `O(n)` |

### Reusable templates

=== "Two pointers"

    ```python
    def has_pair(values: list[int], target: int) -> bool:
        left, right = 0, len(values) - 1
        while left < right:
            total = values[left] + values[right]
            if total == target:
                return True
            if total < target:
                left += 1
            else:
                right -= 1
        return False
    ```

=== "Sliding window"

    ```python
    def max_window(values: list[int], size: int) -> int:
        current = sum(values[:size])
        best = current
        for right in range(size, len(values)):
            current += values[right] - values[right - size]
            best = max(best, current)
        return best
    ```

=== "Binary search"

    ```python
    def lower_bound(values: list[int], target: int) -> int:
        left, right = 0, len(values)
        while left < right:
            middle = (left + right) // 2
            if values[middle] < target:
                left = middle + 1
            else:
                right = middle
        return left
    ```

=== "Breadth-first search"

    ```python
    from collections import deque

    def shortest_distance(graph, start, target):
        queue = deque([(start, 0)])
        seen = {start}
        while queue:
            node, distance = queue.popleft()
            if node == target:
                return distance
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append((neighbor, distance + 1))
        return -1
    ```

## Common traps

- Mutable default arguments are shared across calls.
- `[[0] * width] * height` creates references to the same row.
- `list.sort()` mutates and returns `None`; `sorted()` returns a new list.
- Modifying a collection while iterating over it is error-prone.
- Floating-point values are approximations; use `decimal.Decimal` for exact decimal arithmetic.
- A generator is usually single-use.
- Bare `except` clauses hide failures.
- Type hints are not runtime validation.
- Never store secrets directly in source code.

</div>
