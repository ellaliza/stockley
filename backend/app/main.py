from fastapi import FastAPI, HTTPException, Query, Depends
from typing import Annotated
from app.db.session import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager
from app.models.products import *
from app.api.v1 import auth

origins = ["http://localhost:5173",
           "https://backend.ellaliza.dev",
           "https://frontend.ellaliza.dev"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware,
                   allow_origins = origins,
                   allow_credentials = True,
                   allow_methods = ["*"],
                   allow_headers = ["*"])

app.include_router(auth.router)






@app.get("/")
def root():
    return {"message":"Welcome to Stockley!"}


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
 """