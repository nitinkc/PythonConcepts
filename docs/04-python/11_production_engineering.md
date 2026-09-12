# Senior Python: production engineering

Senior engineers optimize for changeability and operability. Code must remain understandable under failure, load, migration, and team ownership.

## Configuration and secrets

Load configuration at the application boundary, validate it once, and pass typed settings inward. Keep secrets out of source, logs, exceptions, command lines, and generated documentation.

```python { .python-runner title="Configuration boundary experiment" }
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Settings:
    timeout_seconds: float
    max_attempts: int

    @classmethod
    def from_mapping(cls, values):
        timeout = float(values.get("TIMEOUT_SECONDS", "5"))
        attempts = int(values.get("MAX_ATTEMPTS", "3"))
        if timeout <= 0 or attempts < 1:
            raise ValueError("invalid settings")
        return cls(timeout, attempts)

for values in [{}, {"TIMEOUT_SECONDS": "0.5", "MAX_ATTEMPTS": "4"}]:
    print(Settings.from_mapping(values))
```

Environment variables are transport, not a domain model. Convert strings and reject invalid combinations during startup.

## Structured logging and observability

Logs describe discrete events with stable names and fields. Metrics aggregate rates, errors, durations, saturation, and business outcomes. Traces connect work across boundaries.

- Avoid personal data, credentials, and payload dumps.
- Include correlation identifiers where useful.
- Log exceptions once at the boundary that handles or terminates them.
- Prefer bounded-cardinality metric labels.
- Alert on user impact and exhausted capacity, not every individual error.

## Caching

Caching trades freshness and complexity for latency or reduced load. Define the key, lifetime, invalidation rule, size bound, concurrency behavior, and failure policy.

```python { .python-runner title="Bounded cache experiment" }
from functools import lru_cache

calls = 0

@lru_cache(maxsize=3)
def normalize(value):
    global calls
    calls += 1
    return value.strip().casefold()

for value in [" Python ", "SQL", " Python ", "API", "HTTP", "SQL"]:
    print(value, "->", normalize(value))

print("function calls:", calls)
print("cache:", normalize.cache_info())
```

Do not cache exceptions or authorization results accidentally. Distributed caches add serialization, network failure, consistency, and stampede concerns.

## Transactions and idempotency

A transaction protects database invariants, not external side effects. Keep transactions short and never hold one open while waiting on slow remote calls.

For workflows spanning systems, use durable state, idempotency keys, outbox/inbox patterns, compensating actions, or a workflow engine. “Exactly once” is usually implemented as at-least-once delivery plus deduplication and idempotent effects.

## Serialization and trust boundaries

Validate size, shape, type, range, and authorization at external boundaries. Treat deserialization, file upload, archive extraction, templates, regular expressions, and subprocess arguments as security-sensitive.

Never unpickle untrusted bytes. Avoid shell command construction from strings; pass an argument list and use `shell=False`. Apply time and resource limits to untrusted or expensive work.

## Testing portfolio

| Test type | Primary value |
|---|---|
| Unit | Fast feedback for focused logic |
| Property-based | Broad invariant and edge-case exploration |
| Contract | Compatibility between consumers and providers |
| Integration | Real database, queue, framework, or filesystem behavior |
| End-to-end | A few critical user journeys |
| Load/resilience | Capacity and failure behavior |

A useful property test generates many cases and asserts an invariant, such as decode-encode round trips or sorted output preserving elements.

```python { .python-runner title="Property-style invariant experiment" }
import random

random.seed(7)
for size in range(50):
    values = [random.randint(-20, 20) for _ in range(size)]
    ordered = sorted(values)
    assert len(ordered) == len(values)
    assert ordered == sorted(ordered)
    assert sorted(ordered, reverse=True) == list(reversed(ordered))

print("150 invariants checked successfully")
```

Hypothesis automates generation and shrinking in a local test suite. Browser examples keep dependencies small while demonstrating the same reasoning.

## Profiling and memory

Begin with an objective and representative workload. Use a sampling profiler for whole-system hotspots, `cProfile` for call-level CPU analysis, `timeit` for isolated expressions, and `tracemalloc` for Python allocation growth.

Measure tail latency and memory peaks when averages hide operational risk. Optimize algorithms, I/O count, batching, and representation before syntax.

## Compatibility and migration

- Version public behavior and persisted schemas deliberately.
- Make readers tolerant before writers emit a new shape.
- Deploy expand-and-contract database migrations.
- Provide deprecation warnings and migration instructions.
- Use feature flags for reversible rollout, not permanent branching.
- Observe adoption before removing old behavior.

## Code ownership and review

A senior review asks whether ownership, failure behavior, resource bounds, observability, security, and migration are clear. Prefer a smaller understandable design over abstractions justified only by hypothetical reuse.

Record important architectural decisions with their context and rejected alternatives. Revisit them when constraints change.

## Interview checkpoints

- Design validated configuration without global mutable state.
- Explain logs versus metrics versus traces.
- Define a cache invalidation and stampede strategy.
- Coordinate database changes with external side effects.
- Build a risk-based test portfolio.
- Investigate CPU, latency, and memory with different tools.
- Plan a backward-compatible schema and API migration.
