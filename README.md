# Python Concepts

A focused Python learning repository with structured MkDocs documentation, small runnable examples, and tests.

## Repository structure

```text
docs/       Systematic Python and FastAPI learning material
examples/   One focused executable example per major concept
tests/      Tests for the maintained examples
mkdocs.yml  Documentation site configuration
```

The documentation is the canonical learning path. The examples exist only to demonstrate behavior that is useful to run
or test.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Alternatively, run commands in an isolated environment with `uv`:

```bash
uv run --with-requirements requirements.txt <command>
```

## Documentation

```bash
mkdocs serve
mkdocs build --strict
```

## Examples

```bash
python -m examples.fundamentals.collections
python -m examples.functions.imports_and_main
python -m examples.object_oriented.calculator
python -m examples.concurrency.execution_models
python -m examples.typing.mypy_strict_demo
```

Strict typing check on the practice file (errors are intentional — fix them as a drill):

```bash
mypy --strict examples/typing/mypy_strict_demo.py
```

The Jupyter GUI example is imported and displayed from a notebook:

```python
from examples.gui import create_order_form

create_order_form()
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## FastAPI example

```bash
uvicorn examples.web.fastapi_app:app --reload
```

Available routes include `GET /`, `GET /health`, `GET /items`, `GET /items/{item_id}`, and `POST /items`.

!!! info "Browser runtime"
    These playgrounds support Python language exercises and many pure-Python packages. Server processes, unrestricted networking, operating-system access, Selenium, FastAPI servers, and process pools must run locally.

Edit the code and select **Run Python**.

```python { .python-runner title="Collections experiment" }
words = ["python", "api", "python", "widgets"]
counts = {word: words.count(word) for word in set(words)}
unique_in_order = list(dict.fromkeys(words))

print(counts)
print(unique_in_order)
```