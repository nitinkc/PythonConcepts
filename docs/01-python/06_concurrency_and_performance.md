# Concurrency and performance

Choose an execution model from evidence about the workload. Concurrency improves throughput when tasks spend time
waiting; parallelism can reduce CPU-bound processing time.

## Start with measurement

Do not optimize from intuition alone. Measure representative work with `timeit` for small expressions and a profiler for
applications.

```python
from timeit import timeit

elapsed = timeit("sum(range(1000))", number=10_000)
print(elapsed)
```

Prefer algorithm and data-structure improvements before micro-optimizations.

## Threads

Threads share process memory and are suitable for blocking I/O such as multiple network requests. Shared mutable state
requires synchronization and can create race conditions.

```python { .python-runner title="Threads" }
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import hashlib
import math
import time

from concurrent.futures import ThreadPoolExecutor


# 2. Several blocking I/O calls -> Thread pool
def blocking_io_call(task_id: int) -> str:
    time.sleep(0.2)  # Simulates a 200ms blocking network/DB call
    return f"Result-{task_id}"


def demo_thread_pool():
    start = time.perf_counter()
    # 10 blocking calls of 0.2s each -> ~0.2s total instead of 2.0s
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(blocking_io_call, range(10)))
    elapsed = time.perf_counter() - start
    print(f"2. ThreadPool:   Fetched {len(results)} items | Time={elapsed:.3f}s")


if __name__ == "__main__":
    demo_thread_pool()
```

In standard CPython, the Global Interpreter Lock generally prevents Python bytecode from executing in parallel across
threads. Threads can still overlap I/O and native operations that release the lock.

## Processes

Processes have separate memory and can execute CPU-bound Python work in parallel. Data must be serialized between
processes, so startup and communication overhead matter.

```python
from concurrent.futures import ProcessPoolExecutor

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(calculate, inputs))
```

The main guard is essential for portable process creation.

```python  { .python-runner title="Process" }
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import hashlib
import math
import time


# 4. CPU-heavy independent tasks -> Process pool
def cpu_heavy_task(n: int) -> str:
    # CPU-bound cryptographic key stretching
    return hashlib.pbkdf2_hmac("sha256", f"block-{n}".encode(), b"salt", 200_000).hex()


def demo_process_pool():
    start = time.perf_counter()
    # Runs across multiple CPU cores in parallel
    with ProcessPoolExecutor() as pool:
        results = list(pool.map(cpu_heavy_task, range(8)))
    elapsed = time.perf_counter() - start
    print(f"4. ProcessPool:  Computed {len(results)} hashes | Time={elapsed:.3f}s")


if __name__ == "__main__":
    demo_process_pool()

```

## Asynchronous I/O **[FDE]**

`asyncio` coordinates many tasks cooperatively on an event loop. It is effective when libraries expose non-blocking
APIs.

```python { .python-runner title="Asynchronous I/O" }
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import hashlib
import math
import time


# 3. Many async-compatible I/O operations -> asyncio
async def async_io_call(task_id: int) -> str:
    await asyncio.sleep(0.2)  # Simulates a non-blocking 200ms network call
    return f"AsyncResult-{task_id}"


async def demo_asyncio():
    start = time.perf_counter()
    # 1,000 concurrent tasks on a single thread -> ~0.2s total
    tasks = [async_io_call(i) for i in range(1_000)]
    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    print(f"3. asyncio:      Fetched {len(results)} items | Time={elapsed:.3f}s")


if __name__ == "__main__":
    asyncio.run(demo_asyncio())
    
```

An `async def` function returns a coroutine. It runs when awaited or scheduled. Blocking calls inside asynchronous code
block the entire event loop; use an async library or deliberately offload that work.

## Selection guide

| Workload                             | First choice                                |
|--------------------------------------|---------------------------------------------|
| One simple sequential task           | Regular synchronous code                    |
| Several blocking I/O calls           | Thread pool                                 |
| Many async-compatible I/O operations | `asyncio`                                   |
| CPU-heavy independent tasks          | Process pool                                |
| Vectorized numeric work              | Optimized library before custom parallelism |

## Common hazards

- Race conditions from unsynchronized shared state.
- Deadlocks from inconsistent lock ordering.
- Unbounded task creation and exhausted resources.
- Exceptions that are never retrieved from background tasks.
- Process overhead exceeding the work performed.
- Benchmarks using unrealistic or tiny inputs.

Use timeouts, bounded concurrency, structured cleanup, and cancellation-aware code.

## Experiment: asynchronous scheduling

Change the delays and task count. Notice that total duration follows the slowest concurrent task rather than the sum of
every delay.

```python { .python-runner title="Asynchronous scheduling experiment" }
import asyncio
import time


async def worker(name, delay):
    await asyncio.sleep(delay)
    return f"{name} finished after {delay:.2f}s"


async def main():
    started = time.perf_counter()
    results = await asyncio.gather(
        worker("A", 0.10),
        worker("B", 0.20),
        worker("C", 0.05),
    )
    print(*results, sep="\n")
    print(f"total: {time.perf_counter() - started:.2f}s")


await main()
```

## Checkpoint

- Distinguish concurrency from parallelism.
- Choose threads, processes, or async I/O based on the workload.
- Explain the practical impact of CPython's GIL.
- Keep blocking work off an event loop.
- Measure before and after an optimization.

**Next:** [Algorithms and problem solving](03_forge_algorithms_and_interview.md)
