import random

from fastapi import APIRouter, Depends, HTTPException

from fastapidemo.exception.customException import InvalidProductIdException
from fastapidemo.models.model import Product
# from dependencies import get_current_user
from fastapi import status

# Dictionary/Map
fake_db: dict[int, Product] = {
    101: Product(name="A", price=34.00),
    102: Product(name="B", price=34.00),
    103: Product(name="C", price=34.00, description="Product C"),
}

router = APIRouter(
    prefix="/products",  # All routes start with /products
    tags=["products"],  # Groups routes in /docs
    # dependencies=[Depends(get_current_user)],  # Applied to ALL routes in this router
    responses={404: {"description": "Not found"}},
)

@router.get("/")  # Full path: GET /products/
def list_products() -> dict:
    return fake_db

# Query Params
# /products/paged/?skip=0&limit=10
@router.get("/paged/")
def list_products_paged(start: int = 0, limit: int = 10):
    return {"from": start, "limit": limit}

@router.get("/{product_id}")  # Full path: GET /products/{product_id}
def get_product(product_id: int):
    return fake_db.get(product_id)

# {product_id} is a path parameter
#  For 'product_id': Value must be an integer.
@router.get("/detail/{product_id}")
def get_product_strict(product_id: int):  # ← type hint does the validation
    if not product_id.isdigit():
        raise InvalidProductIdException(product_id)

    if product_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found"
        )
    return {"product": fake_db[product_id]}

@router.post("/create/", status_code=status.HTTP_201_CREATED)
def create_product(product: Product) -> dict:  # FastAPI reads body, validates, and passes typed object
    id: int = random.randint(100, 999)
    # Only inserts if id is not already in fake_db; otherwise returns the existing Product
    fake_db.setdefault(id, product)
    return {"id": id, "product": fake_db[id]}

@router.post("/echo/", status_code=status.HTTP_201_CREATED)
def echo_product(product: Product):  # FastAPI reads body, validates, and passes typed object
    return {"product_name": product.name, "product_price": product.price}


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    return None  # 204 = success with no content
