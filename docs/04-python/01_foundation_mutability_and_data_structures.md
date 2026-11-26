# Foundations: values, control flow, and collections

Python programs manipulate **objects**. A variable is a name bound to an object; it is not a box that permanently
contains a value. This model explains assignment, mutability, function arguments, and copying.

## Basic values and types

| Category   | Built-in types            | Typical use                  |
|------------|---------------------------|------------------------------|
| Numeric    | `int`, `float`, `complex` | Counts and calculations      |
| Boolean    | `bool`                    | Conditions                   |
| Text       | `str`                     | Unicode text                 |
| Sequence   | `list`, `tuple`, `range`  | Ordered values               |
| Mapping    | `dict`                    | Key-value associations       |
| Set        | `set`, `frozenset`        | Unique values and membership |
| Null value | `None`                    | Absence of a value           |

Inspect a value with `type(value)`. Prefer explicit conversion—such as `int(text)`—at system boundaries rather than
relying on implicit assumptions.

```python { .python-runner title="Basic values experiment" }
name = "Ada"
age = 36
active = True
message = f"{name} is {age} years old"
```

## Conditions and loops

Conditions use truth values. Empty collections, zero, `None`, and empty strings are false; most other objects are true.

```python
if not users:
    print("No users")
elif len(users) == 1:
    print("One user")
else:
    print(f"{len(users)} users")

for index, user in enumerate(users, start=1):
    print(index, user)
```

Use `while` when repetition depends on state rather than on an iterable. `break` exits a loop, `continue` skips to its
next iteration, and a loop's `else` block runs only when no `break` occurs.

## Choosing a collection

| Need                               | Use     | Important properties                    |
|------------------------------------|---------|-----------------------------------------|
| Ordered, changeable sequence       | `list`  | Duplicates allowed; fast append         |
| Fixed record or immutable sequence | `tuple` | Hashable when all elements are hashable |
| Key-value lookup                   | `dict`  | Insertion ordered; keys are unique      |
| Unique values or fast membership   | `set`   | Unordered; elements must be hashable    |

```python { .python-runner title="Collection selection experiment" }
items = ["apple", "banana", "apple"]
counts = {item: items.count(item) for item in set(items)}
unique_items = set(items)
```

For counting real data, prefer `collections.Counter` over repeatedly calling `list.count`, which rescans the list.

## Mutability and identity

`list`, `dict`, and `set` are mutable. Numbers, strings, tuples, and frozen sets are immutable. Assignment never copies
an object.

```python { .python-runner title="Mutability and identity experiment" }
original = [1, 2]
alias = original
alias.append(3)
assert original == [1, 2, 3]
assert alias is original
```

Use `==` for value equality. Use `is` for identity, most commonly `value is None`.

### Avoid shared mutable defaults

Default arguments are evaluated once when a function is defined.

```python { .python-runner title="Safe default argument experiment" }
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Copy deliberately

```python
from copy import deepcopy

shallow = original.copy()  # nested objects remain shared
independent = deepcopy(original)
```

A comprehension also creates independent nested rows:

```python { .python-runner title="Independent nested lists experiment" }
grid = [[0] * 3 for _ in range(3)]
```

## Core operations

```python { .python-runner title="Core collection operations experiment" }
numbers = [3, 1, 4]
numbers.append(2)
first, *middle, last = numbers
ordered = sorted(numbers)

profile = {"name": "Ada", "role": "engineer"}
role = profile.get("role", "unknown")
for key, value in profile.items():
    print(key, value)
```

Slicing uses `sequence[start:stop:step]`; `stop` is excluded. Negative indexes count from the end.

## Experiment: references and collections

Change the values, add a nested object, or replace the shallow copy with a different copying strategy.

```python { .python-runner title="References and collections experiment" }
original = {"languages": ["Python"], "active": True}
shallow = original.copy()
shallow["languages"].append("SQL")

print("original:", original)
print("shallow: ", shallow)
print("same dictionary:", original is shallow)
print("same nested list:", original["languages"] is shallow["languages"])
```

## Checkpoint

- Explain names, objects, equality, and identity.
- Choose between list, tuple, dictionary, and set.
- Predict whether an operation mutates an existing object.
- Avoid mutable default arguments and shared nested lists.
- Use control flow without unnecessary nesting.

**Next:** [Functions, scope, and modules](02_functions_scope_and_modules.md)
