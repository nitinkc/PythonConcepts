# Senior Python: production async and concurrency

Production concurrency is a resource-management problem. Correct code defines ownership, limits, failure propagation, cancellation, and shutdown—not only task creation.

## Structured concurrency

`TaskGroup` gives related tasks a shared lifetime. If one child fails, siblings are cancelled and failures are reported together.

```python { .python-runner title="TaskGroup failure experiment" }
import asyncio

async def worker(name, delay, fail=False):
    try:
        await asyncio.sleep(delay)
        if fail:
            raise RuntimeError(f"{name} failed")
        return f"{name} complete"
    finally:
        print(f"{name} cleaned up")

async def main():
    tasks = []
    try:
        async with asyncio.TaskGroup() as group:
            tasks.append(group.create_task(worker("fast", 0.05)))
            tasks.append(group.create_task(worker("broken", 0.10, fail=True)))
            tasks.append(group.create_task(worker("slow", 1.00)))
    except* RuntimeError as group:
        print("failures:", [str(error) for error in group.exceptions])

await main()
```

Do not create orphan tasks whose exceptions and lifetime nobody owns. Retain task references and define shutdown behavior for legitimate background work.

## Bounded concurrency and backpressure

A semaphore caps active access; a bounded queue also slows producers when consumers cannot keep up.

```python { .python-runner title="Bounded concurrency experiment" }
import asyncio

active = 0
peak = 0
limit = asyncio.Semaphore(3)

async def operation(value):
    global active, peak
    async with limit:
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0.02)
        active -= 1
        return value * 2

results = await asyncio.gather(*(operation(value) for value in range(12)))
print("results:", results)
print("peak concurrency:", peak)
```

Choose limits from downstream capacity, connection pools, memory, and latency—not arbitrary large numbers.

## Timeouts and cancellation

Use `asyncio.timeout` around a meaningful operation boundary. Cancellation is normal control flow: use `finally` for cleanup and usually re-raise `CancelledError` rather than suppressing it.

Shielding prevents caller cancellation from stopping work and should be rare. It changes ownership and can leave work running after its requester is gone.

## Async iterators and context managers

An async iterator awaits between values through `__aiter__` and `__anext__`. An async generator provides the same protocol with `async def` and `yield`.

```python
async def pages(client):
    cursor = None
    while True:
        page = await client.fetch(cursor=cursor)
        for item in page.items:
            yield item
        cursor = page.next_cursor
        if cursor is None:
            break
```

An async context manager pairs awaited acquisition and cleanup. Use `contextlib.asynccontextmanager` for concise resource scopes.

## Request-local state with `contextvars`

Thread-local storage is insufficient when many coroutines share a thread. A `ContextVar` provides task-local context that child tasks normally inherit.

```python
from contextvars import ContextVar

request_id = ContextVar("request_id", default="unknown")
token = request_id.set("request-42")
try:
    process_request()
finally:
    request_id.reset(token)
```

Use explicit parameters for core domain data. Context variables suit cross-cutting request metadata such as trace identifiers.

## Threads and processes

Use threads for synchronous blocking I/O and native operations that release the GIL. Protect shared invariants with locks or, preferably, single ownership and message passing.

Use processes for substantial independent CPU work. Account for startup, serialization, copied memory, worker crashes, and platform-specific process creation. Send compact immutable inputs rather than a large object graph.

## Retry design

Retry only failures likely to be transient. Require idempotency for operations with side effects, cap attempts and elapsed time, use exponential backoff with jitter, and emit retry metrics.

Do not layer uncoordinated retries across clients, services, and workers: multiplicative retries can amplify an outage.

## Graceful shutdown

1. Stop accepting new work.
2. Signal workers and producers.
3. Allow bounded time for in-flight work.
4. Cancel remaining tasks.
5. Await cleanup and close pools, clients, and files.
6. Report incomplete work so it can be retried safely.

## Free-threaded Python

Newer CPython builds may run without the traditional GIL. This can improve CPU parallelism for compatible workloads, but extension compatibility, synchronization costs, and application race conditions still matter. Never use the GIL as an application lock.

## Interview checkpoints

- Explain structured versus detached task creation.
- Design bounded fan-out to a rate-limited service.
- Propagate cancellation without leaking resources.
- Choose task-local context versus explicit parameters.
- Explain thread and process failure modes beyond the GIL.
- Design idempotent retries and graceful shutdown.
