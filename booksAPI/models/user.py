from sqlmodel import SQLModel, Field, relationship
from typing import Optional
from books import Book

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    college: str

    books: list["Book"] = relationship(back_populates="user")  # Relationship to Book model

