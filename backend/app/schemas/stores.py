"""
Store Pydantic schemas for API request/response validation.

This module defines Pydantic models for store-related API operations,
including creation, reading, and different response formats with relationships.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING
if TYPE_CHECKING:
    from .users import StoreMemberReadWithoutStore
    from .products import ProductRead

class StoreBase(BaseModel):
    """Base schema for store data with common fields."""
    name: str
    description: Optional[str]
    location: Optional[str]


class StoreCreate(StoreBase):
    """Schema for creating new stores. Inherits all fields from StoreBase."""
    pass


class StoreRead(StoreBase):
    """Schema for reading store data with ID."""
    id: Optional[int] = Field(default=None)

    model_config = {"from_attributes": True}


class StoreReadWithProducts(StoreRead):
    """Schema for reading stores with their associated products."""
    products: List["ProductRead"] = Field(default_factory=list)
    model_config = {"from_attributes": True}

class StoreReadWithMembers(StoreRead):
    """Schema for reading stores with their member information."""
    members: List["StoreMemberReadWithoutStore"] = Field(default_factory=list)
    model_config = {"from_attributes": True}


class StoreReadWithProductsAndMembers(StoreReadWithMembers):
    """Schema for reading stores with both products and members."""
    products: List["ProductRead"] = Field(default_factory=list)
    model_config = {"from_attributes": True}

# Runtime imports for forward references to avoid circular imports
from .products import ProductRead
from .users import StoreMemberReadWithoutStore

# Rebuild models to resolve forward references
StoreReadWithProducts.model_rebuild()
StoreReadWithMembers.model_rebuild()
StoreReadWithProductsAndMembers.model_rebuild()
