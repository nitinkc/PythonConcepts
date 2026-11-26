
## Route Shadowing

In FastAPI,  does this code gves an error or runs without issues. what would be printed?
```python
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/")
def read_root():
    return {"status": "ok"}
```

In FastAPI, routes are stored on app.routes (and on APIRouter.routes), so you can inspect registered routes at startup or after route registration to catch duplicate (path, method) pairs.

Use a lifespan handler on FastAPI to scan app.routes once all routes are attached and raise an error if a (path, method) combination appears more than once:

Solution

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    assert_no_duplicate_routes(app)
    yield


app = FastAPI(lifespan=lifespan)
```

When a Validation occurs, does it throw and exceotuon or Error
- Is it 422 Validation Exception 
- Or an error even before 422

```shell
curl -X 'GET' \
  'http://localhost:8001/products/detail/101' \
  -H 'accept: */*'
```


```python
@router.get("/detail/{product_id}")
def get_product_strict(product_id: int):  # ← type hint does the validation
    if not product_id.isdigit():
        raise InvalidProductIdException(product_id)
    # continue as usual

# Define the custom exception Name
class InvalidProductIdException(Exception):
    def __init__(self, raw_id) -> None:
        self.raw_id = raw_id

# Exception Handler
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

