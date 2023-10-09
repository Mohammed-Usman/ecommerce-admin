from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import get_db, engine
from .models import (
    SalesDataRequest,
    SalesDataResponse,
    InventoryStatusResponse,
    ProductRegistrationRequest,
    Revenue,
    LimitOffset
)

from . import schemas

schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/api/sales", response_model=list[SalesDataResponse])
async def get_sales_data(
    db: Session = Depends(get_db),
    request_filter: SalesDataRequest = Depends(),
    limiting: LimitOffset = Depends()
):

    filters = []
    if request_filter.start_date:
        filters.append(schemas.Sales.created_at >= request_filter.start_date)
    if request_filter.end_date:
        filters.append(schemas.Sales.created_at <= request_filter.end_date)
    if request_filter.category:
        filters.append(schemas.ProductCategory.name == request_filter.category)
    if request_filter.product:
        filters.append(schemas.Products.name == request_filter.product)

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
        schemas.SaleItems, schemas.SaleItems.sale_id == schemas.Sales.id
    ).join(
        schemas.Products, schemas.Products.id == schemas.SaleItems.product_id
    ).join(
        schemas.ProductCategory,
        schemas.ProductCategory.id == schemas.Products.category_id
    ).filter(*filters).limit(limiting.limit).offset(limiting.offset)

    result = query.all()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not available"
        )

    return result


@app.get("/api/sales/revenue", response_model=Revenue)
async def analyze_revenue(
    db: Session = Depends(get_db),
    request_filter: SalesDataRequest = Depends()
):

    filters = []
    if request_filter.start_date:
        filters.append(schemas.Sales.created_at >= request_filter.start_date)
    if request_filter.end_date:
        filters.append(schemas.Sales.created_at <= request_filter.end_date)
    if request_filter.category:
        filters.append(schemas.ProductCategory.name == request_filter.category)
    if request_filter.product:
        filters.append(schemas.Products.name == request_filter.product)

    query = db.query(
        func.sum(schemas.Sales.total).label('total_revenue')
    ).join(
        schemas.SaleItems, schemas.SaleItems.sale_id == schemas.Sales.id
    ).join(
        schemas.Products, schemas.Products.id == schemas.SaleItems.product_id
    ).join(
        schemas.ProductCategory,
        schemas.ProductCategory.id == schemas.Products.category_id
    ).filter(*filters).first()

    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not available"
        )

    return query


@app.get("/api/inventory", response_model=List[InventoryStatusResponse])
async def get_inventory_status(
    db: Session = Depends(get_db),
    request_filter: SalesDataRequest = Depends(),
    limiting: LimitOffset = Depends()
):

    filters = []
    if request_filter.category:
        filters.append(schemas.ProductCategory.name == request_filter.category)
    if request_filter.product:
        filters.append(schemas.Products.name == request_filter.product)

    query = db.query(
        schemas.Products.name.label('product_name'),
        schemas.Products.description.label('product_description'),
        schemas.ProductCategory.name.label('category_name'),
        schemas.ProductCategory.description.label('category_description'),
        schemas.Products.price.label('product_price'),
        schemas.Inventory.quantity.label('inventory_quantity'),
        schemas.Inventory.updated_at.label("last_updated_at")
    ).join(
        schemas.ProductCategory,
        schemas.ProductCategory.id == schemas.Products.category_id
    ).join(
        schemas.Inventory,
        schemas.Inventory.id == schemas.Products.inventory_id
    ).filter(*filters).limit(limiting.limit).offset(limiting.offset).all()

    if not query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data not available"
        )

    return query


@app.post("/api/products", status_code=status.HTTP_201_CREATED)
async def register_product(
    product_request: ProductRegistrationRequest,
    db: Session = Depends(get_db)
):

    category = db.query(schemas.ProductCategory).filter(
        schemas.ProductCategory.name == product_request.category
    ).first()

    product = db.query(schemas.Products).filter(
        schemas.Products.name == product_request.product
    ).first()

    if product:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Product with name : {product_request.product} already exists"
                            )

    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with name : {product_request.category} not found"
                            )

    inventory = schemas.Inventory(quantity=product_request.quantity)

    db.add(inventory)

    db.commit()

    db.refresh(inventory)

    product = schemas.Products(
        name=product_request.product,
        price=product_request.price,
        category_id=category.id,
        inventory_id=inventory.id)

    db.add(product)
    db.commit()
    db.refresh(product)

    return product_request

# uvicorn app.main:app
