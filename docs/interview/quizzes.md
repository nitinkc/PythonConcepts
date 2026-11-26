# Senior Python interview quizzes

Select an answer and submit each question. Some questions have more than one correct answer; those use checkboxes and
require every correct option—and no incorrect option—to be selected. Progress is stored in your browser.

## Object model and language behavior

<quiz>
What does Python assignment do for a mutable object?
- [ ] Creates a shallow copy automatically
- [x] Binds a name to an object
- [ ] Converts the object into an immutable value
- [ ] Transfers ownership and invalidates the previous name

Assignment binds names. Two names can reference the same mutable object, so a mutation observed through one name is
visible through the other.
</quiz>

<quiz>
Why is a mutable default argument usually a defect?
- [ ] Python forbids mutation inside functions
- [x] The default object is created once when the function is defined
- [ ] Default values are copied on every call
- [ ] Lists cannot be used as function arguments

The same default object is reused by calls that omit that argument. Use `None` plus initialization inside the function,
or an appropriate immutable default.
</quiz>

<quiz>
Which statements about equality and hashing are correct?
- [x] Objects that compare equal must produce equal hashes
- [x] A dictionary key should not change in a way that changes its hash
- [ ] Every mutable object is hashable
- [ ] Equal hashes guarantee equal values

Hash collisions are allowed, so equal hashes do not prove equality. Mutating a stored key's hash-relevant state can make
its entry unreachable through normal lookup.
</quiz>

<quiz>
What is the primary meaning of `super()` in cooperative multiple inheritance?
- [ ] Call the first base class written in the class declaration
- [x] Continue method lookup at the next class in the current MRO
- [ ] Bypass overridden methods
- [ ] Invoke every base implementation concurrently

`super()` follows the method resolution order. Cooperative classes need compatible signatures and must continue the
chain consistently.
</quiz>

<quiz>
Why do lambdas created in a loop often all observe the final loop value?
- [ ] Lambdas execute immediately
- [x] Closures resolve the captured name when called
- [ ] Loop variables are process-global
- [ ] Python caches the first lambda result

This is late binding. A default parameter such as `lambda value=value: value` can intentionally capture each current
object.
</quiz>

## Iteration, resources, and memory

<quiz>
Which statements about generators are correct?
- [x] A generator suspends its execution frame at `yield`
- [x] A generator is normally consumed once
- [x] A suspended generator can keep referenced objects alive
- [ ] A generator always computes faster than a list

Generators provide lazy iteration and can reduce peak memory, but they add execution overhead and retain their suspended
frame until exhausted or closed.
</quiz>

<quiz>
A generator opens a file and yields lines. A caller consumes one line and stops. What is the strongest design?
- [ ] Rely on cyclic garbage collection to close the file immediately
- [ ] Add a broad `except Exception` around iteration
- [x] Make resource ownership explicit with a context manager and deterministic close behavior
- [ ] Read the entire file first in every case

Prompt cleanup should be part of the API contract. Garbage collection timing is not a portable resource-management
guarantee.
</quiz>

<quiz>
Which tool is most appropriate for locating unexpected allocation growth over time?
- [ ] `sorted`
- [ ] `functools.wraps`
- [x] `tracemalloc`
- [ ] `unittest.mock`

`tracemalloc` records Python allocation traces and snapshots that can be compared to identify growth.
</quiz>

## Concurrency and async

<quiz>
A service makes many requests through a synchronous HTTP client. Which initial design is most reasonable?
- [x] A bounded thread pool with timeouts
- [ ] An unbounded number of threads
- [ ] A process per HTTP request
- [ ] Mark the existing blocking function `async` without changing the client

Threads can overlap blocking I/O. Bound concurrency to protect local and downstream resources, and set explicit
timeouts.
</quiz>

<quiz>
Which statements about the conventional CPython GIL are correct?
- [x] It generally prevents parallel execution of Python bytecode in one process
- [x] It does not make multi-step application invariants thread-safe
- [x] I/O and some native extensions can release it
- [ ] It prevents all race conditions

The GIL protects interpreter internals, not your business invariants. Threads remain useful for I/O and native work that
releases the lock.
</quiz>

<quiz>
What happens when a blocking database client is called directly inside an async route?
- [ ] The event loop automatically moves it to another process
- [x] It can block the event-loop thread and delay unrelated requests
- [ ] The call becomes non-blocking because the route uses `async def`
- [ ] Python rejects the call at compile time

Use an async-compatible client or deliberately offload blocking work to a bounded executor.
</quiz>

