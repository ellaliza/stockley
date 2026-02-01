from sqlmodel import Field as SQLField, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from enum import Enum
from datetime import datetime

if TYPE_CHECKING:
    from .stores import Store


class Product(SQLModel, table=True):
    product_id: Optional[int] = SQLField(
        default=None,
        primary_key=True,
        alias="productId"
    )

    product_name: str
    initial_stock: int
    current_stock: int
    minimum_stock_level: int = SQLField(default=5)
    reserved_stock: int = SQLField(default=0)

    store_id: int = SQLField(foreign_key="store.id")

    store: Optional["Store"] = Relationship(back_populates="products")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
    }


class StockMovementTypes(str, Enum):
    IN = "stock_in"
    OUT = "stock_out"
    RESERVE = "reserve_stock"


class StockMovement(SQLModel, table=True):
    id: Optional[int] = SQLField(default=None, primary_key=True)

    product_id: int = SQLField(foreign_key="product.product_id")

    movement_type: StockMovementTypes
    quantity: int
    note: Optional[str] = None
    created_at: datetime = SQLField(default_factory=datetime.now)
