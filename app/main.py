from fastapi import FastAPI, Depends
from typing import List
from sqlalchemy.orm import Session

from .database import get_db, engine
from .models import (
    SalesDataRequest,
    SalesDataResponse,
    InventoryStatusResponse,
    ProductRegistrationRequest
)

from . import schemas

schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/api/sales")
async def get_sales_data(
    db: Session = Depends(get_db),
    request: SalesDataRequest = Depends()
):

    query = db.query(schemas.Sales)
    return request.model_dump()


@app.get("/api/sales/revenue", response_model=List[SalesDataResponse])
async def analyze_revenue(request: SalesDataRequest = Depends()):
    return []


@app.get("/api/inventory", response_model=List[InventoryStatusResponse])
async def get_inventory_status():
    return []


@app.put("/api/inventory/{product}", response_model=InventoryStatusResponse)
async def update_inventory(product: str, quantity: int):
    return []


@app.post("/api/products", response_model=ProductRegistrationRequest)
async def register_product(product_request: ProductRegistrationRequest):
    return []

# uvicorn app.main:app
