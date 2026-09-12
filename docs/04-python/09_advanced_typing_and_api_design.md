# Senior Python: typing and API design

Senior typing work makes relationships and boundaries visible while keeping APIs usable. Static types do not replace runtime validation.

## Structural interfaces

A `Protocol` lets independent classes satisfy an interface without inheriting from it.

```python { .python-runner title="Protocol-shaped design experiment" }
from typing import Protocol

class Writer(Protocol):
    def write(self, text: str) -> int: ...

class Buffer:
    def __init__(self):
        self.values = []

    def write(self, text):
        self.values.append(text)
        return len(text)

def publish(destination: Writer, message: str) -> int:
    return destination.write(message)

buffer = Buffer()
print(publish(buffer, "event accepted"))
print(buffer.values)
```

Protocols are primarily static. Add `@runtime_checkable` only when a limited runtime structural check is actually needed.

## Generics and variance

`TypeVar` expresses a relationship between types. Mutable generic containers are normally invariant because accepting a broader type could allow unsafe writes. Read-only producers can be covariant; consumers can be contravariant.

- `Sequence[Dog]` can be viewed as `Sequence[Animal]` because it is read-only.
- `list[Dog]` cannot safely be treated as `list[Animal]` because a caller could append a `Cat`.
- Prefer immutable interfaces when covariance improves API flexibility.

Modern Python also supports type-parameter syntax, but library version support should guide public APIs.

## Callable signatures

Use `ParamSpec` when a decorator preserves arbitrary parameters and a type variable for its return value.

```python
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def traced(function: Callable[P, R]) -> Callable[P, R]:
    @wraps(function)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(function.__name__)
        return function(*args, **kwargs)
    return wrapper
```

Use overloads when return types depend on distinct input shapes. Keep the runtime implementation after the overload declarations and ensure all declared cases are true.

## Domain types

Use `NewType` to distinguish primitive identifiers statically, `Literal` for a closed set of values, enums when values need runtime identity and behavior, and data classes for structured internal values.

```python { .python-runner title="Domain model and compatibility experiment" }
from dataclasses import dataclass
from enum import StrEnum

class Status(StrEnum):
    PENDING = "pending"
    COMPLETE = "complete"

@dataclass(frozen=True, slots=True)
class Job:
    id: int
    status: Status = Status.PENDING

    @classmethod
    def from_payload(cls, payload):
        return cls(id=int(payload["id"]), status=Status(payload.get("status", "pending")))

for payload in [{"id": "42"}, {"id": 7, "status": "complete"}]:
    job = Job.from_payload(payload)
    print(job, job.status.value)
```

`TypedDict` describes mapping-shaped data but performs no conversion. Validate untrusted payloads before creating trusted domain objects.

## Stable public APIs

A public contract includes names, signatures, return shapes, exceptions, side effects, ordering, performance expectations, and compatibility behavior.

- Prefer keyword-only parameters for options likely to grow.
- Return stable domain abstractions rather than internal persistence objects.
- Use specific documented exceptions.
- Avoid boolean parameters whose meaning is unclear at the call site.
- Add new optional behavior compatibly; deprecate before removal.
- Keep import paths stable or provide forwarding aliases during migration.

## Serialization and versioning

JSON is interoperable but supports few native types. Schema-based formats can enforce compatibility. `pickle` is Python-specific and unsafe for untrusted input because loading may execute code.

Version externally stored or transmitted data. Readers should tolerate additive fields where possible, while writers should produce one deliberate current version.

```python
payload = {"schema_version": 2, "id": 42, "status": "pending"}
```

Migrations should be deterministic, observable, restartable, and tested against representative historical data.

## Packaging contracts

Use `pyproject.toml` for build metadata, dependencies, tools, and entry points. Separate runtime from development dependencies, constrain compatibility intentionally, and use a reproducible lock or constraints strategy for deployed applications.

Libraries should avoid unnecessarily strict transitive pins; applications should deploy reproducibly. Keep imports free of network calls, configuration mutation, and expensive initialization.

## Interview checkpoints

- Explain why mutable containers are invariant.
- Choose between a protocol, abstract base class, and concrete dependency.
- Type a signature-preserving decorator.
- Separate static typing, parsing, validation, and domain modeling.
- Design an additive API change and a safe deprecation path.
- Explain why untrusted pickle data is dangerous.
