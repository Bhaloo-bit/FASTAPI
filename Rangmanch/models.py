from sqlmodel import SQLModel ,Field
from typing import Optional
from datetime import datetime

#Sql table in db
class Review(SQLModel, table=True):
    id : Optional[int] = Field(default=None , primary_key=True)
    play_name : str = Field(index=True)
    reviewer_name: str
    rating: int = Field(ge=1, le=5)
    comment: str
    created_at: datetime = Field(default_factory=datetime.now)

# validation 
# data validation to create comment
class ReviewCreate(SQLModel):
    play_name: str
    reviewer_name: str
    rating: int = Field(ge=1, le=5)
    comment : str

#data validation for view the comment
class ReviewRead(SQLModel):
    id: int
    play_name: str
    reviewer_name: str
    rating: int
    comment: str
    created_at: datetime

#data validation to update existing review
class ReviewUpdate(SQLModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    comment: Optional[str] = None



