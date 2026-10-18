from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Book(SQLModel, table=True):
    id : Optional[int] = Field(default = None, primary_key=True)
    title : str = Field(index =True)
    author : str = Field(index = True)
    price : float
    is_sold: bool = Field(default = False)

    # Foreign key to user table
    user_id : int= Field(foreign_key="user.id")
    owner : Optional["User"] = Relationship(back_populates="books")

# request body for creatinf a book
class Bookcreate(SQLModel):
    title : str
    author: str
    price : float
    user_id : int

# response body
class Bookread(SQLModel):
    id : int
    title : str
    author: str
    price : float
    is_sold: bool   
    user_id : int

# to update detail of the existing books
class BookUpdate(SQLModel):
    price : Optional[int] = None
    is_sold: Optional[bool] = None



from models.user import User 
Book.model_rebuild()
