# Functions, scope, and modules

Functions turn behavior into reusable units. Good functions have a clear contract, focused responsibility, predictable return value, and explicit dependencies.

## Defining a function

```python { .python-runner title="Function signature experiment" }
def calculate_total(price: float, quantity: int = 1, *, tax: float = 0.0) -> float:
    """Return the total price including tax."""
    subtotal = price * quantity
    return subtotal * (1 + tax)

calculate_total(10, 2, tax=0.08)
```

Parameters before `/` are positional-only; parameters after `*` are keyword-only. Defaults belong after required parameters.

```python { .python-runner title="Parameter kinds experiment" }
def connect(host, /, port=5432, *, timeout=5):
    ...
```

Use `*args` for extra positional arguments and `**kwargs` for extra keyword arguments when the API genuinely needs flexibility—not as a substitute for a clear signature.

## Return values

A function without `return` returns `None`. Returning several comma-separated values creates a tuple.

```python { .python-runner title="Multiple return values experiment" }
def bounds(values):
    return min(values), max(values)

lowest, highest = bounds([4, 1, 9])
```

Avoid mixing incompatible return shapes such as a dictionary on success and `False` on failure. Raise an exception or consistently return an optional value.

## Scope and closures

Python resolves names using **LEGB**: Local, Enclosing, Global, Built-in.

```python { .python-runner title="Closure experiment" }
def make_multiplier(factor):
    def multiply(value):
        return value * factor
    return multiply

double = make_multiplier(2)
```

Use `nonlocal` to rebind an enclosing function's name and `global` to rebind a module-level name. Both should be rare; passing values and returning results is usually clearer.

## First-class functions

Functions can be stored, passed, and returned like other objects.

```python { .python-runner title="First-class functions experiment" }
def apply(values, operation):
    return [operation(value) for value in values]

squares = apply([1, 2, 3], lambda value: value**2)
```

Prefer `operator`, named functions, or comprehensions when they communicate intent better than a complex `lambda`.

## Modules and packages

A module is a `.py` file. A package is an importable directory, commonly containing `__init__.py`.

```python
from pathlib import Path
from statistics import mean
```

Imports execute a module once per interpreter process and cache it in `sys.modules`. Keep import-time behavior lightweight.

### The main guard

```python { .python-runner title="Main guard experiment" }
def main() -> None:
    print("Run application")

if __name__ == "__main__":
    main()
```

The guard prevents command-line behavior from running when another module imports the file.

### Import guidance

- Prefer absolute imports across package boundaries.
- Avoid wildcard imports; they hide where names originate.
- Do not modify `sys.path` in application code to repair package structure.
- Put reusable behavior in modules and invocation logic in a small entry point.
- Break circular imports by moving shared contracts to a lower-level module.

## Documentation and contracts

Type hints document expected values and enable static analysis, but Python does not enforce them at runtime.

```python { .python-runner title="Typed function contract experiment" }
from collections.abc import Iterable

def average(values: Iterable[float]) -> float:
    data = list(values)
    if not data:
        raise ValueError("values must not be empty")
    return sum(data) / len(data)
```

## Experiment: signatures and closures

Change `factor`, add another keyword-only option, or remove the default argument from the lambda to observe late binding.

```python { .python-runner title="Functions and closures experiment" }
def make_transform(factor, *, offset=0):
    def transform(value):
        return value * factor + offset
    return transform

triple_plus_one = make_transform(3, offset=1)
print([triple_plus_one(value) for value in range(5)])

functions = [lambda value=value: value ** 2 for value in range(4)]
print([function() for function in functions])
```

## Checkpoint

- Design required, default, positional-only, and keyword-only parameters.
- Explain LEGB and closures.
- Treat functions as first-class objects without overusing lambdas.
- Structure reusable modules and safe entry points.
- Write signatures that communicate a stable contract.

**Next:** [Object-oriented Python](03_object_oriented_python.md)
