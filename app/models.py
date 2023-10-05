from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class SalesDataRequest(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    product: Optional[str] = None
    category: Optional[str] = None


class SalesDataResponse(BaseModel):
    date: datetime
    sales_amount: float
    product: str
    category: str


class InventoryStatusResponse(BaseModel):
    product: str
    category: str
    inventory_level: int
    is_low_stock: bool


class ProductRegistrationRequest(BaseModel):
    product: str
    category: str
    price: float
