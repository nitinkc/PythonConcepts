### The __***3 Layers***__ of Running Python Code

When you run Python applications (like FastAPI), there are three distinct layers:

1. **Environment & Package Management**: Installing packages without breaking system tools (`venv`, `pip`, `uv`).
2. **Project Specification**: How you declare what packages your app needs (`requirements.txt` vs. `pyproject.toml`).
3. **Application Server/Runner**: The engine that serves your web app (`uvicorn` vs. `fastapi dev`).

### Application-Level Interface Protocols

1. **WSGI (Web Server Gateway Interface):** Designed for synchronous
  frameworks (classic Django, Flask).
    - **Synchronous**, traditional request/response.

2. **ASGI (Asynchronous Server Gateway Interface):** Designed to handle concurrent
  connections, async I/O, **WebSockets**, Server-Sent Events (SSE), and long-polling (FastAPI, modern Django, Starlette).
     - **Asynchronous**, event-loop driven.

3. **RSGI (Rust Server Gateway Interface)**: A newer alternative to ASGI developed specifically for the Granian HTTP
  server. Passes raw HTTP data directly across the Python/Rust boundary with minimal serialization overhead, giving
  higher throughput than ASGI.

4. CGI / FastCGI / SCGI (Legacy): Obsolete in modern Python; replaced universally by WSGI and ASGI.
    The original gateway interfaces that spawned an entirely new process per request (CGI) or persistent worker sockets (FastCGI).

---

### How `uv` is related

```text
┌────────────────────────────────────────────────────────┐
│                          uv                            │
│  (Covers: venv + pip + pyenv + pipx + Poetry/PDM/Hatch)│
└────────────────────────────────────────────────────────┘
                           │
       Replaces or unifies these separate tools:
       ├── Environment creation  ──► venv
       ├── Package installation  ──► pip
       ├── Python versioning     ──► pyenv
       ├── Global CLI tools      ──► pipx
       └── Project & lockfiles   ──► Poetry / PDM / Hatch
```

- **`venv` and `pip`** are the standard, low-level building blocks.
- **Poetry, PDM, and Hatch** brought modern `pyproject.toml` workflows to Python.
- **`uv`** takes those modern workflows and makes them **unified and fast**.

### TL;DR — Which Stack Should You Use?

**Starting a new FastAPI project today** `uv` + `pyproject.toml`**

```shell
uv init my-project
uv add "fastapi[standard]"
uv run fastapi dev main.py
```

**Deploying to Docker / Production**
```shell
Use `uvicorn main:app --host 0.0.0.0 --port 8000` inside your container or process supervisor                                |
```

**Maintaining an older or minimal environment without `uv`**

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Running a one-off standalone script with dependencies** 
```shell
uv run --with requests script.py 
```

**Heavy GPU / scientific ML work** **Conda / Mamba** —

```shell
`uv`/`pip` can't reliably install non-Python binaries like CUDA                                          |
```

### Python Environment & Tooling Matrix (Ready Reference)

| Tool              | Category                        | What It Does                                                                                                                      | Why Use It / Current Status                                                                                                                           |
|:------------------|:--------------------------------|:----------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
| **`venv`**        | Virtual Environment Creator     | Creates lightweight, isolated directories with their own Python binary.                                                           | **Standard Library**: Built into Python 3.3+. Requires no extra installation, but does not install packages by itself.                                |
| **`pip`**         | Package Installer               | Downloads and installs packages from PyPI into an environment using `requirements.txt`.                                           | **Standard Package Manager**: Comes bundled with Python. Simple, but lacks native lockfile and project metadata management.                           |
| **`uv`**          | Unified Python Toolchain (Rust) | Replaces `pip`, `venv`, `pyenv`, `pipx`, and `poetry` with a single, fast binary.                                                 | **Modern Standard / Trending**: Extremely fast (10–100x), fully supports `pyproject.toml` and `uv.lock`. Best choice for new projects.                |
| **Poetry**        | All-in-One Project Manager      | Manages `pyproject.toml`, resolves dependencies, creates lockfiles (`poetry.lock`), builds packages.                              | **Enterprise Standard**: Widely adopted in existing codebases before `uv`. Written in Python, so slower resolution; many teams are migrating to `uv`. |
| **Hatch**         | Modern Project Manager          | PyPA-recommended project manager and build backend; strong support for matrix environments and testing.                           | **Popular & Standard-Compliant**: Follows strict PEP standards with `pyproject.toml`.                                                                 |
| **PDM**           | Modern Package Manager          | Supports PEP 621 (`pyproject.toml`) and modular build backends.                                                                   | **Active Alternative**: Clean modern implementation, alternative to Poetry.                                                                           |
| **Pipenv**        | Workflow Manager                | Combines `pip` + `virtualenv` using `Pipfile` and `Pipfile.lock`.                                                                 | **Declining / Legacy**: Pioneered lockfiles for Python, but largely superseded by Poetry and `uv`.                                                    |
| **Conda / Mamba** | Cross-Language Package Manager  | Manages Python environments along with non-Python binary dependencies (CUDA, C++, BLAS). Mamba is a faster C++ drop-in for Conda. | **Data Science & ML Standard**: Best for GPU and scientific computing; unnecessarily heavy for web APIs.                                              |
| **Pyenv**         | Python Version Manager          | Installs and switches between different Python engine versions (3.9, 3.11, 3.13, PyPy).                                           | **Widely Used**: Specialized tool for managing multiple Python versions on one OS. Mostly superseded by `uv python install`.                          |
| **Pipx**          | Isolated CLI Runner             | Runs and installs Python CLI tools (like `ruff`, `black`, `pre-commit`) in dedicated isolated environments.                       | **Widely Used**: Prevents global tool dependencies from conflicting with your system Python. Mostly superseded by `uvx`/`uv tool`.                    |

