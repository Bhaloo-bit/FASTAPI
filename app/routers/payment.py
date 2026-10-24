"""
POST - orders/{id}/products
GET  - orders/{id}/payments
GET - /payments/{id}
"""
from fastapi import APIRouter, Depends
from models import Order, Payment
from database import get_session
from sqlmodel import Session, select

router = APIRouter(predix="/orders", tags=["Payments"])

@router.post("/{id}/payments")
def create_payment(id: int, payment: Payment, session: Session = Depends(get_session)):
    order = session.exec(select(Order).where(Order.id == id)).first()
    if not order:
        return {"error": "Order not found"}
    
    payment.order_id = id
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return payment  

@router.get("/{id}/payments")
def get_payments(id: int, session: Session = Depends(get_session)):
    order = session.exec(select(Order).where(Order.id == id)).first()
    if not order:
        return {"error": "Order not found"}
    
    payments = session.exec(select(Payment).where(Payment.order_id == id)).all()
    return payments

@router.get("/payments/{id}")
def get_payment(id: int, session: Session = Depends(get_session)):
    payment = session.exec(select(Payment).where(Payment.id == id)).first()
    if not payment:
        return {"error": "Payment not found"}
    
    return payment