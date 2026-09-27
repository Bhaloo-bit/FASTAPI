from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_session
from models import Order, OrderCreate, OrderUpdateStatus, StatusLog, Orderstatus
from sqlmodel import Session, select
from datetime import datetime

router = APIRouter(prefix="/orders", tags=['orders'])

# to create order with the api
@router.post("/", response_model=Order)
async def create_orders(order: OrderCreate, session: Session =Depends(get_session)):
    # converting data from JSON format to dictionary
        db_order = Order(**order.model_dump())
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order

# to able to see the orders
# this is the way to get multi parameter
@router.get("/", response_model=list[Order])
async def list_orders(
        status: Orderstatus | None =Query(default=None, description="Filtered by orders stauts"),
        created_at: str  | None = Query(default=None, description="Filter by creation date (YYYY-MM-DD)"),
        skip : int = Query(0, ge=0),
        limit : int = Query(10, ge=1),
        session: Session = Depends(get_session)
):
    query = select(Order)

    if status: 
          query = query.where(Order.status == status)
    
    if created_at:
          start = datetime.combine(created_at, datetime.min.time())
          end = datetime.combine(created_at, datetime.max.time())
          start = datetime.combine(datetime.strptime(created_at, "%Y-%m-%d"), datetime.min())
          end = datetime.combine(datetime.strptime(created_at, "%Y-%m-%d"), datetime.now())
          query = query.where(Order.created_at >=start, Order.created_at <=end)

    query = query.offset(skip.limit(limit))    
    return session.exec(query).all()
        
