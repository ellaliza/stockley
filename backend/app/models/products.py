"""Product domain models using SQLModel for ORM and Pydantic validation.

This module defines the `Product` and `StockMovement` tables, which
together handle inventory tracking and audit logs. Each product belongs
to a store and may have many stock movements (buy, sell, reserve, etc.).
"""

from sqlmodel import Field as SQLField, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING, List
from enum import Enum
from datetime import datetime

if TYPE_CHECKING:
    from .stores import Store


class Product(SQLModel, table=True):
    """Product inventory record.

    Each product is scoped to a store. The `current_stock`, `initial_stock`,
    `minimum_stock_level`, and `reserved_stock` fields are used for
    inventory management. Movements are tracked via the `movements`
    relationship for full audit trail.

    Fields:
    - `product_id`: auto-incrementing primary key
    - `product_name`: human-readable product name
    - `initial_stock`: quantity when the product was created
    - `current_stock`: current available quantity
    - `minimum_stock_level`: low-stock threshold (default: 5)
    - `reserved_stock`: quantity reserved for pending orders (default: 0)
    - `store_id`: foreign key to the store this product belongs to
    """

    product_id: Optional[int] = SQLField(
        default=None,
        primary_key=True,
        alias="productId",
    )

    product_name: str
    initial_stock: int
    current_stock: int
    minimum_stock_level: int = SQLField(default=5)
    reserved_stock: int = SQLField(default=0)

    # Foreign key to the store this product belongs to
    store_id: int = SQLField(foreign_key="store.id")

    # Relationships for lazy-loading related records
    store: Optional["Store"] = Relationship(back_populates="products")
    movements: List["StockMovement"] = Relationship(back_populates="product")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
    }


class StockMovementTypes(str, Enum):
    """Enumeration of stock movement types for audit trail.

    - `IN`: stock increase (purchase, restock)
    - `OUT`: stock decrease (sale, damage, loss)
    - `RESERVE`: stock reserved for a pending order
    """

    IN = "stock_in"
    OUT = "stock_out"
    RESERVE = "reserve_stock"


class StockMovement(SQLModel, table=True):
    """Audit log entry for product stock changes.

    Each movement records a quantity change and the reason (movement_type).
    Movements create a complete history of stock activity for compliance
    and debugging.

    Fields:
    - `id`: auto-incrementing primary key
    - `product_id`: foreign key to the product
    - `movement_type`: type of movement (IN, OUT, RESERVE)
    - `quantity`: amount changed
    - `note`: optional human-readable reason (e.g., "Initial Stock of Widget")
    - `created_at`: timestamp of movement (auto-set to now)
    """

    id: Optional[int] = SQLField(default=None, primary_key=True)

    # Foreign key to the product this movement affects
    product_id: int = SQLField(foreign_key="product.product_id")

    movement_type: StockMovementTypes
    quantity: int
    note: Optional[str] = None
    # Auto-populated with current UTC time on creation
    created_at: datetime = SQLField(default_factory=datetime.now)

    # Relationship to the parent product
    product: Optional["Product"] = Relationship(back_populates="movements")