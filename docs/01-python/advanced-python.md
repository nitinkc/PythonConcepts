# Advanced Python interview topics

These topics distinguish language familiarity from senior-level reasoning. For each one, be prepared to predict
behavior, explain the mechanism, identify risks, and propose a maintainable design.

## Data model and protocols

Python syntax delegates to protocols implemented by special methods. `len(x)` calls `x.__len__()`, iteration requests
`iter(x)`, and a context manager uses `__enter__` and `__exit__`.

Prefer implementing the smallest coherent protocol. An object with surprising equality, ordering, or truth behavior is
harder to maintain than one with fewer methods.

### Equality and hashing

Equal objects must have equal hashes. Hash keys should be effectively immutable while stored in a dictionary or set.

```python
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserId:
    value: int
```

Overriding mutable value equality while retaining identity-based hashing violates collection assumptions. Data classes
disable or synthesize hashing based on their equality and mutability options.

## Attribute lookup and descriptors

Functions defined on a class are descriptors: accessing one through an instance creates a bound method. Properties,
class methods, static methods, and many ORM fields also use the descriptor protocol.

A descriptor implements `__get__`, `__set__`, or `__delete__`. Data descriptors generally take precedence over instance
attributes; non-data descriptors can be shadowed by an instance attribute.

Use descriptors for reusable attribute semantics. Use a property when behavior belongs to one class and a plain
attribute when no interception is needed.

## Inheritance and MRO

Python uses C3 linearization to create a consistent method resolution order. `super()` means “continue from the next
class in this MRO,” not simply “call my parent.” Cooperative multiple inheritance requires compatible signatures and
every implementation forwarding with `super()`.

Prefer composition when components do not share a genuine substitutable contract. Deep inheritance increases hidden
coupling.

## Closures and late binding

Closures resolve captured names when called:

```python
functions = [lambda value=value: value for value in range(3)]
```

The default argument intentionally freezes each current value. Without it, all functions would read the final loop
value.

## Decorators and metadata

A decorator executes when its function is defined and binds the returned callable to the original name. Use
`functools.wraps` to retain metadata and `ParamSpec` plus `TypeVar` when preserving a typed signature.

Decorator order is bottom-up during application. Stacked decorators can hide control flow, so reserve them for stable
cross-cutting behavior.

## Iteration, generators, and cleanup

A generator owns a suspended frame, local variables, and references. `send`, `throw`, and `close` communicate with that
frame. `yield from` delegates iteration and propagates generator return values.

Do not rely on garbage collection for prompt resource cleanup. Put acquisition inside a context manager and explicitly
close partially consumed generators when resource lifetime matters.

## Memory management

CPython primarily uses reference counting plus a cyclic garbage collector. Reference counting often destroys unreachable
objects immediately, but this is an implementation detail—not a portable cleanup contract.

Useful tools include:

- `sys.getsizeof` for shallow object size
- `tracemalloc` for allocation tracing
- `gc` for cycle diagnostics
- weak references for non-owning caches and registries
- `__slots__` to remove the normal per-instance dictionary where appropriate

Measure realistic workloads before changing representation.

## GIL and concurrency

The conventional CPython GIL protects interpreter state; it does not make compound operations or application invariants
automatically thread-safe. Context switches can occur between bytecode operations, and I/O or native code may release
the GIL.

Senior design discussion should include:

- Workload classification and library compatibility
- Shared-state ownership
- Bounded queues and backpressure
- Cancellation and timeout propagation
- Exception collection from tasks and workers
- Graceful shutdown and resource cleanup
- Whether native code releases the GIL
- Serialization and startup costs for processes

## Async internals **[FDE]**

Calling an `async def` function creates a coroutine object. `await` suspends the current coroutine and lets the event
loop run other ready work. A task schedules a coroutine and retains its result or exception.

Use `asyncio.TaskGroup` for related child tasks so failure and cancellation remain structured. Protect scarce
dependencies with semaphores or bounded worker queues. Treat cancellation as normal control flow and perform cleanup in
`finally` blocks.

## Typing at scale **[FDE]**

Use types to expose stable contracts, not to reproduce every runtime detail.

- `Protocol` provides structural interfaces.
- `TypeVar` relates input and output types.
- `ParamSpec` preserves callable parameters.
- `TypedDict` describes mapping-shaped records.
- `Literal` constrains known values.
- `NewType` distinguishes otherwise identical primitives statically.
- Generics are invariant unless declared or defined otherwise.

Keep `Any` at untyped boundaries and narrow it quickly. Runtime validation remains a separate concern.

## Imports and packaging

Importing executes module top-level code once and caches the module in `sys.modules`. Circular imports expose partially
initialized modules. Reduce cycles by moving shared contracts downward, importing modules rather than many symbols, or
deferring integration wiring.

A production package should define:

- A build configuration and explicit runtime dependencies
- A stable public API
- Semantic versioning and deprecation policy
- Reproducible environment or lock strategy
- Minimal import-time side effects
- Console entry points instead of ad hoc path manipulation

## Exceptions and API design

Exceptions form part of an API contract. Raise specific domain exceptions, preserve causes, and avoid leaking
infrastructure details across layers.

For batch operations, decide whether to fail fast, collect independent failures, or return partial results.
`ExceptionGroup` and `except*` can represent concurrent independent failures, but simpler result models may be easier
for consumers.

## Testing strategy

A senior test strategy balances confidence, feedback speed, and maintenance cost:

- Unit tests for pure logic and edge cases
- Contract tests at service boundaries
- Integration tests for database, queue, and framework behavior
- End-to-end tests for a small number of critical journeys
- Property-based tests for broad invariants when valuable
- Load and resilience tests for operational risks

Avoid asserting internal call sequences unless those interactions are the contract. A test suite that prevents
refactoring is not automatically high quality.

## Performance engineering

1. Define a user-visible objective and representative workload.
2. Measure wall time, CPU, allocations, I/O, and tail latency as relevant.
3. Profile before selecting an optimization.
4. Improve algorithms, reduce I/O, batch work, or choose better representations.
5. Re-measure and add a regression benchmark when stability matters.

Common tools include `timeit`, `cProfile`, `pstats`, `tracemalloc`, and sampling profilers. Beware of cold-start
effects, caches, unrealistic microbenchmarks, and optimizing average latency while worsening the tail.

## Architecture discussion prompts

### Large file ingestion

Discuss streaming, bounded memory, validation, checkpointing, idempotent writes, malformed records, observability, and
restart behavior.

### Rate-limited external API

Discuss connection reuse, bounded concurrency, timeouts, retry classification, exponential backoff with jitter,
idempotency, circuit breaking, caching, and downstream quotas.

### Background job system

Discuss delivery semantics, idempotent handlers, visibility timeouts, poison messages, retry budgets, dead-letter
handling, ordering, backpressure, and graceful shutdown.

### Public Python library

Discuss API boundaries, typing, documentation, compatibility, dependency minimization, deprecations, packaging, test
matrix, and release automation.

## Code-review checklist

- Is the contract clear and appropriately typed?
- Are mutable state and ownership obvious?
- Are resources closed on success, failure, and cancellation?
- Are exceptions actionable and causes retained?
- Could input size cause excessive CPU, memory, or recursion?
- Is concurrency bounded and failure propagation defined?
- Are logs useful without exposing secrets or personal data?
- Do tests cover behavior and important failure modes?
- Is a standard-library or existing project abstraction preferable?
