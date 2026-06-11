# ⚡ FastAPI Boot Camp — Part 3: Async, Middleware, Routers & Production Patterns
### The architecture knowledge that separates junior from senior

> **Goal:** Understand async correctly, structure real applications with routers, and know the production patterns that FDE interviewers specifically probe.

---

## 1. Async — When to Use It and When Not To

This is the most misunderstood part of FastAPI. The rule is simple but important:

| Operation | Use | Why |
|---|---|---|
| DB query (async driver) | `async def` | Non-blocking I/O |
| External HTTP request | `async def` | Waiting on network |
| CPU-heavy computation | `def` (sync) | Async doesn't help here |
| File read (small) | Either | Negligible difference |
| Calling a sync library | `def` | Can't `await` sync code |

```python
import httpx  # async-compatible HTTP client

# ✅ CORRECT — I/O bound: use async
@app.get("/weather/{city}")
async def get_weather(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weather.com/{city}")
    return response.json()


# ✅ CORRECT — CPU bound or sync library: use regular def
@app.get("/compute/{n}")
def heavy_compute(n: int):
    result = sum(i ** 2 for i in range(n))  # CPU work, async won't help
    return {"result": result}


# ❌ WRONG — calling blocking code inside async def freezes the entire server
@app.get("/bad/")
async def bad_endpoint():
    import time
    time.sleep(5)   # THIS BLOCKS THE EVENT LOOP — kills concurrent performance
    return {"status": "done"}

# ✅ FIX — run blocking work in a thread pool
import asyncio
from fastapi.concurrency import run_in_threadpool

@app.get("/ok/")
async def good_endpoint():
    result = await run_in_threadpool(blocking_function, arg1, arg2)
    return {"result": result}
```

> **Interview line:** *"`async def` in FastAPI doesn't make code faster on its own — it only helps when you're waiting on I/O. Blocking calls inside an async route freeze the event loop and kill concurrency."*

---

## 2. Application Routers — Structuring Real Projects

Don't put everything in `main.py`. Use `APIRouter` to split routes into modules.

### Project structure

```
project/
├── main.py
├── routers/
│   ├── items.py
│   ├── users.py
│   └── orders.py
├── models/
│   └── schemas.py
└── dependencies.py
```

### `routers/items.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_current_user

router = APIRouter(
    prefix="/items",             # All routes start with /items
    tags=["items"],              # Groups routes in /docs
    dependencies=[Depends(get_current_user)],  # Applied to ALL routes in this router
    responses={404: {"description": "Not found"}},
)

@router.get("/")                # Full path: GET /items/
def list_items():
    return [{"name": "Widget"}, {"name": "Gadget"}]

@router.get("/{item_id}")       # Full path: GET /items/{item_id}
def get_item(item_id: int):
    return {"item_id": item_id}

@router.post("/")               # Full path: POST /items/
def create_item():
    return {"created": True}
```

### `main.py`

```python
from fastapi import FastAPI
from routers import items, users, orders

app = FastAPI()

app.include_router(items.router)
app.include_router(users.router)
app.include_router(orders.router, prefix="/v2")  # Override/extend prefix
```

---

## 3. Middleware

Middleware runs on every request/response. Use for logging, timing, CORS, auth headers.

### Custom middleware

```python
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)   # call the actual route handler
    process_time = time.time() - start
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### CORS Middleware — almost always needed

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://myapp.com", "http://localhost:3000"],  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

> **Interview tip:** If asked "how do you handle CORS?", say: *"I add `CORSMiddleware` with explicit origin allowlists in production — never `*` in production if credentials are involved."*

---

## 4. Lifespan Events — Startup & Shutdown

For initializing DB pools, loading ML models, connecting to message queues.

```python
from contextlib import asynccontextmanager

# Modern approach (05-FastAPI 0.93+)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: runs before the app starts serving requests
    print("Starting up...")
    await db_pool.connect()
    load_ml_model()

    yield  # ← app runs here

    # SHUTDOWN: runs when the app is stopping
    print("Shutting down...")
    await db_pool.disconnect()

app = FastAPI(lifespan=lifespan)
```

---

## 5. Response Types Beyond JSON

