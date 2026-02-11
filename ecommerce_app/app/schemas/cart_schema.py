from pydantic import BaseModel
from typing import List
from datetime import datetime


class CartItem(BaseModel):
    product_id: str
    quantity: int


class AddToCart(BaseModel):
    user_id: str
    product_id: str
    quantity: int


class Cart(BaseModel):
    user_id: str
    items: List[CartItem]
    total_amount: float
    created_at: datetime
    updated_at: datetime
