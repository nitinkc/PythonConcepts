# Object-oriented Python

Classes combine state and behavior. Use them when an object has invariants, related operations, or a meaningful
lifecycle. A plain function, dictionary, or data class is often better for simpler data transformations.

## Classes and instances

```python
class BankAccount:
    bank_name = "Example Bank"

    def __init__(self, owner: str, balance: float = 0.0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("amount must be positive")
        self._balance += amount
```

Instance attributes belong to each object. Class attributes are shared defaults and should not hold mutable per-instance
state.

## Instance, class, and static methods

- An **instance method** receives `self` and works with one object.
- A **class method** receives `cls` and commonly implements an alternate constructor.
- A **static method** receives neither and is a utility closely related to the class.

```python
from datetime import date

class Person:
    def __init__(self, name: str, birth_year: int):
        self.name = name
        self.birth_year = birth_year

    @classmethod
    def from_age(cls, name: str, age: int):
        return cls(name, date.today().year - age)
```

## Inheritance and polymorphism

Inheritance models an **is-a** relationship. Override behavior while preserving the parent's contract.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height
```

Polymorphism means callers depend on supported behavior rather than a concrete class. Python commonly uses duck typing:
if an object provides the required operation, its inheritance tree may not matter.

## Prefer composition for has-a relationships

```python
class Engine:
    def start(self) -> None:
        print("started")

class Car:
    def __init__(self, engine: Engine):
        self.engine = engine
```

Composition keeps components replaceable and avoids deep inheritance hierarchies.

## Data classes

Use `dataclass` for data-focused objects with generated initialization, representation, and equality.

```python 
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float
    tags: tuple[str, ...] = field(default_factory=tuple)
```

Use `default_factory` for mutable defaults. `frozen=True` prevents normal reassignment, and `slots=True` reduces
per-instance overhead and accidental attributes.

## Protocols **[FDE]**

Protocols describe behavior structurally and support type checking without requiring inheritance.

```python
from typing import Protocol

class Writable(Protocol):
    def write(self, text: str) -> int: ...

def save(output: Writable, text: str) -> None:
    output.write(text)
```

## Special methods

Implement special methods only when the corresponding behavior is natural:

- `__repr__` for debugging, 
- `__len__` for size,
- `__iter__` for iteration, and 
- `__enter__`/`__exit__` for resource management.

## Experiment: composition and polymorphism
Add another notification channel or change the formatter without modifying `AlertService`.

```python { .python-runner title="Composition and polymorphism experiment" }
class ConsoleNotifier:
    def send(self, message):
        print(f"console: {message}")

class UppercaseFormatter:
    def format(self, message):
        return message.upper()

class AlertService:
    def __init__(self, notifier, formatter):
        self.notifier = notifier
        self.formatter = formatter

    def alert(self, message):
        self.notifier.send(self.formatter.format(message))

service = AlertService(ConsoleNotifier(), UppercaseFormatter())
service.alert("deployment complete")
```

## Checkpoint

- Distinguish instance and class state.
- Choose among instance, class, and static methods.
- Use inheritance for is-a and composition for has-a.
- Apply abstract classes or protocols to stable contracts.
- Use data classes for data-focused models.

**Next:** [Pythonic iteration and resource handling](04_scalpel_pythonic_idioms.md)
