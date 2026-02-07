"""
Custom exception classes and utilities for the application.

This module defines application-specific exceptions and helper functions
for consistent error handling across the API.
"""

from fastapi import HTTPException, status


class UserAlreadyAssignedToStore(Exception):
    """
    Exception raised when attempting to add a user to a store they already belong to.

    This prevents duplicate memberships and maintains data integrity.
    """
    pass


class UnauthorizedError(Exception):
    """
    Exception raised when a user attempts an action they don't have permission for.

    This is typically used for role-based access control violations.
    """
    pass


def bad_request_exception(error: str):
    """
    Create a standardized HTTP 400 Bad Request exception.

    Args:
        error (str): The error message to include in the response.

    Returns:
        HTTPException: A FastAPI HTTP exception with status 400.
    """
    return HTTPException(status.HTTP_400_BAD_REQUEST, f"An error occured: {error}")

class StoreNotFoundError(Exception):
    pass