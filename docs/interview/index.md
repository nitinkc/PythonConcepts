# Senior Python interview guide

Use this section for rapid preparation after completing the learning path. Senior interviews evaluate judgment: explain
not only how Python behaves, but also the trade-offs, failure modes, and production consequences.

## Preparation tracks

| Available time | Focus                                                                    |
|----------------|--------------------------------------------------------------------------|
| 30 minutes     | Review the rapid-recall tables and rehearse two system-design stories    |
| 2 hours        | Add object model, concurrency, testing, and performance sections         |
| 1 day          | Complete the advanced guide, quizzes, and two coding exercises           |
| 1 week         | Repeat quizzes, practice design discussions, and conduct mock interviews |

## Rapid recall

### Object model

- Names bind to objects; assignment does not copy.
- `==` compares values; `is` compares identity.
- Mutability belongs to the object, not the variable.
- Function arguments use call-by-sharing: the function receives another reference to the same object.
- Default argument expressions execute once when the function is defined.
- Attribute lookup broadly checks the instance, its class, and the class MRO; descriptors can intercept lookup.
- A class is an object created by a metaclass; `type` is the usual metaclass.

### Collections and complexity

| Operation                               |   Typical cost | Caveat                               |
|-----------------------------------------|---------------:|--------------------------------------|
| List index or append                    |         `O(1)` | Append is amortized                  |
| List membership or insertion near front |         `O(n)` | Elements are scanned or shifted      |
| Dict/set lookup                         | `O(1)` average | Hash collisions can degrade behavior |
| Heap push/pop                           |     `O(log n)` | Root lookup is `O(1)`                |
| Sorting                                 |   `O(n log n)` | Timsort exploits existing order      |
| `deque` append/pop at either end        |         `O(1)` | Random access is not its strength    |

### Functions and iteration

- Closures capture names through cells, not frozen values; late binding matters in loops.
- A decorator replaces a callable at definition time.
- An iterable creates an iterator; an iterator retains traversal state.
- A generator suspends its frame at `yield` and is normally single-use.
- Generator expressions are lazy, but referenced objects may remain alive until exhaustion.
- Context managers guarantee paired entry and exit, not successful completion.

### Concurrency

| Work                                     | First choice             | Reason                                           |
|------------------------------------------|--------------------------|--------------------------------------------------|
| Blocking I/O using synchronous libraries | Threads                  | Waiting releases execution opportunity           |
| Many async-compatible I/O operations     | `asyncio`                | Low-overhead cooperative scheduling              |
| CPU-heavy pure Python                    | Processes                | Bypasses the conventional CPython GIL            |
| Numeric array operations                 | Optimized native library | Vectorization usually beats Python orchestration |

`async` is concurrency, not automatic parallelism. Never call blocking I/O directly on an event-loop thread. Use bounded
concurrency, timeouts, cancellation, and structured cleanup.

### Reliability

- Catch the narrowest exception you can handle.
- Chain translated exceptions with `raise ... from error`.
- Test observable contracts and failure paths, not private implementation details.
- Mock at external boundaries; excessive mocking makes refactoring difficult.
- Type hints aid static analysis but do not validate runtime input.
- Design retries only for transient, idempotent operations and add backoff plus jitter.

## Coding interview loop

1. **Clarify:** define inputs, outputs, invalid cases, scale, and ordering requirements.
2. **Example:** walk through a normal and an adversarial case.
3. **Baseline:** state a correct simple solution before optimizing.
4. **Choose:** connect the bottleneck to a data structure or pattern.
5. **Implement:** use meaningful names and maintain explicit invariants.
6. **Verify:** manually test empty, singleton, duplicate, boundary, and failure cases.
7. **Analyze:** state time and auxiliary space using named input variables.
8. **Extend:** discuss production concerns such as memory, streaming, observability, and concurrency.

## Senior answer structure

For design and experience questions, use **Context → Constraints → Decision → Trade-offs → Evidence**.

> We processed independent I/O-bound jobs with a bounded thread pool because the client library was synchronous. We
> capped concurrency to protect the dependency, applied per-request timeouts, and collected latency and error metrics.
> Async I/O could reduce thread overhead, but migrating the client would have increased delivery risk. Load tests showed a
> fourfold throughput improvement without raising downstream error rates.

Avoid presenting a technology as universally best. State what evidence would make you choose differently.

## Python system-design checklist

- Public API and ownership boundaries
- Data model, persistence, consistency, and migration strategy
- Expected throughput, latency, payload size, and growth
- Synchronous request path versus background work
- Idempotency, retries, deduplication, and failure recovery
- Concurrency limits, backpressure, and timeouts
- Authentication, authorization, validation, and secret handling
- Logs, metrics, traces, alerting, and operational runbooks
- Test pyramid, deployment strategy, rollback, and compatibility
- Cost, team familiarity, and deliberately deferred complexity

## Behavioral prompts to prepare

Prepare evidence-based stories for:

- A design decision with meaningful trade-offs
- A production incident and prevention work
- A performance problem solved through measurement
- A disagreement resolved with data
- A migration delivered without breaking consumers
- Technical debt intentionally accepted or removed
- Mentoring or raising engineering standards

Quantify impact where possible, but do not invent precision.

## Common weak answers

| Weak answer                          | Stronger direction                                                              |
|--------------------------------------|---------------------------------------------------------------------------------|
| “Async makes Python faster.”         | Explain I/O concurrency, blocking hazards, and when processes are needed        |
| “Dict lookup is always O(1).”        | Say average `O(1)` and discuss hashing and key correctness                      |
| “The GIL means threads are useless.” | Separate Python CPU work from I/O and native extensions                         |
| “Microservices scale better.”        | Start from boundaries, deployment needs, operational cost, and team constraints |
| “We need 100% test coverage.”        | Prioritize risk, contracts, failure modes, and mutation-resistant assertions    |
| “Type hints prevent invalid input.”  | Separate static analysis from runtime validation                                |

## Final checklist

- Explain five Python object-model traps without running code.
- Choose correctly among threads, processes, and async I/O.
- Analyze unfamiliar code for complexity, resource lifetime, and failure behavior.
- Design a typed, observable, testable service and defend its boundaries.
- Communicate alternatives and evidence instead of only naming tools.
- Complete the [advanced Python guide](../01-python/advanced-python.md) and [senior quizzes](quizzes.md).
