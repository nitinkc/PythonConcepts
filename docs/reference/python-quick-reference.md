# Python quick reference

Use this page for recall. Follow links in the navigation when you need the underlying mental model.

## Syntax

```python
value = condition_a if condition else value_b
first, *middle, last = values
mapping = {**defaults, **overrides}
unique = {*left, *right}


def function(required, default=0, /, *, keyword_only=False):
    ...
```

## Built-in data types

| Category        | Type         | Example                      | Mutable? | Key property                                          |
|-----------------|--------------|------------------------------|---------:|-------------------------------------------------------|
| Boolean         | `bool`       | `True`, `False`              |       No | Subclass of `int`; used by conditions                 |
| Integer         | `int`        | `42`, `0b1010`, `0xFF`       |       No | Arbitrary precision                                   |
| Floating point  | `float`      | `3.14`, `1e-3`               |       No | Binary floating-point approximation                   |
| Complex number  | `complex`    | `2 + 3j`                     |       No | Real and imaginary components                         |
| Text sequence   | `str`        | `"Python"`                   |       No | Unicode text                                          |
| List            | `list`       | `[1, 2, 3]`                  |      Yes | Ordered sequence with duplicates                      |
| Tuple           | `tuple`      | `(1, 2, 3)`                  |       No | Fixed sequence; hashable if its elements are hashable |
| Range           | `range`      | `range(0, 10, 2)`            |       No | Lazy arithmetic sequence                              |
| Mapping         | `dict`       | `{"name": "Ada", "age": 36}` |      Yes | Insertion-ordered key-value lookup                    |
| Set             | `set`        | `{1, 2, 3}`                  |      Yes | Unique hashable elements                              |
| Frozen set      | `frozenset`  | `frozenset({1, 2})`          |       No | Immutable, hashable set                               |
| Binary sequence | `bytes`      | `b"Python"`                  |       No | Immutable bytes                                       |
| Binary sequence | `bytearray`  | `bytearray(b"Python")`       |      Yes | Mutable bytes                                         |
| Binary view     | `memoryview` | `memoryview(data)`           |  Depends | Accesses binary data without copying                  |
| Null value      | `NoneType`   | `None`                       |       No | Represents the absence of a value                     |

### Construction and conversion

```python
integer = int("42")
decimal = float("3.14")
text = str(42)
characters = list("abc")  # ["a", "b", "c"]
coordinates = tuple([10, 20])  # (10, 20)
profile = dict(name="Ada", age=36)
unique = set([1, 1, 2])  # {1, 2}
immutable_unique = frozenset(unique)
raw = bytes([65, 66, 67])  # b"ABC"
editable_raw = bytearray(raw)
```

### Literal traps

```python
empty_list = []
empty_tuple = ()
single_item_tuple = ("python",)  # comma creates the tuple
empty_dict = {}
empty_set = set()  # {} is an empty dictionary
set_literal = {"python", "fastapi"}
```

### Mutability, hashability, and identity

- Mutable built-ins include `list`, `dict`, `set`, and `bytearray`.
- Immutable built-ins include numbers, `bool`, `str`, `tuple`, `range`, `frozenset`, `bytes`, and `None`.
- Dictionary keys and set elements must be hashable.
- Immutability does not guarantee hashability: a tuple containing a list is not hashable.
- Use `==` for value equality and `is` for identity, especially `value is None`.
- `type(value)` returns the exact runtime type; `isinstance(value, Type)` also recognizes subclasses.

## Collections

| Task                   | Expression                                    |
|------------------------|-----------------------------------------------|
| Last item              | `items[-1]`                                   |
| Reverse copy           | `items[::-1]`                                 |
| Transform              | `[f(item) for item in items]`                 |
| Filter                 | `[item for item in items if predicate(item)]` |
| Index and value        | `enumerate(items, start=1)`                   |
| Parallel iteration     | `zip(left, right, strict=True)`               |
| Safe dictionary lookup | `mapping.get(key, default)`                   |
| Key-value iteration    | `mapping.items()`                             |
| Unique values          | `set(items)`                                  |
| Frequency count        | `Counter(items)`                              |
| Double-ended queue     | `deque(items)`                                |
| Custom ordering        | `sorted(items, key=key_function)`             |

Typical average costs:

| Operation                |   List |   Dict |    Set |
|--------------------------|-------:|-------:|-------:|
| Index/key lookup         | `O(1)` | `O(1)` |      — |
| Membership               | `O(n)` | `O(1)` | `O(1)` |
| Append/add               | `O(1)` | `O(1)` | `O(1)` |
| Insert/delete near start | `O(n)` | `O(1)` | `O(1)` |

## Strings

```python
text.strip()
text.split(",")
",".join(parts)
text.startswith("prefix")
text.replace("old", "new")
f"{name}: {amount:,.2f}"
```

Strings are immutable. Build many fragments in a list and use `str.join`.

## Functions and classes

```python
def function(value: int | None = None) -> str:
    if value is None:
        return "missing"
    return str(value)


from dataclasses import dataclass, field


@dataclass(slots=True)
class Record:
    name: str
    tags: list[str] = field(default_factory=list)
```

## Exceptions and resources

```python
try:
    result = operation()
except SpecificError as error:
    raise DomainError("operation failed") from error
else:
    use(result)
finally:
    cleanup()

with open("data.txt", encoding="utf-8") as stream:
    text = stream.read()
```

Catch specific exceptions. Use `finally` or a context manager for cleanup.

## Iteration

```python
def generate(limit):
    for number in range(limit):
        yield number ** 2


total = sum(number ** 2 for number in range(1000))
```

An iterable creates an iterator; an iterator yields values until `StopIteration`; a generator is a convenient iterator
implementation.

## Typing

```python
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence

str | None
list[str]
tuple[int, ...]
dict[str, object]
Callable[[int], str]
Iterator[bytes]
```

## Testing

```python
import unittest


class ExampleTests(unittest.TestCase):
    def test_behavior(self):
        self.assertEqual(function(1), "1")

    def test_error(self):
        with self.assertRaises(ValueError):
            parse("invalid")
```

Run the repository's tests:

```bash
python3 -m unittest discover -s tests -v
```

## Complexity patterns

| Pattern        | Typical cost | Use                              |
|----------------|-------------:|----------------------------------|
| Hash map/set   |       `O(n)` | Fast lookup and deduplication    |
| Two pointers   |       `O(n)` | Ordered data or opposite ends    |
| Sliding window |       `O(n)` | Contiguous ranges                |
| Binary search  |   `O(log n)` | Sorted or monotonic search space |
| BFS/DFS        |   `O(V + E)` | Graph and tree traversal         |
| Sorting        | `O(n log n)` | Ordering enables a simpler scan  |

## Common traps

- `is` compares identity; `==` compares values.
- Mutable default arguments are shared across calls.
- `[[0] * width] * height` shares rows.
- `list.sort()` mutates and returns `None`; `sorted()` returns a new list.
- A generator is usually single-use.
- Bare `except` clauses hide failures.
- `async def` does not make blocking work non-blocking.
- Type hints are not runtime validation.
- Never store secrets directly in source code.
