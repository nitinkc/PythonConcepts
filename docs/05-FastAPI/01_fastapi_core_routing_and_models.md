# ⚡ FastAPI Boot Camp — Part 1: Core Concepts

### Path & Query Params, Request & Response Models

> **Goal:** Understand how FastAPI receives requests, validates input, and sends structured responses — the backbone of
> every API you'll build or debug.

---

## 1. What Makes FastAPI Different

Before diving in, internalize the three things that separate FastAPI from Flask/Django REST:

| Feature                 | FastAPI                   | Flask              |
|-------------------------|---------------------------|--------------------|
| Type hints = validation | ✅ Automatic via Pydantic | ❌ Manual          |
| Auto docs (Swagger UI)  | ✅ `/docs` out of the box | ❌ Needs extension |
| Async support           | ✅ Native `async/await`   | ⚠️ Limited         |
| Speed                   | ⚡ ~3× faster than Flask  | Slower             |

```python
# The minimal FastAPI app
from fastapi import FastAPI  # Pulls FastAPI class,
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}  # FastAPI auto-serializes dicts to JSON
```

Run it:

```bash
uvicorn main:app --reload   # main = filename, app = FastAPI() instance
# Visit http://127.0.0.1:8000/docs  ← free Swagger UI
```

---

## 2. Path Parameters

Values embedded directly in the URL path.

```python
from fastapi import FastAPI
app = FastAPI()

# {item_id} is a path parameter — FastAPI extracts and casts it automatically
@app.get("/items/{item_id}")
def get_item(item_id: int):  # ← type hint does the validation
    return {"item_id": item_id}

# GET /items/42   → {"item_id": 42}     ✓
# GET /items/abc  → 422 Unprocessable Entity  ← FastAPI rejects invalid type automatically
```

### Order matters — **fixed paths** BEFORE parameterized ones

```python
# ✅ CORRECT ORDER
@app.get("/users/me")  # matched first — specific
def get_current_user():
    return {"user": "current_user"}

@app.get("/users/{user_id}")  # matched second — parameterized
def get_user(user_id: int):
    return {"user_id": user_id}

# ❌ WRONG ORDER — /users/me would try to cast "me" as int → 422 error
@app.get("/users/{user_id}")  # this would catch /users/me first
@app.get("/users/me")
```

### Enum path parameters (restrict valid values)

```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    vgg = "vgg"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model": model_name, "message": "Deep Learning FTW!"}
    return {"model": model_name}

# GET /models/resnet  → valid ✓
# GET /models/bert    → 422 — not in enum ✓
```

---

## 3. Query Parameters

Key-value pairs after the `?` in the URL. Any function parameter that isn't a path parameter is treated as a query
parameter.

```python
@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

# GET /items/          → {"skip": 0, "limit": 10}   (defaults)
# GET /items/?skip=20  → {"skip": 20, "limit": 10}
# GET /items/?skip=20&limit=5  → {"skip": 20, "limit": 5}
```

### Optional query parameters

```python
from typing import Optional


@app.get("/items/{item_id}")
def get_item(item_id: int, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item["q"] = q
    if not short:
        item["description"] = "This is a long description..."
    return item

# GET /items/1                      → {"item_id": 1, "description": "..."}
# GET /items/1?q=search&short=true  → {"item_id": 1, "q": "search"}
```

> **Note:** FastAPI auto-converts `"true"`, `"1"`, `"yes"` → `True` for `bool` parameters.

### Validation with `Query()`

```python
from fastapi import Query


@app.get("/search/")
def search(
        q: str = Query(min_length=3, max_length=50, description="Search query string"),
        page: int = Query(default=1, ge=1, description="Page number, starting at 1"),
        size: int = Query(default=10, ge=1, le=100),
):
    return {"q": q, "page": page, "size": size}

# GET /search/?q=ab        → 422 — q too short (min_length=3)
# GET /search/?q=abc&page=0 → 422 — page must be >= 1
# GET /search/?q=abc       → {"q": "abc", "page": 1, "size": 10} ✓
```

---

## 4. Request Body with Pydantic Models

For POST/PUT/PATCH — structured data sent in the request body. This is where Pydantic shines.

```python
from pydantic import BaseModel
from typing import Optional


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False  # optional with default
    description: Optional[str] = None  # truly optional, can be None


@app.post("/items/")
def create_item(item: Item):  # FastAPI reads body, validates, and passes typed object
    return {"item_name": item.name, "item_price": item.price}
```

**Request body (JSON):**

```json
{
  "name": "Widget",
  "price": 9.99,
  "description": "A useful widget"
}
```

**What Pydantic does automatically:**

- Parses JSON → Python object
- Validates types (e.g., `"price": "not_a_number"` → 422 error with helpful message)
- Sets defaults for missing optional fields
- Generates the schema shown in `/docs`

### Accessing body fields

```python
@app.post("/items/{item_id}")
def update_item(item_id: int, item: Item):
    # Access fields directly as attributes
    total = item.price * 1.1  # 10% markup
    return {
        "item_id": item_id,
        "item_name": item.name,
        "price_with_tax": total
    }
```

---

## 5. Response Models — Controlling What You Return

Use `response_model` to declare the shape of the response. FastAPI will filter and validate the output.

```python
class UserIn(BaseModel):
    username: str
    email: str
    password: str  # received in request


class UserOut(BaseModel):
    username: str
    email: str
    # NO password field — it won't appear in the response


@app.post("/users/", response_model=UserOut)  # ← strips password from output
def create_user(user: UserIn):
    # Even if we return the full user object, FastAPI only outputs UserOut fields
    return user  # password is filtered out automatically ✓
```

> **Interview line:** *"I use `response_model` to decouple input schema from output schema — it's the clean way to avoid
> accidentally leaking fields like passwords or internal IDs."*

### Response status codes

```python
from fastapi import status


@app.post("/items/", status_code=status.HTTP_201_CREATED)  # 201 not 200
def create_item(item: Item):
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    return None  # 204 = success with no content
```

---

## 6. Path Parameter Validation with `Path()`

```python
from fastapi import Path


@app.get("/items/{item_id}")
def get_item(
        item_id: int = Path(ge=1, le=1000, description="Item ID between 1 and 1000"),
        q: Optional[str] = None
):
    return {"item_id": item_id}

# GET /items/0    → 422 — must be >= 1
# GET /items/500  → {"item_id": 500} ✓
```

---

## ✅ Part 1 Checklist

- [ ] Know the difference between path params, query params, and request body
- [ ] Can explain what Pydantic does in 1 sentence
- [ ] Know that type hints = automatic validation (not just documentation)
- [ ] Know to put fixed routes before parameterized routes
- [ ] Understand `response_model` as output filtering/validation
- [ ] Can use `Query()` and `Path()` for field-level constraints

---

*Next up → **Part 2: Pydantic Deep Dive, Error Handling & Dependencies***
