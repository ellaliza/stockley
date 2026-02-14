"""Product request/response schemas.

This module uses Pydantic `BaseModel` for request validation and
serialization. Field aliases are used to provide camelCase keys in
JSON while the Python model attributes stay snake_case.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.products import StockMovementTypes


class ProductBase(BaseModel):
    """Base product fields shared by create/read/update schemas.

    - `sku`: unique stock keeping unit identifier (auto-generated)
    - `product_name` (alias: `productName`): human readable name
    - `initial_stock` (alias: `initialStock`): quantity when product was created
    - `current_stock` (alias: `currentStock`): current available quantity
    - `minimum_stock_level` (alias: `minimumStockLevel`): low-stock threshold
    - `reserved_stock` (alias: `reservedStock`): quantity reserved for pending orders
    """
    sku : Optional[str] = Field(default=None, description="SKU")
    product_name: str = Field(..., alias="productName", description="Product Name")
    initial_stock: int = Field(..., alias="initialStock", description="Initial quantity of product in stock.")
    current_stock: int = Field(..., alias="currentStock", description="Current quantity of product in stock.")
    minimum_stock_level: int = Field(default=5, alias="minimumStockLevel", description="Minimum level of stock for this product.")
    reserved_stock: Optional[int] = Field(default=0, alias="reservedStock")

    # Allow model creation from attribute-accessible ORM objects
    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    """Schema used when updating a product.

    All fields are optional except `store_id` which is required to
    ensure updates are scoped to a store. Use `exclude_unset` when
    serializing updates to avoid overwriting unspecified fields.
    """

    product_id: int | None = None
    product_name: str | None = None
    initial_stock: int | None = None
    current_stock: int | None = None
    minimum_stock_level: int | None = None
    store_id: int

    model_config = ConfigDict(
        validate_by_alias=True,
        validate_by_name=True,
        from_attributes=True,
        serialize_by_alias=True,
    )


class ProductCreate(ProductBase):
    """Request body for creating a new product.

    `store_id` is required and provided as `storeId` in JSON.
    """

    store_id: int = Field(..., alias="storeId", description="Store the product belongs to.")

    model_config = ConfigDict(validate_by_alias=True)


class ProductRead(ProductBase):
    """Product representation returned by the API.

    Includes `product_id` (alias: `productId`) and uses alias
    serialization so responses are camelCase.
    """

    product_id: int | None = Field(default=None, alias="productId", description="Product ID")

    model_config = ConfigDict(from_attributes=True, serialize_by_alias=True, validate_by_alias=True, validate_by_name=True)


class StockMovementBase(BaseModel):
    """Base fields for stock movement operations.

    `movement_type` uses the `StockMovementTypes` enum from the models
    to ensure consistency between code and persisted values.
    """

    movement_type: StockMovementTypes = Field(..., alias="movementType")
    quantity: int
    note: Optional[str] = None

    model_config = ConfigDict(validate_by_name=True)


class StockMovementCreate(StockMovementBase):
    """Request body for creating a stock movement entry.

    Includes `product_id` (alias: `productId`) so the movement is
    associated with the correct product.
    """

    product_id: int = Field(..., alias="productId")
    model_config = ConfigDict(validate_by_alias=True)


class StockMovementRead(BaseModel):
    """Stock movement representation returned by the API."""

    id: int
    product_id: int = Field(..., alias="productId")
    movement_type: StockMovementTypes = Field(..., alias="movementType")
    quantity: int
    note: Optional[str] = None
    created_at: datetime = Field(..., alias="createdAt")

    model_config = ConfigDict(from_attributes=True, validate_by_name=True, serialize_by_alias=True)


class ProductBulkCreate(BaseModel):
    """Bulk-create request when adding multiple products to a store.

    JSON shape:
    {
      "products": [ { ProductBase }, ... ],
      "storeId": 1
    }
    """

    products: List[ProductBase]
    store_id: int = Field(..., alias="storeId")

    model_config = ConfigDict(from_attributes=True, validate_by_alias=True)


class ProductReadWithStockMovement(ProductRead):
    """Extended product read model including stock movement history."""

    movements: List["StockMovementRead"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)