from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapidemo.main import app
from fastapi import status

class InsufficientStockException(Exception):
    def __init__(self, product_id: int, available: int):
        self.product_id = product_id
        self.available = available

@app.exception_handler(InsufficientStockException)
async def stock_exception_handler(request: Request, exc: InsufficientStockException):
    return JSONResponse(
        status_code=409,  # Conflict
        content={
            "error": "insufficient_stock",
            "product_id": exc.product_id,
            "available": exc.available,
            "message": f"Only {exc.available} units available"
        }
    )

class InvalidProductIdException(Exception):
    def __init__(self, raw_id) -> None:
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

#### GENERAL EXCEPTION ####
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
