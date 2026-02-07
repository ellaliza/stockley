"""
Authentication and user management API endpoints.

This module provides REST API endpoints for user authentication, registration,
profile management, and protected resource access using JWT tokens.
"""

from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from typing import Annotated, List
from fastapi import Depends, HTTPException, status, Form, APIRouter
from app.services.auth import *
from sqlmodel import select
from app.db.session import SessionDep
from app.models.auth import Token
from app.models.users import User
from app.schemas.users import UserRead, UserCreate
from app.services.users import CurrentUserDep

router = APIRouter(
    prefix="/auth",
    tags = ["Authentication"]
)

# ------------path operations -------------
@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep
    ):
    """
    Authenticate user and return JWT access token.

    This endpoint implements OAuth2 password flow for user login.
    Validates credentials and returns a JWT token for authenticated requests.

    Args:
        form_data: OAuth2 form containing username and password.
        session: Database session dependency.

    Returns:
        Token: JWT access token with bearer type.

    Raises:
        HTTPException: 401 if credentials are invalid.
    """
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserRead)
async def register(session: SessionDep, user: UserCreate = Depends(UserCreate.as_form)):
    """
    Register a new user account.

    Creates a new user account with the provided information. Performs validation
    to ensure username uniqueness and securely hashes the password.

    Args:
        session: Database session dependency.
        user: User creation data from form submission.

    Returns:
        UserRead: The created user information (excluding password).

    Raises:
        HTTPException: 400 if username already exists.
    """
    
    db_user = get_user_by_username(session, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )


    hashed_password = get_password_hash(user.password)
    user_data = {
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": hashed_password,
    }
    

    db_user = create_user(session, user_data)
    return db_user


@router.get("/users/me", response_model=User)
async def read_users_me(
    current_user: CurrentUserDep,
):
    """
    Retrieve current authenticated user's profile information.

    Returns the full user object for the currently authenticated user.
    Requires a valid JWT token in the Authorization header.

    Args:
        current_user: The authenticated user from JWT token.

    Returns:
        User: Complete user profile information.
    """
    return current_user

@router.put("/users/me", response_model=UserRead)
async def update_user(
    user_update: UserCreate,
    current_user: CurrentUserDep,
    session: SessionDep
):
    """
    Update current authenticated user's profile information.

    Allows users to update their own profile data including email, full name, and password.
    Only provided fields will be updated (partial update).

    Args:
        user_update: Updated user data (only provided fields are updated).
        current_user: The authenticated user making the request.
        session: Database session dependency.

    Returns:
        UserRead: Updated user information.
    """
    update_data = user_update.model_dump(exclude_unset=True)

    # Hash password if provided
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

    # Update user fields
    for key, value in update_data.items():
        setattr(current_user, key, value)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.get("/users", response_model=List[UserRead])
async def read_users(
    session: SessionDep,
    current_user: CurrentUserDep,
    skip: int = 0,
    limit: int = 100
):
    """
    Retrieve a paginated list of all users.

    Returns a list of all registered users with pagination support.
    Requires authentication but no specific permissions.

    Args:
        session: Database session dependency.
        current_user: Authenticated user (for access control).
        skip: Number of records to skip (default: 0).
        limit: Maximum number of records to return (default: 100).

    Returns:
        List[UserRead]: Paginated list of user information.
    """
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users


# ==================== Protected Resource Example ====================

@router.get("/items")
async def read_items(
    current_user: CurrentUserDep
):
    """
    Example protected endpoint demonstrating authentication.

    Returns sample items owned by the authenticated user.
    This is a demonstration endpoint for testing authentication.

    Args:
        current_user: The authenticated user.

    Returns:
        dict: Sample items data with user ownership.
    """
    return {
        "items": [
            {"id": 1, "name": "Item 1", "owner": current_user.username},
            {"id": 2, "name": "Item 2", "owner": current_user.username},
        ],
        "user": current_user.username
    }


# ==================== Health Check ====================

@router.get("/")
async def root():
    """
    API health check endpoint.

    Returns basic API information and status.
    No authentication required.

    Returns:
        dict: API status and information.
    """
    return {
        "message": "JWT Auth API with SQLite and Argon2",
        "status": "running"
    }

@router.get("/items/")
async def read_items(current_user: CurrentUserDep):
    """
    Alternative example of a protected endpoint.

    Returns sample item data for the authenticated user.
    Demonstrates multiple protected endpoints.

    Args:
        current_user: The authenticated user.

    Returns:
        List[dict]: Sample items with ownership information.
    """
    return [
        {"item_id": 1, "owner": current_user.username},
        {"item_id": 2, "owner": current_user.username},
    ]