"""
User and membership database models.

This module defines the SQLModel database models for users, platform roles,
store roles, and store memberships.
"""

from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .stores import Store


class PlatformRoles(str, Enum):
    """Platform-wide user roles."""
    ADMIN = "admin"
    REGULAR = "regular"


class StoreRoles(str, Enum):
    """Roles for users within specific stores."""
    OWNER = "owner"
    STAFF = "staff"


class User(SQLModel, table=True):
    """
    User model representing a platform user.

    Users can have platform-wide roles and can be members of multiple stores
    with different roles in each store.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    full_name: str
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    role: PlatformRoles = Field(default=PlatformRoles.REGULAR)

    # Relationship to store memberships
    store_memberships: List["StoreMember"] = Relationship(
        back_populates="user"
    )


class StoreMember(SQLModel, table=True):
    """
    Junction model representing a user's membership in a specific store.

    Each membership has a role (OWNER or STAFF) and tracks when the membership
    was created. Owners have additional permissions like adding/removing members.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    store_id: int = Field(foreign_key="store.id")
    role: StoreRoles
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships
    user: Optional[User] = Relationship(
        back_populates="store_memberships"
    )

    store: Optional["Store"] = Relationship(back_populates="members")
