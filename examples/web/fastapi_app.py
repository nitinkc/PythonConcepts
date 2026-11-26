from typing import Annotated

from fastapi import FastAPI, Query, status
from pydantic import BaseModel, Field

app = FastAPI(title="Python Concepts API")


class ItemIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    description: str | None = None


class ItemOut(ItemIn):
    id: int


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Python Concepts API"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int) -> ItemOut:
    return ItemOut(id=item_id, name="Example", price=9.99)


@app.get("/items")
def list_items(
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=100)] = 10,
) -> dict[str, int]:
    return {"skip": skip, "limit": limit}


@app.post("/items", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemIn) -> ItemOut:
    return ItemOut(id=1, **item.model_dump())