---

### Deep Dive: `uv` (The Daily Driver)

`uv` is an extremely fast Python package & project manager written in **Rust**. It ***completely replaces*** `pip`, `venv`, `pyenv`, `pipx`, and `poetry` with a single binary — installs run 10x–100x faster, and you never need to manually activate a virtual environment.

#### Install `uv`

```bash
# macOS / Linux
brew install uv
# or the official installer:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Standard Project Workflow

```bash
# 1. Initialize a new project (creates pyproject.toml and a .venv automatically)
uv init my-api
## If you are building an application rather than a reusable library
uv init --app my-api
uv init --no-package taskapi

cd my-api

# 2. Add dependencies (updates pyproject.toml & creates a deterministic uv.lock file)
uv add "fastapi[standard]"

# 3. Run any command directly (uv manages the virtual environment automatically)
uv run python main.py
uv run fastapi dev main.py

uv run -m http.server 8000
```

#### Everything Else `uv` Replaces

| Task                          | Old Toolchain                     | Modern `uv` Equivalent                                  |
|:------------------------------|:----------------------------------|:--------------------------------------------------------|
| Virtual environments          | `python -m venv .venv`            | `uv venv`                                               |
| Installing packages           | `pip install numpy`               | `uv pip install numpy`                                  |
| Install from requirements     | `pip install -r requirements.txt` | `uv pip install -r requirements.txt`                    |
| Project dependencies & locks  | `poetry` or `pip-tools`           | `uv add` / `uv.lock`                                    |
| Multiple Python versions      | `pyenv install 3.12`              | `uv python install 3.12`                                |
| Running isolated CLIs         | `pipx run ruff`                   | `uvx ruff` (or `uv tool install ruff`)                  |
| One-off script with deps      | manual venv + install             | `uv run --with requests script.py`                      |
| One-off run from requirements | manual venv + install             | `uv run --with-requirements requirements.txt <command>` |

#### Working in an Existing (non-uv) Project

```bash
uv venv                          # create .venv (add --seed to pre-install pip/setuptools)
uv pip install -r requirements.txt
source .venv/bin/activate        # optional — only if you want classic activation
```

**Recommendation:** Understand what `venv` and `pip` do conceptually, but use **`uv` + `pyproject.toml`** as your daily driver. When you encounter older projects, recognize what `Pipfile` (Pipenv), `poetry.lock` (Poetry), and `environment.yml` (Conda) represent — then move on.

---

### `pyproject.toml` vs. `requirements.txt`

- **For any new project today:** Prefer **`pyproject.toml`**. It consolidates all configuration (dependencies, build system, tool settings) into one standard file — and it's what `uv`, Poetry, Hatch, and PDM all use.
- **When to use `requirements.txt`:** Quick tutorials, older CI/CD scripts, or exporting a frozen snapshot (`pip freeze > requirements.txt`).

### Fallback: The Traditional Way (`venv` + `pip`)

For minimal environments where `uv` isn't available:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

- **Pros:** Universal; works everywhere without installing external tools.
- **Cons:** Slower installs and dependency resolution; manual venv activation.

**Useful tips:**

```bash
# If pip is missing inside a venv, bootstrap it into the active env:
python -m ensurepip --upgrade
```

```bash
# Add to ~/.zshrc to block pip installs when NO virtualenv is active
# (prevents accidentally polluting system Python):
export PIP_REQUIRE_VIRTUALENV=true
```

---

### Running Web Servers: `uvicorn` vs. `fastapi dev`

Both commands start an ASGI server (FastAPI runs on ASGI), but they serve different phases:

```text
[ Your Code (app) ] ──▶ [ ASGI Server (Uvicorn) ] ──▶ [ Web / HTTP Client ]
```

#### `fastapi dev fast_api.py` (Local Development)

- **What it is:** The official FastAPI CLI wrapper designed for active development.
- **What it does under the hood:** Automatically starts `uvicorn` with hot-reload enabled, mounts the interactive docs
  UI, and formats debug logs nicely.
- **When to use:** **Everyday local development.**

#### `uvicorn examples.web.fastapi_app:app --reload` (Underlying Server)

- **Syntax breakdown:** `path.to.module:app_variable --reload`
- **What it is:** The actual server engine running the ASGI event loop.
- **When to use:**
  - Production deployments (without `--reload`, often managed with multiple workers:
    `uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4`).
  - When configuring low-level network options, SSL certificates, or custom ASGI middleware directly.


#### Fast API with uv



```shell
uv init --no-package --python 3.13 taskapi

