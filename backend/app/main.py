"""
Stockley FastAPI Application

Main application module that configures and runs the FastAPI server.
Handles CORS, database initialization, and router registration.
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from typing import Annotated
from app.db.session import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager
from app.models.products import *
from app.api.v1 import auth, stores, products

# CORS allowed origins for cross-origin requests
origins = ["http://localhost:5173",
           "https://backend.ellaliza.dev",
           "https://frontend.ellaliza.dev"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Handles startup and shutdown events. Currently only initializes
    the database tables on startup.
    """
    create_db_and_tables()
    yield


# Create FastAPI application instance
app = FastAPI(lifespan=lifespan)

# Configure CORS middleware for cross-origin requests
app.add_middleware(CORSMiddleware,
                   allow_origins = origins,
                   allow_credentials = True,
                   allow_methods = ["*"],
                   allow_headers = ["*"])

# Register API routers
app.include_router(auth.router)
app.include_router(stores.router)
app.include_router(products.router)


@app.get("/")
def root():
    """
    Root endpoint providing basic API information.

    Returns a welcome message indicating the API is running.
    No authentication required.

    Returns:
        dict: Welcome message and API name.
    """
    return {"message":"Welcome to Stockley!"}

