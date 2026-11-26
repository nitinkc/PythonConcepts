from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field

# Input Schema
class Product(BaseModel):
    name: str
    price: float = Field(gt=0, description="Must be positive") # Field level Validation
    description: Optional[str] = None  # truly optional, can be None

# Output Schema
class ItemOut(BaseModel):
    name: str
    price: float
    sku: Optional[str] = Field(default=None, pattern=r"^[A-Z]{3}-\d{4}$")
    # sku must match pattern like "ABC-1234" if provided

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    vgg = "vgg"