```python
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
    PlainTextResponse,
    FileResponse,
    StreamingResponse,
    RedirectResponse,
)

# HTML response
@app.get("/page", response_class=HTMLResponse)
def get_page():
    return "<html><body><h1>Hello</h1></body></html>"

# File download
@app.get("/download/{filename}")
def download_file(filename: str):
    return FileResponse(
        path=f"/files/{filename}",
        media_type="application/octet-stream",
        filename=filename           # sets Content-Disposition header
    )

# Streaming — for large files or real-time data
import io
def generate_csv():
    yield "id,name,price\n"
    for item in get_all_items():   # doesn't load all into memory
        yield f"{item.id},{item.name},{item.price}\n"

@app.get("/export/csv")
def export_csv():
    return StreamingResponse(
        generate_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"}
    )

# Redirect
@app.get("/old-path")
def legacy_redirect():
    return RedirectResponse(url="/new-path", status_code=301)
```

---

## 6. Security Patterns

### API Key auth

```python
from fastapi.security import APIKeyHeader
from fastapi import Security

API_KEY = "secret-key-from-env"
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@app.get("/protected/", dependencies=[Depends(verify_api_key)])
def protected_route():
    return {"data": "sensitive"}
```

### JWT Bearer token (common pattern)

```python
from jose import jwt, JWTError  # pip install 04-python-jose
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "your-secret"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(user_id)
    if not user:
        raise credentials_exception
    return user
```

---

## 7. Testing FastAPI

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1}

def test_item_not_found():
    response = client.get("/items/9999")
    assert response.status_code == 404

def test_create_item_validation_error():
    response = client.post("/items/", json={"price": -1})  # missing name, invalid price
    assert response.status_code == 422

def test_create_item():
    response = client.post("/items/", json={"name": "Widget", "price": 9.99})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Widget"
```

---

## 8. The Interview Scenario Table — FastAPI Edition

| Question | Weak answer | Strong answer |
|---|---|---|
| "How does FastAPI handle validation?" | "It uses Pydantic" | "Pydantic models are bound to route parameters via type hints — FastAPI parses the request, runs Pydantic validation, and returns a 422 with structured error details automatically if it fails. No manual validation code needed." |
| "When would you use `async def`?" | "For performance" | "Only for I/O-bound operations — DB queries, external HTTP calls. CPU-bound work or sync libraries should stay in regular `def`. Blocking calls inside `async def` freeze the event loop." |
| "How do you share logic across routes?" | "I copy it" | "Dependency injection with `Depends()`. I write the logic once — auth, DB sessions, pagination — and compose it into routes. FastAPI resolves the dependency graph, including nested dependencies." |
| "How do you structure a large FastAPI app?" | "One big main.py" | "`APIRouter` per domain (items, users, orders), each in its own module. `main.py` just calls `include_router`. Shared auth and DB deps go in a `dependencies.py`." |
| "How do you avoid leaking sensitive fields?" | "I just don't include them" | "`response_model` on the route — define a separate output schema that excludes sensitive fields. FastAPI filters the output against that schema before serializing." |

---

## ✅ Part 3 Checklist

- [ ] Can explain when `async def` helps and when it doesn't (I/O vs CPU)
- [ ] Know that blocking inside `async def` is a bug, not a feature
- [ ] Can structure a project with `APIRouter` + `include_router`
- [ ] Know how CORS middleware works and why `*` is unsafe in production
- [ ] Know the `lifespan` pattern for startup/shutdown
- [ ] Can write a basic `TestClient` test
- [ ] Can articulate the auth dependency chain (token → user → role)

---

## 🔑 FastAPI One-Page Cheat Sheet

```python
from fastapi import FastAPI, HTTPException, Depends, Query, Path, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

app = FastAPI()

# CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Pydantic model
class Item(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    tags: List[str] = []

# Dependency
def get_db():
    db = connect()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.get("/items/",          response_model=List[Item])
@app.get("/items/{id}",      response_model=Item)
@app.post("/items/",         response_model=Item, status_code=201)
@app.put("/items/{id}",      response_model=Item)
@app.patch("/items/{id}",    response_model=Item)
@app.delete("/items/{id}",   status_code=204)

# Key patterns
# raise HTTPException(status_code=404, detail="Not found")
# item.model_dump(exclude_unset=True)  ← for PATCH
# background_tasks.add_task(fn, arg)
# Depends(get_db), Depends(get_current_user)
```

---

*You're ready. Go ship something. 🚀*