<quiz>
Why prefer `asyncio.TaskGroup` for related concurrent operations?
- [ ] It converts CPU work into native machine code
- [x] It gives child tasks structured lifetime, failure, and cancellation behavior
- [ ] It disables exceptions from child tasks
- [ ] It creates an operating-system process for every coroutine

Structured concurrency keeps related tasks from silently outliving their owner and defines how sibling work responds to
failure.
</quiz>

<quiz>
Which controls help a high-concurrency client remain production-safe?
- [x] Bounded concurrency
- [x] Per-operation timeouts
- [x] Cancellation-aware cleanup
- [x] Backpressure
- [ ] Retrying every failure indefinitely

Concurrency without limits can overwhelm connection pools, memory, or downstream services. Retries need classification,
budgets, backoff, and idempotency.
</quiz>

## Typing, testing, and API design

<quiz>
Which statement best distinguishes type hints from runtime validation?
- [ ] Type hints always reject invalid input at runtime
- [x] Type hints support static analysis; runtime validation requires executable checks
- [ ] Runtime validation makes type hints useless
- [ ] Type hints only work for numeric values

Use both where appropriate: types document internal contracts, while validation protects external boundaries.
</quiz>

<quiz>
When is a `Protocol` especially useful?
- [ ] When every implementation must inherit shared state
- [x] When consumers need a structural behavior contract without forced inheritance
- [ ] When runtime input must be converted from JSON
- [ ] When a function has no parameters

Protocols let independently defined classes satisfy a typed interface by implementing the required members.
</quiz>

<quiz>
What is the most maintainable mocking strategy?
- [ ] Mock every internal function call
- [x] Mock slow or nondeterministic external boundaries and assert public behavior
- [ ] Avoid integration tests entirely
- [ ] Assert private call order in every unit test

Mocking implementation details creates brittle tests. Control external boundaries while keeping meaningful logic real.
</quiz>

<quiz>
A library catches a database exception and raises a domain exception. Which form preserves diagnostic causality?
- [ ] `raise DomainError()` with no context in every case
- [x] `raise DomainError("operation failed") from error`
- [ ] `return None`
- [ ] `except Exception: pass`

Explicit chaining preserves the original failure as the cause while presenting a stable domain-level API.
</quiz>

## Performance and architecture

<quiz>
What should happen before a performance optimization is selected?
- [ ] Rewrite all loops as comprehensions
- [ ] Add multiprocessing
- [x] Define a representative workload and measure the bottleneck
- [ ] Remove type annotations

Optimization starts with a user-visible objective and evidence. Algorithmic and I/O improvements generally matter more
than syntax-level changes.
</quiz>

<quiz>
A worker consumes messages that may be delivered more than once. Which property is most important?
- [ ] Recursive implementation
- [x] Idempotent processing or reliable deduplication
- [ ] Global mutable state
- [ ] An unlimited retry loop

At-least-once delivery requires handling duplicates without repeating harmful side effects.
</quiz>

<quiz>
Which concerns belong in a senior design for a rate-limited external API?
- [x] Connection reuse and bounded concurrency
- [x] Timeout and retry classification
- [x] Backoff with jitter and idempotency
- [x] Metrics for latency, errors, retries, and quota use
- [ ] Assuming every HTTP failure is transient

A robust client protects both systems, distinguishes retryable failures, and exposes enough telemetry to operate safely.
</quiz>

<quiz>
A dictionary lookup is commonly described as `O(1)`. What is the most precise interview answer?
- [ ] It is guaranteed constant time for every input
- [x] It is constant time on average, subject to hashing behavior and collisions
- [ ] It is always `O(log n)`
- [ ] It scans every key

Python dictionaries are hash tables. Average lookup is constant time, while pathological collisions can degrade
performance.
</quiz>

## FDE deep dive: modern Python

These questions cover the five **`[FDE]`**-tagged topics interviewers probe hardest: pattern matching, `Protocol`,
`asyncio` execution, strict typing, and Pydantic V2.

<quiz>
In `match status:` what does `case failed:` do, where `failed` is a bare name?
- [ ] Compares the subject to the variable `failed`
- [x] Matches anything and binds the subject to the name `failed`
- [ ] Compares the subject to the string `"failed"`
- [ ] Raises a syntax error

A bare name in a `case` is a capture pattern — it always matches and binds. To compare against an existing value, use a
literal, a dotted name such as `State.FAILED`, or a guard like `if status == failed`.
</quiz>

<quiz>
Which statements about `case {"type": "created", "id": int(item_id)}:` are correct?
- [x] It requires the keys `"type"` and `"id"` to be present
- [x] Extra keys in the subject do not prevent the match
- [x] `int(item_id)` runs the `int` class pattern and binds the id value
- [ ] The subject must contain exactly those two keys

