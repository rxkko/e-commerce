from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime, func

from .base import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=func.now())