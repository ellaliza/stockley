from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends
from app.models import users, products, stores

sqlite_file_name = "stockley.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
sqlite = "sqlite://"

engine = create_engine(sqlite, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]