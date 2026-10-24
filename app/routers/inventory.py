from models import inventory
from sqlmodel import Session , select
from database import get_session
from fastapi import APIRouter, Depends, Query, HTTPException

router = APIRouter("/inventory", tags=["inventory"])

"""
GET /inventory
GET /inventory/{id}
PUT / inventoru/{id}
"""
# to view entire inventory
@router.get("/", response_mode= list[inventory])
def get_total_stock(session: Session = Depends(get_session)):
    return session.exec(select(inventory)).all()


# to get invetory of particular product / items

@router.get("/{inventory_id}", response_model=inventory)
def get_product_inventory(inventory_id: int, session: Session = Depends(get_session)):
    item_stock = session.get(inventory, inventory_id)
    if not item_stock:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_stock 

# to update inventory of particular product / items
@router.put("/{inventory_id}", response_model=inventory)
def update_product_inventory(inventory_id: int, data: inventory, session: Session = Depends(get_session)):
    item_stock = session.get(inventory, inventory_id)
    if not item_stock:
        raise HTTPException(status_code=404, detail="Item not found")
    item_stock.available_quantity = data.available_quantity
    item_stock.updated_at = data.updated_at
    session.add(item_stock)
    session.commit()
    session.refresh(item_stock)
    return item_stock
    

