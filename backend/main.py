from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost:5173",
           "https://mallie-lacklustre-deadra.ngrok-free.dev"]

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins = origins,
                   allow_credentials = True,
                   allow_methods = ["*"],
                   allow_headers = ["*"])
class Product(BaseModel):
    product_id: int = Field(..., alias = "productId", description = "Product ID")
    product_name: str = Field(..., alias = "productName", description = "Product Name")
    initial_stock: int = Field(..., alias = "initialStock", description = "Initial quantity of product in stock.")
    current_stock: int = Field(..., alias = "currentStock", description = "Current quantity of product in stock.")
    minimum_stock_level : int = Field(default=5, alias="minimumStockLevel", description="Minimum level of stock for this product.")

    model_config = {
        "populate_by_name": True
    }

class DashboardData(BaseModel):
    total_product_count: int = Field(..., alias="totalProductCount", description="Total number of available products")
    low_stock_count: int = Field(..., alias="lowStockCount", description="Number of products considered low on stock")
    out_of_stock_count: int = Field(..., alias="outOfStockCount", description="Number of products that are out of stock")

    model_config = {
        "populate_by_name": True
    }
    


products: list[Product] = []
details: Product = {
    "product_id": 100,
    "product_name": "Verna Drinking Water 500ml",
    "initial_stock": 10,
    "current_stock": 10,

}
verna = Product(**details)
products.append(verna)

@app.get("/")
def root():
    return {"message":"Welcome to Stockley!"}

@app.get("/products/")
async def get_products():
    return products



@app.get("/products/{product_id}")
async def get_product(product_id: int ):
    product_ids = [product.product_id for product in products]
    if product_id in product_ids:
        for thing in products:
            if product_id == thing.product_id:
                return thing
    else:
        raise HTTPException(status_code=404, detail=f"product {product_id} not found")
    
@app.post("/products/")
async def create_product(product: Product):
    products.append(product)
    return products

@app.post("/products/bulk-create/")
async def create_bulk_products(product_list: list[Product]):
    for product in product_list:
        products.append(product)
    return products

@app.get("/products/stock-out/{product_id}")
async def sell_product(
    product_id: int, 
    quantity: int = Query(default=1, ge=1)
    ):
    product_dict: dict = {}
    for product in products:
        product_dict.setdefault(str(product.product_id), product)
    if str(product_id) in product_dict:
        product_record: Product = product_dict.get(str(product_id), None)
        product_record.current_stock -= quantity
        return product_record
    else:
        return {"message": f"Could not record sale of {quantity} unit for product id {product_id}."}


@app.get("/products/restock/{product_id}")
async def restock_product(product_id: int, quantity: int = 1):
    product_dict: dict = {}
    for product in products:
        product_dict.setdefault(str(product.product_id), product)
    if str(product_id) in product_dict:
        product_record: Product = product_dict.get(str(product_id), None)
        product_record.current_stock += quantity
        return product_record
    else:
        return {"message": f"Could not record sale of {quantity} unit for product id {product_id}."}



@app.get("/api/dashboard")
async def get_dashboard_data() -> DashboardData:
    total_product_count = len(products)
    low_stock_count = 0
    for product in products:
        if product.current_stock < product.minimum_stock_level:
            low_stock_count += 1
    out_of_stock_count = 0
    for product in products:
        if product.current_stock == 0:
           out_of_stock_count += 1
    
    response: DashboardData = DashboardData(
        total_product_count = total_product_count, 
        low_stock_count = low_stock_count,
        out_of_stock_count = out_of_stock_count)
    return response