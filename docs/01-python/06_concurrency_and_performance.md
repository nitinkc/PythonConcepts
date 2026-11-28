# Concurrency and performance

Choose an execution model from evidence about the workload. Concurrency improves throughput when tasks spend time
waiting; parallelism can reduce CPU-bound processing time.

The examples on this page mirror
[`examples/concurrency/execution_models.py`](https://github.com/nitinkc/PythonConcepts/blob/main/examples/concurrency/execution_models.py),
which drives the same three-element task list through a thread pool, a process pool, and `asyncio`.

## Two kinds of workload

Every concurrency decision starts by identifying what a task spends its time on.

- **I/O-bound** work waits on something external: the network, disk, a database, a lock, `sleep()`. The CPU is mostly
  idle while the task waits, so *overlapping the waits* is what matters.
- **CPU-bound** work is busy computing: hashing, compression, parsing, numeric loops. The CPU is the bottleneck, so the
  only way to go faster is to *use more cores*.

```python
from time import sleep

def blocking_io(value: int) -> int:
    sleep(0.01)          # I/O-bound: the thread sits idle, waiting
    return value

def cpu_bound(value: int) -> int:
    return sum(number * number for number in range(value))  # CPU-bound: pure computation
```

## Concurrency is not parallelism

- **Concurrency** is about *structure*: several tasks make progress by interleaving. Only one may be executing at any
  instant, but while one waits, another can run.
- **Parallelism** is about *execution*: several tasks literally run at the same instant on different CPU cores.

All three models below provide concurrency. Only `ProcessPoolExecutor` provides parallelism for Python code.

| Model                 | Provides    | Best for                          |
|-----------------------|-------------|-----------------------------------|
| `ThreadPoolExecutor`  | Concurrency | Blocking I/O calls                |
| `asyncio`             | Concurrency | Many async-compatible I/O tasks   |
| `ProcessPoolExecutor` | Parallelism | CPU-bound work                    |

`asyncio` does **not** run tasks in parallel — it is a single thread that switches between coroutines at `await`
points. Threads in standard CPython do not execute Python bytecode in parallel either (see the GIL below); they overlap
only the *waiting*, not the *computing*.

## Start with measurement

Do not optimize from intuition alone. Measure representative work with `timeit` for small expressions and a profiler for
applications.

```python
from timeit import timeit

elapsed = timeit("sum(range(1000))", number=10_000)
print(elapsed)
```

Prefer algorithm and data-structure improvements before micro-optimizations.

## Threads: concurrency for blocking I/O

Threads **share process memory** and are suitable for **blocking I/O** such as multiple network requests. Shared mutable
state requires synchronization and can create race conditions.

```python
from concurrent.futures import ThreadPoolExecutor
from time import sleep

def blocking_io(value: int) -> int:
    sleep(0.01)
    return value

def run_threaded(values: list[int]) -> list[int]:
    with ThreadPoolExecutor() as executor:
        return list(executor.map(blocking_io, values))
```

In standard CPython, the **Global Interpreter Lock (GIL)** prevents Python bytecode from executing in parallel across
threads. Threads still help here because `sleep()` — like socket and file I/O — **releases the GIL while it waits**, so
ten `blocking_io` calls finish in roughly one wait instead of ten sequential waits.

The same pool gives no speedup on `cpu_bound`: pure Python computation holds the GIL, so threads merely take turns.
Free-threaded CPython builds (3.13+) can remove this limit, but the standard build still has the GIL.

## Processes: parallelism for CPU-bound work

Processes have **separate interpreters and separate memory**, so each has its own GIL and they execute Python code truly
in parallel across cores.

```python
from concurrent.futures import ProcessPoolExecutor

def cpu_bound(value: int) -> int:
    return sum(number * number for number in range(value))

def run_parallel(values: list[int]) -> list[int]:
    with ProcessPoolExecutor() as executor:
        return list(executor.map(cpu_bound, values))
```

Trade-offs to weigh:

- Arguments and results are **pickled** between processes — functions must be importable (module-level, not closures)
  and data must be serializable. That is why `cpu_bound` is a top-level function.
- Process startup and serialization cost real time. Parallelism only pays off when each task is expensive enough to
  outweigh it; `sum(range(3))` would be faster sequentially.
- The `if __name__ == "__main__":` guard is essential so child processes do not re-run the spawning code on import.

## Asynchronous I/O **[FDE]**

`asyncio` runs many tasks **cooperatively on a single thread**. Each `await` is a yield point where the event loop can
switch to another coroutine. It is effective when libraries expose non-blocking APIs, and it scales to thousands of
waiting tasks with far less memory than a thread per task.

```python
import asyncio

async def run_async(values: list[int]) -> list[int]:
    async def identity(value: int) -> int:
        await asyncio.sleep(0.01)   # yields control; the loop runs other coroutines meanwhile
        return value

    return list(await asyncio.gather(*(identity(value) for value in values)))
```

Key rules:

- An `async def` function only **returns a coroutine** — nothing runs until it is awaited, gathered, or scheduled.
  `asyncio.run()` starts the event loop; `asyncio.gather()` schedules the coroutines concurrently and returns results in
  input order.
- `asyncio.sleep()` is not `time.sleep()`. `await asyncio.sleep()` parks the coroutine and frees the loop; calling
  `time.sleep()` inside a coroutine **blocks the entire event loop** and every task on it stalls. Offload unavoidable
  blocking calls with `asyncio.to_thread()`.
- Because everything shares one thread, `identity` can safely be a closure — no pickling, no locks needed for
  coroutine-local state between `await` points.
- Async is not a CPU-bound tool: a hot loop inside a coroutine never yields and starves the loop. CPU work belongs in a
  process pool.

## One task list, three models

The complete file runs identical input through all three models. The output is the same each time — `[1, 2, 3]` —
because the models differ in *how* the work is scheduled, not in *what* it produces:

```python
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from time import sleep

def blocking_io(value: int) -> int:
    sleep(0.01)
    return value

def cpu_bound(value: int) -> int:
    return sum(number * number for number in range(value))

def run_threaded(values: list[int]) -> list[int]:
    with ThreadPoolExecutor() as executor:
        return list(executor.map(blocking_io, values))

def run_parallel(values: list[int]) -> list[int]:
    with ProcessPoolExecutor() as executor:
        return list(executor.map(cpu_bound, values))

async def run_async(values: list[int]) -> list[int]:
    async def identity(value: int) -> int:
        await asyncio.sleep(0.01)
        return value

    return list(await asyncio.gather(*(identity(value) for value in values)))

def main() -> None:
    values = [1, 2, 3]
    print(run_threaded(values))
    print(run_parallel(values))
    print(asyncio.run(run_async(values)))

if __name__ == "__main__":
    main()
```

Run it locally with `python examples/concurrency/execution_models.py`. (Thread and process pools need real OS threads
and processes, so this file cannot run in the browser-based runner — the asyncio experiment below can.)

## Selection guide

| Workload                             | First choice                                |
|--------------------------------------|---------------------------------------------|
| One simple sequential task           | Regular synchronous code                    |
| Several blocking I/O calls           | Thread pool                                 |
| Many async-compatible I/O operations | `asyncio`                                   |
| CPU-heavy independent tasks          | Process pool                                |
| CPU work inside async code           | `loop.run_in_executor()` with a process pool|
| Blocking call inside async code      | `asyncio.to_thread()`                       |
| Vectorized numeric work              | Optimized library before custom parallelism |

## Common hazards

- Race conditions from unsynchronized shared state.
- Deadlocks from inconsistent lock ordering.
- A blocking call inside a coroutine stalling the entire event loop.
- Unbounded task creation and exhausted resources.
- Exceptions that are never retrieved from background tasks.
- Process overhead exceeding the work performed.
- Benchmarks using unrealistic or tiny inputs.

Use timeouts, bounded concurrency, structured cleanup, and cancellation-aware code.

## Experiment: asynchronous scheduling

Change the delays and task count. Notice that total duration follows the slowest concurrent task rather than the sum of
every delay — the hallmark of cooperative concurrency.

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

- Distinguish I/O-bound from CPU-bound work before choosing a model.
- Distinguish concurrency (interleaved progress) from parallelism (simultaneous execution).
- Choose threads for blocking I/O, processes for CPU work, `asyncio` for many async-compatible I/O tasks.
- Explain the practical impact of CPython's GIL: `sleep()` and socket I/O release it; pure-Python computation holds it.
- Keep blocking work off an event loop — `await asyncio.sleep()`, never `time.sleep()`.
- Measure before and after an optimization.

**Next:** [Algorithms and problem solving](07_forge_algorithms_and_interview.md)
