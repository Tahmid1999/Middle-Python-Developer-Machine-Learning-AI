from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.orm import Session
from typing import List
from fastapi import  HTTPException, status
from app.models import book, author, client
from sqlalchemy.orm import joinedload


class BorrowCreate(BaseModel):
    book_id: int

class UnlinkRequest(BaseModel):
    borrow_id: int

    
class Borrow(Base):
    __tablename__ = "borrows"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    clients = relationship("Client", back_populates="borrows")
    books = relationship("Book", back_populates="borrows")


def get_borrowed_books(db: Session, client_id: int):
    borrows = db.query(Borrow).filter(Borrow.client_id == client_id).all()

    for borrow in borrows:
        # Fetch book details
        borrow.book = db.query(book.Book).filter(book.Book.id == borrow.book_id).first()

        # Fetch client details without password
        client_data = db.query(client.Client).filter(client.Client.id == borrow.client_id).first()
        borrow.client = client.Client(id=client_data.id, full_name= client_data.full_name, email=client_data.email)
        
    return borrows

def create_borrow(db: Session, borrow_data: BorrowCreate, current_user: int):
    db_borrow = Borrow(**borrow_data.dict(), client_id=current_user)
    db.add(db_borrow)
    db.commit()
    db.refresh(db_borrow)
    return db_borrow

def delete_borrow(db: Session, borrow_id: int, current_user: int):
    db_borrow = db.query(Borrow).filter(Borrow.id == borrow_id, Borrow.client_id == current_user).first()
    if db_borrow is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrow not found")
    db.delete(db_borrow)
    db.commit()
    return {"message": "Boook un-borrowed successfully"}

