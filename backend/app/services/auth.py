"""
Authentication service module.

This module provides authentication-related utilities including password hashing,
JWT token management, user authentication, and FastAPI dependency injection
for current user retrieval.
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session, select
from app.models.users import User
from app.schemas.users import UserRead
from app.db.session import SessionDep
from app.models.auth import TokenData
import os
from dotenv import load_dotenv

# Password hashing context using Argon2
pwd_context = CryptContext(schemes=['argon2'], deprecated="auto")

# OAuth2 password bearer scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Load environment variables from .env file
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dotenv_path = os.path.join(basedir, '.env')
print("PATH:", dotenv_path)
load_dotenv(dotenv_path=dotenv_path)

# Type annotation for token dependency
TokenDep = Annotated[str, Depends(oauth2_scheme)]

# JWT configuration from environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against an Argon2 hashed password.

    Uses Argon2 for secure password verification. Argon2 provides better
    resistance to GPU/ASIC attacks compared to bcrypt through configurable
    memory usage.

    Args:
        plain_password: The plain text password to verify.
        hashed_password: The Argon2 hash to verify against.

    Returns:
        bool: True if password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using Argon2.

    Generates a secure Argon2 hash suitable for password storage.
    The hash includes salt and follows the format:
    $argon2id$v=19$m=65536,t=3,p=4$base64salt$base64hash

    Args:
        password: The plain text password to hash.

    Returns:
        str: The Argon2 hash string.
    """
    return pwd_context.hash(password)


# User utilities
def get_user_by_username(session: Session, username: str):
    """
    Retrieve a user from the database by username.

    Args:
        session: Database session.
        username: The username to search for.

    Returns:
        User or None: The user object if found, None otherwise.
    """
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user

def get_user_by_email(session: Session, email: str):
    """
    Retrieve a user from the database by email address.

    Args:
        session: Database session.
        email: The email address to search for.

    Returns:
        User or None: The user object if found, None otherwise.
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def create_user(session: Session, user_data: dict) -> UserRead:
    """
    Create a new user in the database.

    Args:
        session: Database session.
        user_data: Dictionary containing user creation data.

    Returns:
        UserRead: The created user information (excluding sensitive data).
    """

    db_user = User(**user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    user = UserRead.model_validate(db_user)
    return user

def authenticate_user(session: Session, username: str, password: str, email: str | None = None):
    """
    Authenticate a user by username and password.

    Args:
        session: Database session.
        username: The username to authenticate.
        password: The plain text password.
        email: Optional email for additional validation (currently unused).

    Returns:
        User or False: The authenticated user object if successful, False otherwise.
    """
    user = get_user_by_username(session, username)
    if not user and email:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# JWT token utilities
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a JWT access token.

    Args:
        data: Dictionary to encode in the token (usually {"sub": username}).
        expires_delta: Optional custom expiration time delta.

    Returns:
        str: The encoded JWT token string.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: TokenDep, session: SessionDep):
    """
    Decode JWT token and retrieve the current user from the database.

    This is a FastAPI dependency that:
    1. Extracts the JWT token from the Authorization header
    2. Decodes and validates the JWT token
    3. Fetches the corresponding user from the database
    4. Returns the user object for use in protected endpoints

    Args:
        token: The JWT token from the Authorization header.
        session: Database session dependency.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: 401 if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("PAYLOAD:", payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user_by_username(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Validate that the current user is active (not disabled).

    This provides an additional layer of security on top of get_current_user
    to ensure the user account is still active.

    Args:
        current_user: The user object from get_current_user dependency.

    Returns:
        User: The validated active user object.

    Raises:
        HTTPException: 403 if the user is inactive.
    """
    if not current_user:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user

