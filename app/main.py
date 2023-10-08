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


@app.get("/api/sales", response_model=list[SalesDataResponse])
async def get_sales_data(
    db: Session = Depends(get_db),
    request: SalesDataRequest = Depends()
):

    query = db.query(
        schemas.Sales.id,
        schemas.Sales.user_id,
        schemas.SaleItems.created_at.label('transaction_timestamp'),
        schemas.Products.name.label('product_name'),
        schemas.Products.description,
        schemas.ProductCategory.name.label('category_name'),
        schemas.Products.price,
        schemas.SaleItems.quantity
    ).join(
        schemas.SaleItems, schemas.SaleItems.sale_id == schemas.Sales.id, isouter=True
    ).join(
        schemas.Products, schemas.Products.id == schemas.SaleItems.product_id, isouter=True
    ).join(
        schemas.ProductCategory,
        schemas.ProductCategory.id == schemas.Products.category_id, isouter=True
    ).limit(request.limit).offset(request.offset)

    print(query)

    return query.all()


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
