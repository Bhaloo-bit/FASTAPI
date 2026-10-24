# Pydantic models to validate user data 

from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLCreate(BaseModel):
    original_url : HttpUrl

class URLResponse(BaseModel):
    short_url : str


class AnalyticsResponse(BaseModel):
    short_url : str
    click_count: int
    last_accessed: datetime | None = None