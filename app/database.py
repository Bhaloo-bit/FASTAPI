<<<<<<< HEAD
from sqlmodel import create_engine, Session , SQLModel

DATABASE_URL= "sqlite:///e_commerce.db"

engine = create_engine(DATABASE_URL, echo= True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    """Provide a new database session for each request."""
    with Session(engine) as Depsession:
        yield Depsession
=======
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
>>>>>>> 5ed265d418d0eb04aab90627542e987f350730fd
