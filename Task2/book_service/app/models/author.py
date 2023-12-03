# app/models/author.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from typing import List


class AuthorCreate(BaseModel):
    full_name: str

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    books = relationship("Book", back_populates="author")

def create_author(db: Session, author_data: AuthorCreate):
    db_author = Author(**author_data.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors_with_filter(db: Session, full_name_start: str = None) -> List[Author]:
    query = db.query(Author)

    if full_name_start:
        query = query.filter(Author.full_name.startswith(full_name_start))

    authors = query.all()
    return authors