from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, TYPE_CHECKING
from fastapi import Form
if TYPE_CHECKING:
    from .stores import StoreRead
class UserBase(BaseModel):
    full_name: str = Field()
    email: str = Field(index = True, unique= True)
    role: str = Field(default="regular")
    username: str = Field()

class UserCreate(UserBase):
    password: str

    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        email: str = Form(...),
        full_name: str = Form(...),
        password: str = Form(...)
    ):
        return cls(
            username=username,
            email=email,
            full_name=full_name,
            password=password,
        )

class UserRead(UserBase):
    id: int
    created_at: datetime

class UserReadWithStores(UserBase):
    id: int
    created_at: datetime


class StoreMemberBase(BaseModel):
    role: str
    user_id : int = Field(foreign_key="user.id")

class StoreMemberRead(StoreMemberBase):
    id: int
    created_at: datetime
    user: UserRead
    stores: List[StoreRead]

class StoreMemberWrite(StoreMemberBase):
    pass
