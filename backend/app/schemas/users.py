"""
User and store member Pydantic schemas for API validation.

This module defines Pydantic models for user-related API operations,
including registration, profile management, and store membership data.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, TYPE_CHECKING
from fastapi import Form
if TYPE_CHECKING:
    from .stores import StoreRead

class UserBase(BaseModel):
    """Base schema for user data with common fields."""
    full_name: str = Field(alias="fullName")
    email: str = Field(index = True, unique= True)
    role: str = Field(default="regular")
    username: str = Field()


class UserCreate(UserBase):
    """Schema for creating new users, includes password."""
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        email: str = Form(...),
        full_name: str = Form(..., alias="fullName"),
        password: str = Form(...)
    ):
        """Create UserCreate instance from form data for registration."""
        return cls(
            username=username,
            email=email,
            full_name=full_name,
            password=password,
        )

    model_config = ConfigDict(validate_by_alias=True, validate_by_name=True)


class UserRead(UserBase):
    """Schema for reading user data with system-generated fields."""
    id: int
    created_at: datetime = Field(..., alias="createdAt")
    
    model_config = ConfigDict(serialize_by_alias=True, validate_by_name=True, validate_by_alias=True, from_attributes=True)

class StoreMemberBase(BaseModel):
    """Base schema for store membership data."""
    role: str
    user_id : int = Field(foreign_key="user.id", alias="userId")


class StoreMemberRead(StoreMemberBase):
    """Schema for reading complete store membership data with user and store info."""
    id: int
    created_at: datetime = Field(..., alias="createdAt")
    user: UserRead
    store: StoreRead
    model_config = ConfigDict(from_attributes=True, validate_by_name=True, serialize_by_alias = True)

class UserReadWithStoreMemberships(UserBase):
    """Schema for reading user data (currently unused, for future expansion)."""
    id: int
    created_at: datetime = Field(..., alias="createdAt")
    store_memberships: StoreMemberRead
    model_config = ConfigDict(from_attributes=True, serialize_by_alias=True, validate_by_name=True)





class StoreMemberReadWithoutStore(StoreMemberBase):
    """Schema for reading store membership data without store details (to avoid circular refs)."""
    id: int
    created_at: datetime = Field(..., alias="createdAt")
    user: UserRead
    model_config = ConfigDict(from_attributes=True, serialize_by_alias=True, validate_by_name=True)

class StoreMemberWrite(StoreMemberBase):
    """Schema for creating/updating store memberships."""
    pass

# Runtime import to resolve forward references
from .stores import StoreRead
StoreMemberRead.model_rebuild()
