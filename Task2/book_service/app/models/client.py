# app/models/client.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.orm import Session
from typing import List
from fastapi import  HTTPException, status
from passlib.context import CryptContext

#from app.models.client import ClientCreate, Client  # Import Client model


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ClientCreate(BaseModel):
    full_name: str
    email: str
    password: str

class ClientLogin(BaseModel):
    email: str
    password: str    
    
class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    password = Column(String, index=True)
    email = Column(String, index=True)
    borrows = relationship('Borrow', back_populates='clients')
    


def create_client(db: Session, client_data: ClientCreate):
    db_client = Client(**client_data.dict())
    #Verity if  email is unique
    if db.query(Client).filter(Client.email == db_client.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    #Verify if  email is valid
    if not "@" in db_client.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")
    
    hashed_password = pwd_context.hash(client_data.password)
    
    
    new_client = Client(full_name=client_data.full_name, email=client_data.email, password=hashed_password)
    
    # Save the new client to the database
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


def login_client(db: Session, client_data: ClientLogin):
    # Check if the client with the provided email exists
    db_client = db.query(Client).filter(Client.email == client_data.email).first()

    if db_client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")

    if pwd_context.verify(client_data.password, db_client.password) == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")

    return db_client

def get_clients_with_filter(db: Session, full_name_start: str = None) -> List[Client]:
    query = db.query(Client)

    if full_name_start:
        query = query.filter(Client.full_name.startswith(full_name_start))

    clients = query.all()
    return clients


