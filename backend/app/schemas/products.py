from pydantic import BaseModel, Field
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.products import StockMovementTypes

class ProductBase(BaseModel):
    product_name: str = Field(..., alias = "productName", description = "Product Name")
    initial_stock: int = Field(..., alias = "initialStock", description = "Initial quantity of product in stock.")
    current_stock: int = Field(..., alias = "currentStock", description = "Current quantity of product in stock.")
    minimum_stock_level : int = Field(default=5, alias="minimumStockLevel", description="Minimum level of stock for this product.")
    reserved_stock : int = Field(alias="reservedStock")
    model_config = {
        "populate_by_name": True
        
    }


class ProductUpdate(BaseModel):
    product_name: str| None = None
    initial_stock: int | None = None
    current_stock: int | None = None
    minimum_stock_level : int | None = None

    model_config = {
        "populate_by_name": True,
        "from_attributes": True, 
        "serialize_by_alias": True,
    }

class ProductRead(BaseModel):
    product_id: int | None = Field(default=None, alias = "productId", description = "Product ID") 
    product_name: str = Field(..., alias = "productName", description = "Product Name", serialization_alias = "productName",) 
    initial_stock: int = Field(..., alias = "initialStock", serialization_alias = "initialStock", description = "Initial quantity of product in stock.") 
    current_stock: int = Field(..., alias = "currentStock", serialization_alias = "currentStock", description = "Current quantity of product in stock.") 
    minimum_stock_level : int = Field(default=5, alias="minimumStockLevel", serialization_alias="minimumStockLevel", description="Minimum level of stock for this product.")

    model_config = {
        "from_attributes": True,
        "serialize_by_alias": True,
        "populate_by_name": True,
    
    }



class StockMovementBase(BaseModel):
    movement_type: StockMovementTypes = Field(
        ...,
        alias="movementType"
    )
    quantity: int
    note: Optional[str] = None

    model_config = {
        "populate_by_name": True
    }


class StockMovementCreate(StockMovementBase):
    product_id: int = Field(
        ...,
        alias="productId"
    )

    model_config = {
        "populate_by_name": True
    }


class StockMovementRead(BaseModel):
    id: int
    product_id: int = Field(
        ...,
        alias="productId"
    )
    movement_type: StockMovementTypes = Field(
        ...,
        alias="movementType"
    )
    quantity: int
    note: Optional[str] = None
    created_at: datetime = Field(
        ...,
        alias="createdAt"
    )

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
        "serialize_by_alias": True
    }