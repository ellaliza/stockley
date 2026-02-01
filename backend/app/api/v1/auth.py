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
    Login endpoint - OAuth2 password flow
    
    Returns JWT access token if credentials are valid
    
    Request body (form data):
        username: User's username
        password: User's password
    
    Response:
        access_token: JWT token
        token_type: "bearer"
    """

    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserRead)
async def register(session: SessionDep, user: UserCreate = Depends(UserCreate.as_form)):
    """
    Register a new user
    
    Process:
    1. Check if username/email already exists
    2. Hash password with Argon2
    3. Store user in database
    4. Return user info (without password)
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
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """
    Get current authenticated user's information
    
    Requires valid JWT token in Authorization header
    """
    return current_user

@router.put("/users/me", response_model=UserRead)
async def update_user(
    user_update: UserCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: SessionDep
):
    """
    Update current user's information
    
    Can update: email, full_name, password
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
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100
):
    """
    Get list of all users (requires authentication)
    
    Query params:
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return
    """
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users


# ==================== Protected Resource Example ====================

@router.get("/items")
async def read_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Example of a protected endpoint
    
    Only authenticated users can access this
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
    """Health check endpoint"""
    return {
        "message": "JWT Auth API with SQLite and Argon2",
        "status": "running"
    }
@router.get("/items/")
async def read_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    """
    Protected endpoint example
    """
    return [
        {"item_id": 1, "owner": current_user.username},
        {"item_id": 2, "owner": current_user.username},
    ]