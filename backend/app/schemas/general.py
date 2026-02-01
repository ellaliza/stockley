from pydantic import BaseModel, Field

class DashboardData(BaseModel):
    total_product_count: int = Field(..., alias="totalProductCount", description="Total number of available products")
    low_stock_count: int = Field(..., alias="lowStockCount", description="Number of products considered low on stock")
    out_of_stock_count: int = Field(..., alias="outOfStockCount", description="Number of products that are out of stock")

    model_config = {
        "populate_by_name": True,
    }
    