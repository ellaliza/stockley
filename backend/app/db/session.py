"""
Database session management.

This module configures the SQLAlchemy/SQLModel database engine and provides
session management utilities for database operations.
"""

from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends
from app.models import users, products, stores

# Database configuration
sqlite_file_name = "stockley.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
sqlite = "sqlite://"

# Create SQLAlchemy engine with SQLite
# echo=True enables SQL query logging for development
# check_same_thread=False allows the engine to be used in FastAPI's async context
engine = create_engine(sqlite, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """
    Create all database tables defined in SQLModel models.

    This function should be called during application startup to ensure
    all tables exist in the database.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Generator function that provides database sessions.

    Yields a SQLAlchemy Session object for database operations.
    The session is automatically closed when the context ends.
    Used as a FastAPI dependency for injecting database sessions.
    """
    with Session(engine) as session:
        yield session

# FastAPI dependency for injecting database sessions into endpoints
SessionDep = Annotated[Session, Depends(get_session)]