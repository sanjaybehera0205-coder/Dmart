from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str
    description: str
    category: str
    brand: str
    price: float
    discount_price: Optional[float] = None
    stock: int
    sku: str
    image_url: Optional[str] = None
    is_active: bool = True