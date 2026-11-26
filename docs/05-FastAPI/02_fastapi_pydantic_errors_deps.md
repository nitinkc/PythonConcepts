# ⚡ FastAPI Boot Camp — Part 2: Pydantic, Error Handling & Dependencies

### Validation, Custom Errors & Dependency Injection

> **Goal:** Go beyond basic models. Know how to validate complex data, raise meaningful errors, and share logic cleanly
> across routes using dependency injection.

---

## 1. Pydantic Deep Dive **[FDE]**

!!! note "Pydantic V2"
    Everything here uses the **V2 API** — the version interviewers probe. Know the renames cold:

    | V1 (legacy) | V2 (current) |
    |:-----|:---|
    | `@validator("field")` | `@field_validator("field")` |
    | `@root_validator` | `@model_validator(mode="before"/"after")` |
    | `.dict()` / `.json()` | `.model_dump()` / `.model_dump_json()` |
    | `.parse_obj(data)` | `.model_validate(data)` |
    | `class Config:` | `model_config = ConfigDict(...)` |

    V2's validation core is written in Rust (`pydantic-core`), so models are ~5–20x faster than V1 — a useful "why it matters" detail.


### Field-level validation with `Field()`

```python
from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Product name")
    price: float = Field(gt=0, description="Must be positive")
    stock: int = Field(ge=0, default=0, description="Cannot be negative")
    sku: Optional[str] = Field(default=None, pattern=r"^[A-Z]{3}-\d{4}$")
    # sku must match pattern like "ABC-1234" if provided

# Valid:   Product(name="Widget", price=9.99, sku="WDG-0001")
# Invalid: Product(name="Widget", price=-1)  → validation error: price must be > 0
```

### Validators — custom logic on fields

```python
from pydantic import BaseModel, field_validator, model_validator


class Order(BaseModel):
    username: str
    quantity: int
    discount: float = 0.0

    @field_validator("username")
    @classmethod
    def username_must_be_lowercase(cls, v):
        if v != v.lower():
            raise ValueError("username must be lowercase")
        return v

    @field_validator("discount")
    @classmethod
    def discount_must_be_valid(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("discount must be between 0 and 1")
        return v

    # Cross-field validation (both fields available)
    @model_validator(mode="after")
    def check_bulk_discount(self):
        if self.quantity < 10 and self.discount > 0.2:
            raise ValueError("Discount over 20% only available for orders of 10+")
        return self
```

### Nested models

```python
from typing import List


class Address(BaseModel):
    street: str
    city: str
    zip_code: str = Field(pattern=r"^\d{5}$")


class Customer(BaseModel):
    name: str
    email: str
    address: Address  # nested model — 05-FastAPI handles the nested JSON automatically
    tags: List[str] = []  # list of strings

# Request body:
# {
#   "name": "Alice",
#   "email": "alice@example.com",
#   "address": {"street": "123 Main St", "city": "Seattle", "zip_code": "98101"},
#   "tags": ["vip", "wholesale"]
# }
```

### `model_dump()` and `model_dump(exclude_unset=True)`

```python
@app.patch("/items/{item_id}")
def partial_update(item_id: int, item: Item):
    # exclude_unset=True — only fields the client actually sent
    # This is critical for PATCH endpoints (partial update)
    update_data = item.model_dump(exclude_unset=True)

    # Now update_data only has the fields that were included in the request
    # If client sent {"price": 19.99}, update_data = {"price": 19.99}
    # NOT {"price": 19.99, "name": None, "description": None}
    existing_item = get_item_from_db(item_id)
    updated = existing_item.model_copy(update=update_data)
    return updated
```

> **Interview line:** *"For PATCH endpoints, I always use `exclude_unset=True` — otherwise default values overwrite
> fields the client didn't intend to change."*

---

## 2. Error Handling

### Raising HTTP exceptions

```python
from fastapi import FastAPI, HTTPException, status

fake_db = {1: "Widget", 2: "Gadget"}


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    return {"item": fake_db[item_id]}

# GET /items/99 → 404 {"detail": "Item 99 not found"}
```

### Custom exception handlers — app-wide error handling

