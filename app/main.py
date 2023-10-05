from fastapi import FastAPI, Depends
from typing import List

from .models import SalesDataRequest, SalesDataResponse, InventoryStatusResponse, ProductRegistrationRequest

app = FastAPI()


@app.get("/api/sales", response_model=List[SalesDataResponse])
async def get_sales_data(request: SalesDataRequest = Depends()):

    return []


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
