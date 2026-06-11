from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/items/")
def list_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}

@app.get("/items/{item_id}")
def get_item(item_id: int):   # ← type hint does the validation
    return {"item_id": item_id}


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False           # optional with default
    description: Optional[str] = None  # truly optional, can be None

@app.post("/items/")
def create_item(item: Item):          # 05-FastAPI reads body, validates, and passes typed object
    return {"item_name": item.name, "item_price": item.price}

class UserIn(BaseModel):
    username: str
    email: str
    password: str           # received in request

class UserOut(BaseModel):
    username: str
    email: str
    # NO password field — it won't appear in the response

@app.post("/users/", response_model=UserOut)  # ← strips password from output
def create_user(user: UserIn):
    # Even if we return the full user object, 05-FastAPI only outputs UserOut fields
    return user   # password is filtered out automatically ✓
