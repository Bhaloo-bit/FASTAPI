# SQLAlchemy tables  | SQL models
from  sqlmodel import SQLModel, Field 

from datetime import datetime, timezone

# Ownership - Url shorting services table : 1
class URLMapping(SQLModel, table = True):
    short_url : str = Field(default="none", primary_key=True, index=True)
    original_url : str = Field(default="None")
    created_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# Ownership - Url Analytics servics  table: 2
class Analytics(SQLModel, table= True):
    short_url : str = Field(primary_key=True, foreign_key="urlmapping.short_url")
    click_count : int = Field(default="0")
    last_accessed: datetime | None = None

# sql model to get original urls

class URLCreate(SQLModel):
    original_url : str

class URLResponse(SQLModel):
    short_url : str


# to get the analysis 
class AnalyticsResponse(SQLModel):
    short_url : str
    click_count : int
    last_accessed: datetime | None
