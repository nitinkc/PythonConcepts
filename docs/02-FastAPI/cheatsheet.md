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


# Routes, if used in the main.py
@app.get("/items/", response_model=List[Item])
@app.get("/items/{id}", response_model=Item)
@app.post("/items/", response_model=Item, status_code=201)
@app.put("/items/{id}", response_model=Item)
@app.patch("/items/{id}", response_model=Item)
@app.delete("/items/{id}", status_code=204)

# Key patterns
# raise HTTPException(status_code=404, detail="Not found")
# item.model_dump(exclude_unset=True)  ← for PATCH
# background_tasks.add_task(fn, arg)
# Depends(get_db), Depends(get_current_user)
```

## Project settings
- [project.scripts] - Console script - runs `__init__.py`
- [tool.fastapi] entrypoint in pyproject.toml- runs `main.py`

**Use `fastapi dev `to run the API**: Keep `uv run fastapi dev ... --port 8001 `

(or uv run fastapi run ... --port 8001 for non-reload mode) for serving the FastAPI app,
and reserve [project.scripts] for **custom CLI tasks** or scripts you explicitly want to run.

## Api Router
Define the routers
```python
# routers/product.py
router = APIRouter(
    prefix="/products",  # All routes start with /products
    tags=["products"],  # Groups routes in /docs
    responses={404: {"description": "Not found"}},
)
```

Register the routes in the main.py
```python
# main.py
from fastapi import FastAPI
app = FastAPI()
app.include_router(products.router, prefix="/v2")
```

Define the route
```python
@router.post("/")
def create_order(product_id: int, quantity: int):
    stock = get_stock(product_id)
    if quantity > stock:
        raise InsufficientStockException(product_id=product_id, available=stock)
    # ... process order
    return {"order_created": True, "product_id": product_id, "quantity": quantity}
```

## LifeSpan

Command line runner before server comes up 
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Modern approach
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: runs before the app starts serving requests
    print("LIFESPAN : ############ Starting up... ############")

    yield  # ← app runs here

    # SHUTDOWN: runs when the app is stopping
    print("LIFESPAN : ############ Shutting down... ############")
```

Get the LifeCycle code from the module
```python
from fastapidemo.events.lifeCycleEvents import lifespan

app = FastAPI(lifespan=lifespan)
```

## Exceptions
Define the exception class and its corresponding handler. All runtime exceptions inherit from Python's built-in 
`BaseException` (and application exceptions normally inherit from `Exception`).

```python
class InvalidProductIdException(Exception):
    def __init__(self, raw_id) -> None: # Define the params
        self.raw_id = raw_id

# Register on your FastAPI app instance
@app.exception_handler(InvalidProductIdException)
async def invalid_product_id_handler(request: Request, exc: InvalidProductIdException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "INVALID_PRODUCT_ID",
            "detail": f"Product ID '{exc.raw_id}' must be a positive integer.",
        },
    )

```

