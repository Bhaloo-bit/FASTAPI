"""SQLModel table definitions for the e-commerce API."""

from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp for new and updated records."""
    return datetime.now(timezone.utc)


# These plural table names keep the schema consistent with the existing app modules.
class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    created_at: datetime = Field(default_factory=utc_now)


class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    id: int | None = Field(default=None, primary_key=True)
    name: str
    phone: str
    email: str | None = None
    city: str
    state: str
    created_at: datetime = Field(default_factory=utc_now)


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    customer_id: int | None = Field(default=None, foreign_key="customers.id")
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = True
    role: str = "customer"


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int | None = Field(default=None, primary_key=True)
    brand: str
    name: str
    price: float
    model: str
    category_id: int = Field(foreign_key="categories.id")
    expiry_date: str | None = None


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.id")
    total_amount: float
    status: str = "pending"
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")
    quantity: int
    price: float


class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    amount: float
    payment_method: str
    status: str = "pending"
    created_at: datetime = Field(default_factory=utc_now)


class Inventory(SQLModel, table=True):
    __tablename__ = "inventory"

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    available_quantity: int
    updated_at: datetime = Field(default_factory=utc_now)