uv add "fastapi[standard]"
uv run fastapi dev
uv run fastapi dev --port 8001
```


```txt
root .
├── README.md
├── pyproject.toml
├── src
│   └── testapi
│       ├── __init__.py
│       └── main.py
└── uv.lock
```

```toml
[tool.fastapi]
entrypoint = "testapi.main:app"
```

```shell
uv run fastapi dev --port 8001
```

---

### Common Python Servers (Ready Reference)

| Server | Type | Primary Use Case | Key Features / Notes |
| :--- | :--- | :--- | :--- |
| **Uvicorn** | ASGI | FastAPI, Starlette, Django Channels | High-performance, built on `uvloop` and `httptools`. Standard for async APIs and WebSockets. |
| **Gunicorn** | WSGI (Process Manager) | Flask, Django (production) | Robust pre-fork worker model. Industry standard process supervisor for production deployments. |
| **Daphne** | ASGI | Django Channels, WebSockets | Official server built by the Django Channels team. Native support for HTTP/2 and WebSockets. |
| **Hypercorn** | ASGI | FastAPI, Quart, WebSockets | Supports HTTP/1.1, HTTP/2, and **HTTP/3 (QUIC)**. Driven by `asyncio` or `trio`. |
| **Granian** | ASGI / RSGI / WSGI | High-concurrency APIs | Rust-based HTTP server for Python. Exceptionally high throughput and low memory footprint. |
| **uWSGI** | WSGI / Custom | Legacy enterprise Django/Flask | Highly configurable and fast, but complex syntax and configuration. Considered in maintenance mode. |
| **Waitress** | WSGI | Windows & Linux deployments | Pure Python, production-ready, no C-compiler needed. Great for internal tools and cross-platform apps. |

**Which server should you choose?**

- **FastAPI / Starlette (REST + WebSockets):** Use **`uvicorn`** (or **`granian`** for maximum raw speed).
- **Standard Django / Flask (No WebSockets):** Use **`gunicorn`**.
- **Django with WebSockets (Channels):** Use **`daphne`** or **`uvicorn`**.
- **Edge cases requiring HTTP/3:** Use **`hypercorn`**.

---

### Common Framework Architectures & Patterns

#### 1. Traditional Django (Synchronous / Standard HTTP)

Classic Django views are synchronous and run on WSGI:

- **Local Dev:** `python manage.py runserver` (built-in dev server, not for production).
- **Production:** **Gunicorn** handling multiple worker processes:

```bash
gunicorn myproject.wsgi:application --workers 4 --bind 0.0.0.0:8000
```

#### 2. Django with WebSockets & Real-Time (Django Channels / Async)

When Django needs WebSockets, chat systems, or notifications, it requires an ASGI server:

```bash
# Option A (Daphne - Django native):
daphne -b 0.0.0.0 -p 8000 myproject.asgi:application

# Option B (Uvicorn workers):
uvicorn myproject.asgi:application --host 0.0.0.0 --port 8000 --workers 4
```

#### 3. The Gold Standard Production Pattern: Gunicorn + Uvicorn Workers

For high-traffic production workloads (FastAPI or async Django), a very common pattern combines

- **Gunicorn** as the process manager with
- **Uvicorn** as the worker:

```text
[ Nginx / Cloud Load Balancer ]
            │
            ▼
[ Gunicorn Master Process ]  (monitors health, reboots crashed processes)
        ├── [ Uvicorn Worker 1 ] (handles async event loop + WebSockets)
        ├── [ Uvicorn Worker 2 ]
        └── [ Uvicorn Worker 3 ]
```

```bash
gunicorn main:app \
      --workers 4 \
      --worker-class uvicorn.workers.UvicornWorker \
      --bind 0.0.0.0:8000
```

**Why this works well:** Gunicorn handles process management, worker restarts, and OS-level signals, while Uvicorn
handles the fast async event loop and WebSocket connections inside each worker.
