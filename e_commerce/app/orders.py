from fastapi import APIRouter, Depends, HTTPException
from database import get_session
from models import orders, customers, products
from sqlmodel import Session, select    

router = APIRouter(prefix="/orders", tags=["orders"])

# to create order 
@router.post("/", response_model=orders, status_code=201)
async def create_order(order: orders, session: Session = Depends(get_session)):
    customer = session.get(customers, order.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    new_order = orders(**order.model_dump())
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

# to get all orders
@router.get("/", response_model=list[orders])
async def get_all_orders(session: Session = Depends(get_session)):  
    return session.exec(select(orders)).all()


# to get order by id
@router.get("/{order_id}", response_model=orders)
async def get_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(orders, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order    


# to update order by id
@router.patch("/{order_id}", response_model=orders)
async def update_order(order_id: int, data: orders, session: Session = Depends(get_session)):
    order = session.get(orders, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.customer_id = data.customer_id
    order.total_amount = data.total_amount
    order.status = data.status
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

# to delete order by id
@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(orders, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(order)
    session.commit()    