# Algorithms and problem solving

Algorithmic thinking is the ability to define a contract, select a suitable data structure, reason about cost, and
verify edge cases. Optimize only after establishing a correct baseline.

## Complexity

| Complexity   | Typical example               |
|--------------|-------------------------------|
| `O(1)`       | Dictionary lookup; list index |
| `O(log n)`   | Binary search in sorted data  |
| `O(n)`       | One pass over input           |
| `O(n log n)` | Comparison sorting            |
| `O(n²)`      | Comparing every pair          |
| `O(2ⁿ)`      | Enumerating all subsets       |

State both time and auxiliary space complexity. Built-in operations still have costs: slicing copies values, `x in list`
is linear, and `x in set` is constant-time on average.

## A repeatable method

1. Restate inputs, outputs, and invalid cases.
2. Work through a small example.
3. Write a clear baseline solution.
4. Identify the bottleneck.
5. Select a pattern or data structure that removes it.
6. Test normal, empty, minimal, duplicate, and boundary cases.
7. State complexity and trade-offs.

## Hash lookup

A dictionary can replace repeated scans with average constant-time lookup.

```python { .python-runner title="Hash lookup experiment" }
def two_sum(numbers: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}
    for index, number in enumerate(numbers):
        complement = target - number
        if complement in seen:
            return seen[complement], index
        seen[number] = index
    return None
```

Time is `O(n)` and auxiliary space is `O(n)`.

## Two pointers

Use pointers moving through ordered data or toward each other.

```python { .python-runner title="Two pointers experiment" }
def is_palindrome(text: str) -> bool:
    left, right = 0, len(text) - 1
    while left < right:
        if text[left] != text[right]:
            return False
        left += 1
        right -= 1
    return True
```

## Sliding window

Maintain a summary while moving over contiguous values instead of recomputing each range.

```python { .python-runner title="Sliding window experiment" }
def max_window_sum(numbers: list[int], size: int) -> int:
    if size <= 0 or size > len(numbers):
        raise ValueError("invalid window size")
    current = sum(numbers[:size])
    best = current
    for index in range(size, len(numbers)):
        current += numbers[index] - numbers[index - size]
        best = max(best, current)
    return best
```

## Binary search

Binary search requires a sorted search space or a monotonic condition.

```python { .python-runner title="Binary search experiment" }
def binary_search(values: list[int], target: int) -> int | None:
    low, high = 0, len(values) - 1
    while low <= high:
        middle = low + (high - low) // 2
        if values[middle] == target:
            return middle
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return None
```

## Breadth-first and depth-first search

Use breadth-first search for shortest paths in an unweighted graph and level-order traversal. Use depth-first search for
exhaustive traversal, reachability, and backtracking.

```python { .python-runner title="Breadth-first traversal experiment" }
from collections import deque


def breadth_first(graph, start):
    queue = deque([start])
    visited = {start}
    while queue:
        node = queue.popleft()
        yield node
        for neighbor in graph.get(node, ()):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

## Additional patterns

- **Stack:** nested structures, expression evaluation, depth-first traversal.
- **Heap:** repeatedly retrieving the smallest or largest items.
- **Prefix sum:** repeated range totals.
- **Backtracking:** combinations and constraint search.
- **Dynamic programming:** overlapping subproblems with reusable results.
- **Sorting plus scanning:** transform order to simplify later decisions.

## Experiment: compare solutions

Change the input size and target, then compare the number of pair checks with the hash-map solution.

```python { .python-runner title="Algorithm complexity experiment" }
def two_sum_brute(numbers, target):
    checks = 0
    for left in range(len(numbers)):
        for right in range(left + 1, len(numbers)):
            checks += 1
            if numbers[left] + numbers[right] == target:
                return (left, right), checks
    return None, checks


def two_sum_hash(numbers, target):
    seen = {}
    for index, number in enumerate(numbers):
        complement = target - number
        if complement in seen:
            return (seen[complement], index), index + 1
        seen[number] = index
    return None, len(numbers)


values = list(range(1_000))
target = 1_997
print("brute:", two_sum_brute(values, target))
print("hash: ", two_sum_hash(values, target))
```

## Checkpoint

- Explain complexity using input variables.
- Select hash lookup, pointers, windows, search, or traversal intentionally.
- State preconditions such as sorted or monotonic input.
- Verify edge cases and trade-offs.
- Prefer clear correctness over a clever one-liner.

**Next:** [Python quick reference](../reference/python-quick-reference.md)
