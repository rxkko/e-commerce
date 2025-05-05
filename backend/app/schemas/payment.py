from decimal import Decimal
from pydantic import BaseModel

class PaymentRequest(BaseModel):
    order_id: int
    amount: Decimal
    currency: str = "USD"

class PaymentResponse(BaseModel):
    success: bool
    payment_url: str

    class Config:
        orm_mode = True