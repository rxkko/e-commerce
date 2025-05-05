from pydantic import BaseModel
from decimal import Decimal
from typing import List
from .cart import CartItemCreate 

class OrderCreate(BaseModel):
    cart_items: List[CartItemCreate]

class OrderItemResponse(BaseModel):
    product_name: str
    quantity: int
    price: Decimal

class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    created_at: str
    items: List[OrderItemResponse]

    class Config:
        orm_mode = True