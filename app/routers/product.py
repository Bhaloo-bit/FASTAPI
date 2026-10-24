from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_session
from models import products
from sqlmodel import Session, select

router = APIRouter("/product", tags=["products"])


# to add products in database
@router.post("/", response_model=products)
def create_products(product:str, session: Session = Depends(get_session)):
    new_products = products(**product.model_dump())
    session.add(new_products)
    session.commit()
    session.refresh()
    return new_products



# to get all the product in a list
@router.get("/", response_model=products)
def list_products(session: Session = Depends(get_session)):
    return session.exec(select(products)).all()


# to get product by id 
@router.get("/{product_id}", response_model=products)
def productby_id(product_id : int, session : Session = Depends(get_session)):
    product = session.get(products, product_id)
    if not product:
        raise HTTPException(status_code=404, details= "Product not found")
    return product

# to delete the products

@router.delete("/{product_id}",response_model=products)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    delete_product = session.get(products, product_id)
    if not delete_product:
        raise HTTPException(status_code=404, detail="product not found")
    session.delete(delete_product)
    session.refresh


