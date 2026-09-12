# Python playground

Run focused Python examples directly in your browser. The first run downloads the Pyodide runtime; later runs reuse it. Code executes locally in your browser and is not sent to this site.

!!! info "Browser runtime"
    These playgrounds support Python language exercises and many pure-Python packages. Server processes, unrestricted networking, operating-system access, Selenium, FastAPI servers, and process pools must run locally.

## Collections

Edit the code and select **Run Python**.

```python { .python-runner title="Collections experiment" }
words = ["python", "api", "python", "widgets"]
counts = {word: words.count(word) for word in set(words)}
unique_in_order = list(dict.fromkeys(words))

print(counts)
print(unique_in_order)
```

## Functions and generators

```python { .python-runner title="Functions and generators experiment" }
def even_squares(limit):
    for number in range(limit):
        if number % 2 == 0:
            yield number ** 2

print(list(even_squares(10)))
print(sum(even_squares(1_000)))
```

## Algorithm practice

```python { .python-runner title="Two Sum experiment" }
def two_sum(numbers, target):
    seen = {}
    for index, number in enumerate(numbers):
        complement = target - number
        if complement in seen:
            return seen[complement], index
        seen[number] = index
    return None

print(two_sum([2, 7, 11, 15], 9))
print(two_sum([3, 3], 6))
```

## Need a full notebook?

Use the <a href="../lab/">browser-based JupyterLab</a> for multi-cell experiments and GUI widgets. The lab also runs locally in your browser and does not require a Python server.
