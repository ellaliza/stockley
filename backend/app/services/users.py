"""
User service utilities.

This module provides common user-related dependencies and utilities
for dependency injection in FastAPI endpoints.
"""

from fastapi import Depends
from typing import Annotated
from app.models.users import User
from app.services.auth import get_current_user

# Dependency for injecting the currently authenticated user into endpoint functions
# This combines the User type with the get_current_user dependency for clean usage
CurrentUserDep = Annotated[User, Depends(get_current_user)]