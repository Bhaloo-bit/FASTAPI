from sqlmodel import SQLModel, Field, relationship
from typing import Optional

class User(SQLModel, table=True):
    pass