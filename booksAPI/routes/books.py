from fastapi import Depends, HTTPException, APIRouter,Query
from sqlmodel import select, Session
from database import get_session
from typing import Optional

from models.books import Book, Bookread,  Bookcreate, BookUpdate

from auth import verify_api_key

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=list[Bookread])
async def list_books(
    title: Optional[str] = Query(default = None),
    author : Optional[str] = Query(default=None),
    session : Session = Depends(get_session)
):
    query = select(Book).where(
        Book.is_sold == False
    )
    if title:
        query = query.where(Book.title.conatains(title))
    if author:
        query = query.where(Book.author.cantains(author))
    books = session.exec(query).all()
    return books    

# to create books

@router.post("/", response_model=Bookread)
async def create_book(
    book_data: Bookcreate,
    session : Session= Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    book = Book.model_validate(book_data)
    session.add(book)
    session.commit()
    session.refresh()
    return book

@router.patch("/{book_id}", response_model=Bookread)
async def book_update(
    book_id : int,
    updates: BookUpdate,
    session : Session = Depends(get_session),
    api_key: str = Depends(verify_api_key)
):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, details="Book not found")

    book_data = updates.model_dump(exclude_unset=True)
    for key , value in book_data.items():
        setattr(book, key, value)
    
    session.add(book_data)
    session.commit()
    session.refresh(book_data)
    return book_data    

@router.patch("/{book_id}/sold", response_model=Bookread)
async def mark_book_sold(
    book_id : int,
    session: Session = Depends(get_session),
    api_key : str = Depends(verify_api_key)
):

    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    bool.is_sold = True
    session.add(book)
    session.commit()
    session.refresh(book)
    return book