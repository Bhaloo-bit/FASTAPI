from fastapi import APIRouter, Depends, HTTPException, Query
from  models import categories, products
from database import get_session
from sqlmodel import Session, select
from datetime import datetime


router = APIRouter(prefix="category", tags=['cateogories'])

# to post categories
@router.post("/", response_model=categories, status_code=201)
async def create_category(categories: create_category, session: Session = Depends(get_session)):
        categorie = categories(**create_category.model_dump())
        session.add(categorie)
        session.commit()
        session.refresh(categorie)
        return categorie

# to list all the catogery at once
@router.get("/", response_model=list[categories])
async def get_categories(session: Session= Depends(get_session)):
        return session.exec(select(categories)).all()


# to list category by id
@router.get("/{category_id}", response_model=categories)
async def get_catogery(category_id: int, session: Session = Depends(get_session)):
        catogery = session.get(categories, category_id)
        if not catogery:
                raise HTTPException(status_code=404, detail="Catogry not found")
        return catogery


# to update category 
@router.put("/{category_id}", response_model=categories)
async def update_category(category_id: int, data: categories, session: Session = Depends(get_session)):
        category = session.get(categories, category_id)
        if not category:
                raise HTTPException(status_code=404, detail="Category does not exist")
        category.name = data.name
        category.description = data.description
        session.add(category)
        session.commit()
        session.refresh(category)
        return category

# to delete category 
@router.delete("/{category_id}", status_code=204)
async def delete_categroy(categroy_id: int, session: Session = Depends(get_session)):
        category = session.get(categories, categroy_id)
        if not category:
                raise HTTPException(status_code=404,detail="Category not found")
        session.delete(category)
        session.commit()

# to category with product id
@router.get("/categories/{id}/products", response_model =list[products]) 
async def get_categories_product(category_id : int, session: Session = Depends(get_session)):
        if not session.get(categories, category_id):
                raise HTTPException(status_code=404, detail="Not found")
        return session.exec(select(products).where(products.category_id = category_id)).all()        


