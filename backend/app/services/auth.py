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

pwd_context = CryptContext(schemes=['argon2'], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dotenv_path = os.path.join(basedir, '.env')
print("PATH:", dotenv_path)
load_dotenv(dotenv_path=dotenv_path)

TokenDep = Annotated[str, Depends(oauth2_scheme)]

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against an Argon2 hashed password
    
    Argon2 advantages over bcrypt:
    - More resistant to GPU/ASIC attacks
    - Configurable memory usage
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password using Argon2
    
    Example output:
    $argon2id$v=19$m=65536,t=3,p=4$base64salt$base64hash
    """
    return pwd_context.hash(password)


# User utilities
def get_user_by_username(session: Session, username: str):
    """Get user from database by username"""
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    return user

def get_user_by_email(session: Session, email: str):
    """Get user from database by username"""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def create_user(session: Session, user_data: dict) -> UserRead:
    """Create a new user in the database"""
    db_user = User(**user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    user = UserRead(**db_user.model_dump())
    return user

def authenticate_user(session: Session, username: str, password: str, email: str | None = None):
    """
    Authenticate a user by username and password
    
    Returns:
        User object if authentication successful
        False if authentication failed
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
    Create a JWT access token
    
    Args:
        data: Dictionary to encode (usually {"sub": username})
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token string
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
    Decode JWT token and get current user from database
    
    This is a dependency that:
    1. Extracts token from Authorization header
    2. Decodes and validates the JWT
    3. Fetches user from database
    4. Returns user object
    
    Raises:
        HTTPException 401 if token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
    Check if current user is active (not disabled)
    
    This is an additional layer of security on top of get_current_user
    """
    if not current_user:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user