```python
from fastapi import Request
from fastapi.responses import JSONResponse


class InsufficientStockError(Exception):
    def __init__(self, item_id: int, available: int):
        self.item_id = item_id
        self.available = available


@app.exception_handler(InsufficientStockError)
async def stock_exception_handler(request: Request, exc: InsufficientStockError):
    return JSONResponse(
        status_code=409,  # Conflict
        content={
            "error": "insufficient_stock",
            "item_id": exc.item_id,
            "available": exc.available,
            "message": f"Only {exc.available} units available"
        }
    )


@app.post("/orders/")
def create_order(item_id: int, quantity: int):
    stock = get_stock(item_id)
    if quantity > stock:
        raise InsufficientStockError(item_id=item_id, available=stock)
    # ... process order
```

### Overriding the default validation error handler

```python
from fastapi.exceptions import RequestValidationError


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Custom format for 422 errors — useful for client-friendly error messages
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " → ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    return JSONResponse(status_code=422, content={"validation_errors": errors})
```

---

## 3. Dependency Injection

FastAPI's `Depends()` is one of its most powerful features. Use it to share logic across routes without repetition.

### Simple dependency — common query params

```python
from fastapi import Depends


# Define reusable logic as a function
def pagination_params(skip: int = 0, limit: int = Query(default=10, le=100)):
    return {"skip": skip, "limit": limit}


# Inject into any route
@app.get("/items/")
def list_items(pagination: dict = Depends(pagination_params)):
    return {"pagination": pagination, "items": get_items(**pagination)}


@app.get("/users/")
def list_users(pagination: dict = Depends(pagination_params)):
    return {"pagination": pagination, "users": get_users(**pagination)}

# Both routes get ?skip= and ?limit= validation for free
```

### Class-based dependencies

```python
class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
def list_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    # Shorthand: Depends() with no args infers the class
    # commons.q, commons.skip, commons.limit are all available
    return {"q": commons.q, "skip": commons.skip}
```

### Authentication dependency — the real-world pattern

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)  # your token validation logic
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_admin(current_user=Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


# Protect specific routes
@app.get("/admin/stats")
def admin_stats(admin=Depends(require_admin)):  # chains: token → user → admin check
    return get_stats()


@app.get("/profile")
def my_profile(user=Depends(get_current_user)):  # only needs auth, not admin
    return user
```

> **Interview line:** *"Dependency injection in FastAPI lets me write auth, pagination, and DB session logic once and
> compose it across routes — no decorators, no middleware spaghetti."*

### Database session dependency — the standard pattern

```python
from sqlalchemy.orm import Session
from database import SessionLocal  # your DB setup


def get_db():
    db = SessionLocal()
    try:
        yield db  # generator — gives db to route, then runs cleanup
    finally:
        db.close()  # always closes, even on exception


@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item
```

---

## 4. Background Tasks

Run work after returning the response — useful for sending emails, logging, etc.

```python
from fastapi import BackgroundTasks


def send_notification_email(email: str, message: str):
    # Simulating a slow operation (email sending)
    time.sleep(2)
    print(f"Email sent to {email}: {message}")


@app.post("/users/{user_id}/notify")
def notify_user(
        user_id: int,
        background_tasks: BackgroundTasks
):
    user = get_user(user_id)
    background_tasks.add_task(
        send_notification_email,
        email=user.email,
        message="Your order has shipped!"
    )
    return {"message": "Notification queued"}  # Returns immediately, email sends after
```

---

## ✅ Part 2 Checklist

- [ ] Can add field validation with `Field(gt=, min_length=, pattern=)`
- [ ] Know `@field_validator` for single-field logic and `@model_validator` for cross-field
- [ ] Know `exclude_unset=True` for PATCH endpoints — can explain why it matters
- [ ] Can raise `HTTPException` with correct status codes
- [ ] Can write a custom `@app.exception_handler`
- [ ] Understand `Depends()` — can write a reusable auth dependency
- [ ] Know the `yield` DB session pattern — why `finally` matters there

---

*Next up → **Part 3: Async, Middleware, Routers & Production Patterns***
