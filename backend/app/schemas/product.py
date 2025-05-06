from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    quantity: int
    category_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    quantity: int
    category_id: int
    image_url: Optional[str] = None

    class Config:
        orm_mode = True