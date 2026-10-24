from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

# to create all the table for the e-com api
'''
table name customers'''
class customers(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    phone: str = Field(nullable=False)
    email: str = Field(default=None, nullable=True)
    city: str = Field(nullable=False)
    state: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

"""
users table
"""
class users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.id", nullable=False)
    username: str = Field(nullable=False)
    email: str = Field(nullable=False)
    hashed_password: str = Field(nullable=False)
    role: str = Field(nullable=False)

"""
orders table
"""
class orders(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.id", nullable=False)
    total_amount: float = Field(nullable=False)
    status: str = Field(nullable=False, default="pending")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


"""
order_items table
"""
class order_items(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    product_id: int = Field(foreign_key="products.id", nullable=False)
    quantity: int = Field(nullable=False)
    price: float = Field(nullable=False)

"""
catogories table
"""

class categories(SQLModel, table=True): 
    id: int = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



""" products table
"""
class products(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    brand: str = Field(nullable=False)
    name : str 
    price : bool
    model: str = Field(nullable=False)
    category_id: int = categories.ForeignKey(on_delete=categories.CASCADE)
    expiry_date: str = Field(default=None, nullable=True)

"""
inventory table

"""
class inventory(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id", nullable=False)
    available_quantity: int = Field(nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))



"""
payements table

"""

class payments(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    amount: float = Field(nullable=False)
    payment_method: str = Field(nullable=False)
    status: str = Field(nullable=False, default="pending")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
