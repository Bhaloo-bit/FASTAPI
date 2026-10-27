from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, SQLModel, create_engine, select

# Your SQLModel tables live in models.py (table=True classes)
from models import Category, Customer, Order, OrderItem, Payment, Product

DATABASE_URL = "sqlite:///./ecommerce.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="E-commerce API", lifespan=lifespan)


@app.get("/")
def root():
    return {"status": "ok"}


# ---------- Categories ----------
@app.post("/categories", response_model=Category)
def create_category(category: Category, session: SessionDep):
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@app.get("/categories", response_model=list[Category])
def list_categories(session: SessionDep):
    return session.exec(select(Category)).all()


# ---------- Products ----------
@app.post("/products", response_model=Product)
def create_product(product: Product, session: SessionDep):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@app.get("/products", response_model=list[Product])
def list_products(session: SessionDep, offset: int = 0, limit: int = 20):
    return session.exec(select(Product).offset(offset).limit(limit)).all()


@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int, session: SessionDep):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, session: SessionDep):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    session.delete(product)
    session.commit()
    return {"deleted": product_id}


# ---------- Customers ----------
@app.post("/customers", response_model=Customer)
def create_customer(customer: Customer, session: SessionDep):
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@app.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int, session: SessionDep):
    customer = session.get(Customer, customer_id)
    if not customer:
        raise HTTPException(404, "Customer not found")
    return customer


# ---------- Orders ----------
@app.post("/orders", response_model=Order)
def create_order(order: Order, session: SessionDep):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int, session: SessionDep):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    return order


