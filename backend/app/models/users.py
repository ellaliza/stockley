from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from enum import Enum

from .stores import StoreToStoreMemberLink

if TYPE_CHECKING:
    from .stores import Store


class PlatformRoles(str, Enum):
    ADMIN = "admin"
    REGULAR = "regular"


class StoreRoles(str, Enum):
    OWNER = "owner"
    STAFF = "staff"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    full_name: str
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    role: PlatformRoles = Field(default=PlatformRoles.REGULAR)

    store_memberships: List["StoreMember"] = Relationship(
        back_populates="user"
    )


class StoreMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    role: StoreRoles
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)

    user: Optional[User] = Relationship(
        back_populates="store_memberships"
    )

    stores: List["Store"] = Relationship(
        back_populates="members",
        link_model=StoreToStoreMemberLink
    )
