from fastapi import APIRouter

from fastapidemo.exception.customException import InsufficientStockException
from fastapidemo.routers.products import fake_db

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)

@router.post("/")
def create_order(product_id: int, quantity: int):
    stock = get_stock(product_id)
    if quantity > stock:
        raise InsufficientStockException(product_id=product_id, available=stock)
    # ... process order
    return {"order_created": True, "product_id": product_id, "quantity": quantity}


def get_stock(product_id: int) -> int:
    # Stub: fixed stock for known products, 0 for unknown ones
    return 10 if product_id in fake_db else 0