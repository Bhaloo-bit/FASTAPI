from enum import Enum
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

# orderStatus (Enum) -> preparing , picked_up, in_trasnsit, delivered
class Orderstatus(str, Enum):
    PREPARING = "preparing"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"

# Database table for orders
class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    delivery_address: str
    items: str
    status: Orderstatus = Field(default=Orderstatus.PREPARING)
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})


# schema for creating an order
class OrderCreate(SQLModel):
    customer_name: str
    delivery_address: str
    items: str 

# schema for updating an order's status
class OrderUpdateStatus(SQLModel):
    status: Optional[Orderstatus] = None
    delivery_address: Optional[str] = None

# StatusLog
class StatusLog(SQLModel):
    order_id: int 
    old_status: str
    new_status: str
    changed_at: datetime 

