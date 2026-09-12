# Pythonic iteration and resource handling

Python's iteration tools separate **what values are produced** from **how they are consumed**. Prefer clear, lazy pipelines for large inputs and explicit loops when logic has side effects or several branches.

## Comprehensions

Use comprehensions for a single transformation with an optional simple filter.

```python { .python-runner title="Comprehensions experiment" }
squares = [number**2 for number in range(10)]
even_squares = {number: number**2 for number in range(10) if number % 2 == 0}
letters = {word[0] for word in ["apple", "apricot", "banana"]}
```

Do not force complex branching, exception handling, or side effects into a comprehension. A normal loop is then easier to read.

## Iterables, iterators, and generators

An **iterable** can produce an iterator. An **iterator** tracks progress and returns its next item through `next()`. A **generator** is an iterator created by a function containing `yield` or by a generator expression.

```python
def read_nonempty(lines):
    for line in lines:
        text = line.strip()
        if text:
            yield text

length_total = sum(len(line) for line in read_nonempty(source))
```

Generators are lazy: they produce one item at a time and are normally consumed once. This reduces memory use, but it does not automatically make computation faster.

## Useful built-ins

```python
for index, value in enumerate(values, start=1):
    print(index, value)

pairs = zip(names, scores, strict=True)
ordered = sorted(records, key=lambda record: record["date"], reverse=True)
has_error = any(result.failed for result in results)
all_ready = all(worker.ready for worker in workers)
```

Other common tools include `min`, `max`, `sum`, `reversed`, `map`, and `filter`. Comprehensions are often clearer than `map` and `filter` when a lambda would be required.

## Standard-library iteration tools

- `collections.Counter` counts hashable values.
- `collections.defaultdict` supplies missing values from a factory.
- `collections.deque` supports efficient operations at both ends.
- `itertools.chain` joins iterables lazily.
- `itertools.islice` takes a lazy slice.
- `itertools.pairwise` yields adjacent pairs.
- `functools.reduce` combines values cumulatively, though `sum` or a loop is often clearer.

```python
from collections import Counter, deque
from itertools import chain, islice

counts = Counter(words)
queue = deque([start])
first_ten = list(islice(chain(source_a, source_b), 10))
```

## Decorators

A decorator receives a callable and returns a replacement callable. Preserve metadata with `functools.wraps`.

```python { .python-runner title="Decorator experiment" }
from functools import wraps

def trace(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        print(f"calling {function.__name__}")
        return function(*args, **kwargs)
    return wrapper
```

Decorators are useful for cross-cutting behavior such as caching, registration, authorization, and instrumentation. Keep business logic visible rather than stacking opaque decorators.

## Context managers

A context manager pairs acquisition with guaranteed cleanup.

```python
from pathlib import Path

with Path("data.txt").open(encoding="utf-8") as stream:
    data = stream.read()
```

Create one from a generator when needed:

```python
from contextlib import contextmanager

@contextmanager
def transaction(connection):
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
```

## Experiment: lazy iteration

Change the filter, remove `islice`, or consume the generator twice and compare the results.

```python { .python-runner title="Lazy iteration experiment" }
from itertools import islice


def matching_squares(limit, divisor):
    for number in range(limit):
        square = number ** 2
        if square % divisor == 0:
            yield square

values = matching_squares(1_000_000, 3)
print("first five:", list(islice(values, 5)))
print("next three: ", list(islice(values, 3)))
print("remaining generator:", values)
```

## Checkpoint

- Use comprehensions only when they remain readable.
- Explain iterable, iterator, and generator.
- Build lazy pipelines without accidentally consuming them twice.
- Reach for standard-library tools before custom loops.
- Use decorators and context managers for focused, reusable behavior.

**Next:** [Errors, files, testing, and typing](05_reliability_testing_and_typing.md)
