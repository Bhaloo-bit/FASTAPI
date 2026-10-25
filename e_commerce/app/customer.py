from fastapi import APIRouter, Depends, HTTPException
from database import get_session
from models import customers, orders
from sqlmodel import Session, select 

router = APIRouter(prefix="/customer", tags=["customers"])
# to add customer to database

@router.post("/", response_model=customers, status_code=201)
async def create_customer(customer: customers, session: Session = Depends(get_session)):
    new_customer = customers(**customer.model_dump())
    session.add(new_customer)
    session.commit()
    session.refresh(new_customer)
    return new_customer


# to return all the customers in the database
@router.get("/", response_model=list[customers])
async def get_all_customers(session: Session = Depends(get_session)):   
    return session.exec(select(customers)).all()



# to return customer by id
@router.get("/{customer_id}", response_model=customers)
async def get_customer(customer_id: int, session: Session = Depends(get_session)): 
    customer = session.get(customers, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


# to update customer by id
@router.put("/{customer_id}", response_model=customers)
def update_customer(customer_id: int, data: customers, session: Session = Depends(get_session)):
    customer = session.get(customers, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.name = data.name
    customer.phone = data.phone
    customer.email = data.email
    customer.city = data.city
    customer.state = data.state
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

# to delete customer by id
@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, session: Session = Depends(get_session)):
    customer = session.get(customers, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    session.delete(customer)
    session.commit()