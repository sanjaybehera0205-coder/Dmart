from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    subtotal: float


class CreateOrder(BaseModel):
    user_id: str


class Order(BaseModel):
    order_id: str
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: str
    created_at: datetime
