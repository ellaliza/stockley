"""
Stockley FastAPI Application

Main application module that configures and runs the FastAPI server.
Handles CORS, database initialization, and router registration.
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from typing import Annotated
from app.db.session import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager
from app.models.products import *
from app.api.v1 import auth, stores

# CORS allowed origins for cross-origin requests
origins = ["http://localhost:5173",
           "https://backend.ellaliza.dev",
           "https://frontend.ellaliza.dev"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Handles startup and shutdown events. Currently only initializes
    the database tables on startup.
    """
    create_db_and_tables()
    yield


# Create FastAPI application instance
app = FastAPI(lifespan=lifespan)

# Configure CORS middleware for cross-origin requests
app.add_middleware(CORSMiddleware,
                   allow_origins = origins,
                   allow_credentials = True,
                   allow_methods = ["*"],
                   allow_headers = ["*"])

# Register API routers
app.include_router(auth.router)
app.include_router(stores.router)


@app.get("/")
def root():
    """
    Root endpoint providing basic API information.

    Returns a welcome message indicating the API is running.
    No authentication required.

    Returns:
        dict: Welcome message and API name.
    """
    return {"message":"Welcome to Stockley!"}


"""
Legacy product endpoints (commented out - to be moved to proper API structure)

These endpoints were part of the initial development but are currently
disabled pending proper API organization and testing.
""" 
@app.get("/products/", response_model=list[ProductRead], response_model_by_alias=True)
async def get_products(session: SessionDep):
    products = session.exec(select(Product)).all()
    return products

@app.get("/products/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, session: SessionDep):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Hero not found")
    return product
    
@app.post("/products/", response_model=list[ProductRead])
async def create_product(product: ProductBase, session: SessionDep, offset: int = 0, limit: int = 100):
    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    return products

@app.post("/products/bulk-create/", response_model=list[ProductRead])
async def create_bulk_products(product_list: list[ProductBase], session:SessionDep):
    for product in product_list:
        db_product = Product.model_validate(product)
        session.add(db_product)
    session.commit()
    products = session.exec(select(Product).offset(0).limit(100)).all()
    return products

@app.post("/products/stock-out/{product_id}", response_model=ProductRead)
async def sell_product(
    product_id: int,
    
    session: SessionDep,
    quantity: int = Query(default=1, ge=1),
):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.current_stock < quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    product.current_stock -= quantity
    session.add(product)
    session.commit()
    session.refresh(product)

    return product


@app.post("/products/restock/{product_id}", response_model=ProductRead)
async def restock_product(
    product_id: int,
    session: SessionDep,
    quantity: int = Query(default=1, ge=1),
    
):
    product = session.get(Product, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.current_stock += quantity
    session.add(product)
    session.commit()
    session.refresh(product)

    return product

@app.get("/api/dashboard", response_model=DashboardData)
async def get_dashboard_data(session: SessionDep):
    products = session.exec(select(Product)).all()

    total_product_count = len(products)
    low_stock_count = sum(
        1 for product in products
        if product.current_stock < product.minimum_stock_level
    )
    out_of_stock_count = sum(
        1 for product in products
        if product.current_stock == 0
    )

    return DashboardData(
        total_product_count=total_product_count,
        low_stock_count=low_stock_count,
        out_of_stock_count=out_of_stock_count
    )