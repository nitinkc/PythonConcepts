# Senior Python: internals and metaprogramming

Senior Python work requires understanding the protocols behind ordinary syntax. Use these mechanisms to make APIs
predictable—not merely clever.

## The data model

Operations delegate to special methods: iteration uses `__iter__`, containment uses `__contains__`, calls use
`__call__`, and context management uses `__enter__` and `__exit__`. Implement only coherent protocols and obey their
expected contracts.

```python { .python-runner title="Data model experiment" }
class Version:
    def __init__(self, major, minor):
        self.major = major
        self.minor = minor

    def __repr__(self):
        return f"Version({self.major}, {self.minor})"

    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor) == (other.major, other.minor)

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor) < (other.major, other.minor)


versions = [Version(3, 12), Version(3, 10), Version(3, 14)]
print(sorted(versions))
print(Version(3, 12) == (3, 12))
```

Return `NotImplemented` for unsupported comparisons so Python can try reflected behavior. Equal hashable objects must
have equal hashes, and hash-relevant state must not mutate.

## Attribute lookup and descriptors

A descriptor centralizes attribute behavior through `__get__`, `__set__`, or `__delete__`. Functions, properties, class
methods, and many ORM fields are descriptors.

```python { .python-runner title="Descriptor validation experiment" }
class Positive:
    def __set_name__(self, owner, name):
        self.storage_name = f"_{name}"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError("value must be positive")
        setattr(instance, self.storage_name, value)


class Product:
    price = Positive()
    quantity = Positive()

    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity


product = Product(9.99, 2)
print(product.price * product.quantity)
try:
    product.quantity = 0
except ValueError as error:
    print(type(error).__name__, error)
```

A data descriptor usually takes precedence over an instance dictionary entry. Prefer a property for behavior used by one
class and a descriptor for semantics reused across classes.

## MRO and cooperative inheritance

Python uses C3 linearization. `super()` continues at the next class in the current method resolution order; it does not
mean “my direct parent.” Cooperative mixins need compatible signatures and must forward the call.

```python { .python-runner title="Cooperative inheritance experiment" }
class LoggingMixin:
    def save(self, **kwargs):
        print("logging")
        return super().save(**kwargs)
```

Inspect resolution with `Class.mro()`. Prefer composition unless every subclass genuinely satisfies the base contract.

## Classes and metaclasses

A class body executes to produce a namespace, then its metaclass creates the class object. Use `__init_subclass__` for
most registration and subclass validation; use a metaclass only when class creation itself must be controlled across a
hierarchy.

```python { .python-runner title="Subclass registration experiment" }
class Handler:
    registry = {}

    def __init_subclass__(cls, *, event, **kwargs):
        super().__init_subclass__(**kwargs)
        Handler.registry[event] = cls
```

Metaclasses are appropriate for framework infrastructure such as declarative models. They are usually excessive for
application-level factories or registries.

## Structural pattern matching **[FDE]**

`match` performs structural decomposition, not general boolean branching. Cases run top to bottom; guards add
conditions.

```python
match message:
    case {"type": "created", "id": int(item_id)}:
        handle_created(item_id)
    case {"type": "deleted", "id": item_id} if item_id > 0:
        handle_deleted(item_id)
    case _:
        raise ValueError("unsupported message")
```

Mapping patterns ignore additional keys unless captured. Class patterns depend on `__match_args__` or named attributes.
Avoid pattern matching when a dictionary dispatch table is simpler.

## Generic functions with `singledispatch`

`functools.singledispatch` chooses an implementation from the first argument's runtime type. It is useful for open
conversion or rendering operations, but not for validation across several arguments.

```python { .python-runner title="Single dispatch experiment" }
from functools import singledispatch


@singledispatch
def serialize(value):
    raise TypeError(f"unsupported: {type(value).__name__}")


@serialize.register
def _(value: int):
    return str(value)
```

## Interview checkpoints

- Explain `NotImplemented` versus raising `NotImplementedError`.
- Trace descriptor and instance-attribute precedence.
- Predict a diamond hierarchy's MRO and explain cooperative `super()`.
- Choose between a decorator, descriptor, `__init_subclass__`, and metaclass.
- Explain when pattern matching improves or harms maintainability.
