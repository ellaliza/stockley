from pydantic import BaseModel, Field
from typing import Optional, List, TYPE_CHECKING
if TYPE_CHECKING:
    from .users import StoreMemberRead
    from .products import ProductRead

class StoreBase(BaseModel):
    name: str
    description: Optional[str]
    location: Optional[str]


class StoreCreate(BaseModel):
    pass


class StoreRead(StoreBase):
    id: Optional[int] = Field(default=None, primary_key=True)


class StoreReadWithProducts(StoreRead):
    
    products: List["ProductRead"] = Field(default_factory=list)

class StoreReadWithMembers(StoreRead):
    
    members: List["StoreMemberRead"] = Field(default_factory=list)
    
class StoreReadWithProductsAndMembers(StoreReadWithMembers):
    
    products: List["ProductRead"] = Field(default_factory=list)
