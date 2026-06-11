# PythonLearning

A small Python learning workspace with package demos, unit tests, and Selenium examples.

## 1) Setup

Create and activate a virtual environment, then install dependencies.

```bash
cd "/Users/nchaur590@cable.comcast.com/Programming/PythonLearning"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

.venv/bin/python -m mkdocs serve

```

## 2) Run the current demos

Run from the project root (organized under `demos/`):

```bash
python3 -m demos.package_runner
python3 -m demos.class_runner
python3 -m demos.module_test_demo
python3 -m demos.wildcard_import_demo
python3 -m demos.dict_merge_demo
```

## 3) Run unit tests

```bash
python3 -m unittest discover -s learning/basic_concepts/unitTest -p "test_*.py"
```

## 4) Run the Selenium demo

```bash
python3 learning/selenium/learn.py
```

Notes:
- Selenium needs Chrome installed.
- You may also need a compatible ChromeDriver available for your environment.

## 5) FastAPI-ready dependency flow

`requirements.txt` already includes `fastapi` and `uvicorn` so you can start creating API demos without reinstalling packages each time.

When you add a new library, update and freeze versions with:

```bash
pip install <package-name>
pip freeze > requirements.txt
```

Then anyone can recreate your environment with:

```bash
pip install -r requirements.txt
```

## 6) Run FastAPI demo

The current API app is at `fastapi_demo/main.py` with `app = FastAPI()`.

```bash
uvicorn fastapi_demo.main:app --reload
```

Available routes:
- `GET /`
- `GET /health`

## 7) Run API smoke test

Start the API first, then in another terminal run:

```bash
python3 -m demos.api_smoke_test
```
