"""
Store database models.

This module defines the SQLModel database models for stores and their relationships.
"""

from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .users import StoreMember
    from .products import Product


class Store(SQLModel, table=True):
    """
    Store model representing a physical or logical store/warehouse.

    A store can have multiple members with different roles and contains products.
    The creator of a store automatically becomes its owner.
    """
    id: Optional[int] = Field(default=None, primary_key=True)

    # Basic store information
    name: str
    description: Optional[str]
    location: Optional[str]

    # Relationships
    members: List["StoreMember"] = Relationship(
        back_populates="store",
    )

    products: List["Product"] = Relationship(
        back_populates="store"
    )
