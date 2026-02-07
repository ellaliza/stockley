"""
User service utilities.

This module provides common user-related dependencies and utilities
for dependency injection in FastAPI endpoints.
"""

from fastapi import Depends
from typing import Annotated
from app.models.users import User, StoreMember
from app.services.auth import get_current_user
from sqlmodel import Session, select

# Dependency for injecting the currently authenticated user into endpoint functions
# This combines the User type with the get_current_user dependency for clean usage
CurrentUserDep = Annotated[User, Depends(get_current_user)]

from sqlmodel import select, exists

def is_user_in_store(
    session: Session,
    user_id: int,
    store_id: int
) -> bool:
    stmt = select(StoreMember).where(
        StoreMember.user_id == user_id,
        StoreMember.store_id == store_id
    )
    
    return session.exec(select(exists(stmt))).one()