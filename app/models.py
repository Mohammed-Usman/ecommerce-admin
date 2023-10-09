from typing import Optional
from pydantic import BaseModel, validator
from sqlalchemy import and_, or_

from datetime import datetime
import pytz


class DateFilter(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None

    @validator("start_date", "end_date")
    def validate_and_convert_to_utc(cls, value):
        try:

            if value is None:
                return None
            # Parse the datetime string
            dt = datetime.fromisoformat('+'.join(value.split(' ')))

            # Ensure the parsed datetime is in UTC
            if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
                raise ValueError(
                    "Datetime string should include timezone information")

            # Convert the datetime to UTC using pytz
            utc_timezone = pytz.UTC
            dt_utc = dt.astimezone(utc_timezone)

            return dt_utc
        except ValueError:
            raise ValueError("Invalid ISO datetime format")


class LimitOffset(BaseModel):
    limit: Optional[int] = 10
    offset: Optional[int] = 0


class SalesDataRequest(DateFilter):

    product: Optional[str] = None
    category: Optional[str] = None


class SalesDataResponse(BaseModel):
    id: int
    user_id: int
    transaction_timestamp: datetime
    product_name: str
    description: str
    category_name: str
    price: float
    quantity: int

    class Config:
        from_attributes = True


class Revenue(BaseModel):
    total_revenue: float


class InventoryStatusResponse(BaseModel):
    product_name: str
    product_description: str
    category_name: str
    category_description: str
    product_price: float
    inventory_quantity: int
    last_updated_at: datetime


class ProductRegistrationRequest(BaseModel):
    product: str
    product_description: Optional[str] = None
    category: str
    category_description: Optional[str] = None
    price: float
    quantity: int
