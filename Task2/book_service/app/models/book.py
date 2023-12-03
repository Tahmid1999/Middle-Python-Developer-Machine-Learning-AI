# app/models/book.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from typing import List



class BookCreate(BaseModel):
    title: str
    author_id: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author_id: Optional[int] = None
        
class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
    borrows = relationship("Borrow", back_populates="books")

def create_book(db: Session, book_data: BookCreate):
    db_book = Book(**book_data.dict())  
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def edit_book(db: Session, book_id: int, book_data: BookUpdate, current_user: str):
    db_book = db.query(Book).filter(Book.id == book_id, Book.author_id == current_user).first()
    if db_book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    
    for key, value in book_data.dict().items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, title_start: str = None, author_id: int = None):
    query = db.query(Book)

    if title_start:
        query = query.filter(Book.title.startswith(title_start))
    if author_id:
        query = query.filter(Book.author_id == author_id)

    books = query.all()
    return books


def create_books_by_author(db: Session, author_id: int, book_titles: List[str]):
    for title in book_titles:
        db_book = Book(title=title, author_id=author_id)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    return {"message": "Books added successfully to author with id: " + str(author_id)}     