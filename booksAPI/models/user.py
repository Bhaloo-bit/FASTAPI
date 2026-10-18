from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from models.books import Book

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    college: str

    books: list["Book"] = Relationship(back_populates="user")  # Relationship to Book model

# request body for creating a user
class UserCreate(SQLModel):
    name : str
    email : str
    college : str

# response body
class UserRead(SQLModel):
    id : int
    name: str
    email : str
    collge: str




# avoid circular import

from models.books import Book
User.model_rebuild()