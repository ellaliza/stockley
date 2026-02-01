from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .users import StoreMember
    from .products import Product


class StoreToStoreMemberLink(SQLModel, table=True):
    storemember_id: Optional[int] = Field(
        default=None,
        foreign_key="storemember.id",
        primary_key=True
    )
    store_id: Optional[int] = Field(
        default=None,
        foreign_key="store.id",
        primary_key=True
    )


class Store(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    description: Optional[str]
    location: Optional[str]

    members: List["StoreMember"] = Relationship(
        back_populates="stores",
        link_model=StoreToStoreMemberLink
    )

    products: List["Product"] = Relationship(
        back_populates="store"
    )