Mapping patterns match a subset of keys; additional keys are ignored unless captured with `**rest`. Class patterns such
as `int(item_id)` check the runtime type and bind the attribute or value.
</quiz>

<quiz>
What does `@runtime_checkable` on a `Protocol` allow `isinstance` to verify?
- [ ] Full method signatures and return types
- [x] Only the presence of the required members
- [ ] That the class inherits from the Protocol
- [ ] The types of instance attributes

Runtime checks are structural presence tests only — `isinstance` cannot inspect signatures, and data-attribute Protocols
are not supported at runtime. Static checkers verify the complete contract.
</quiz>

<quiz>
When is a `Protocol` the better choice over an abstract base class?
- [x] When consumers should not control the concrete implementation hierarchy
- [x] When typing third-party or already-written classes
- [ ] When implementations must share inherited state or helper methods
- [ ] When method bodies must be enforced at runtime

Protocols express structural subtyping — a class satisfies one by implementing its members without inheriting anything.
ABCs are nominal, can share implementation, but force a common hierarchy.
</quiz>

<quiz>
What happens when you call `coro()` where `coro` is declared `async def`?
- [ ] The body starts running immediately on the event loop
- [ ] A new thread is created for it
- [x] A coroutine object is created; nothing runs until it is awaited or scheduled
- [ ] The body executes synchronously up to the first `await`

Calling an `async def` function is lazy — it produces a coroutine object. Forgetting to await it leaves the body
unexecuted and emits a "coroutine was never awaited" warning.
</quiz>

<quiz>
Why is `asyncio.create_task(work())` without storing the result a latent bug?
- [ ] The task is executed twice
- [x] The task may be garbage-collected mid-run and silently cancelled
- [ ] It blocks the event loop until awaited
- [ ] The task runs on the calling thread synchronously

The event loop keeps only weak references to scheduled tasks. Hold a strong reference — a set, a list, or a
`TaskGroup` — and retrieve the result so exceptions are not dropped.
</quiz>

<quiz>
Which behaviors does `mypy --strict` enforce beyond default checking?
- [x] Function signatures must be fully annotated
- [x] Returning `Any` from a typed function produces a warning
- [x] Bare generics such as `list` without parameters are rejected
- [ ] Type errors become runtime exceptions

`--strict` enables `disallow_untyped_defs`, `warn_return_any`, `disallow_any_generics`, `no_implicit_optional`, and
related flags. mypy is a static checker — it never changes what happens at runtime.
</quiz>

<quiz>
A mypy error cannot be fixed cleanly in legacy code. Which suppression is most defensible?
- [ ] `# type: ignore` on the whole file
- [x] `# type: ignore[attr-defined]` on the single line, with a justification comment
- [ ] Wrap the code in `try`/`except TypeError`
- [ ] Rewrite the annotation as `Any` everywhere

Code-scoped ignores fail loudly if the code changes in a way that produces a different error. Bare ignores and blanket
`Any` silently widen the unchecked surface.
</quiz>

<quiz>
In Pydantic V2, which are the correct replacements for V1's `@validator` and `.dict()`?
- [ ] `@validate` and `.to_dict()`
- [x] `@field_validator` and `.model_dump()`
- [ ] `@validator` still works identically in V2
- [ ] `@model_validator` and `.json()`

V2 renamed the API: `field_validator` / `model_validator` for validation, `model_dump` / `model_dump_json` for
serialization, `model_validate` for parsing, and `model_config = ConfigDict(...)` instead of `class Config`.
</quiz>

<quiz>
A PATCH endpoint merges a validated model into stored data. Which dump prevents defaults from overwriting fields the client omitted?
- [ ] `item.model_dump(include_none=True)`
- [x] `item.model_dump(exclude_unset=True)`
- [ ] `item.dict(exclude_defaults=True)`
- [ ] `item.model_copy()`

`exclude_unset` drops fields that were never supplied, so only provided values are merged — the standard pattern for
partial updates.
</quiz>

## Interpretation

- **25–30 correct:** strong recall; focus on communication, production stories, and system design.
- **19–24 correct:** interview-ready foundation; revisit explanations for missed topics.
- **13–18 correct:** review the advanced guide and repeat the quiz after coding examples.
- **Below 13:** work through the systematic learning path before emphasizing senior scenarios.

A score measures recall, not seniority. Senior performance also requires sound trade-offs, operational judgment, and
clear evidence from real engineering work.
