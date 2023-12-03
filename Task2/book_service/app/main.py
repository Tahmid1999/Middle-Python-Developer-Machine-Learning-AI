# app/main.py
from fastapi import FastAPI, HTTPException, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import book, author, client, borrow
from typing import List
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os



Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login/")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token_data):
    try:
        payload = jwt.decode(token_data, SECRET_KEY, algorithms=[ALGORITHM])
        
        print("Payload:", payload)
        return payload
    except JWTError:
        print("JWTError occurred")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )



        
class AdminLogin(BaseModel):
    username: str
    password: str

@app.post("/api/admin/login/", description="Login for admin.")
async def login_for_access_token(user_login: AdminLogin):
    # For testing purposes, let's assume there is a user with username "admin" and password "admin123"
    if user_login.username == "admin" and user_login.password == "admin123":
        access_token = create_access_token(data={"sub": user_login.username, "role": "admin"})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        # If the credentials are invalid, raise an HTTPException
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

#Write  function to register a user (client). Client  have  full name , email and  password  fields.        
@app.post("/api/register/", description="Register a client.")
def register_client(client_data: client.ClientCreate, db: Session = Depends(get_db)):
    return client.create_client(db, client_data)

@app.post("/api/login/", description="Login for client.")
def login_client(client_data: client.ClientLogin, db: Session = Depends(get_db)):
    Client = client.login_client(db, client_data)
    if Client:
        access_token = create_access_token(data={"id": Client.id,"role":"client"})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
            
# Add book
@app.post("/api/books/", description="Add a book. This endpoint is only accessible to admin.")
def add_book(book_data: book.BookCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")  
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user is not an admin")
    try:
        return book.create_book(db, book_data)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid book data")  

# Edit book
@app.put("/api/books/{book_id}", description="Edit a book. This endpoint is only accessible to admin.")
def edit_book(book_id: int, book_data: book.BookUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")    
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user is not an admin")
    return book.edit_book(db, book_id, book_data)

# Retrieve list of books with filtering options
@app.get("/api/books/", description="Retrieve list of books with filtering options. This endpoint is only accessible to admin.")
def get_books(title_start: str = None, author_id: int = None, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")   
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user is not an admin") 
    return book.get_books(db, title_start, author_id)

# Add multiple books by the same author
@app.post("/api/authors/{author_id}/books/", description="Add multiple books by the same author. This endpoint is only accessible to admin.")
def add_books_by_author(author_id: int, book_titles: List[str], db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")    
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user is not an admin")
    return book.create_books_by_author(db, author_id, book_titles)

# Add author
@app.post("/api/authors/", description="Add author. This endpoint is only accessible to admin.")
def add_author(author_data: author.AuthorCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")    
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user is not an admin")
    return author.create_author(db, author_data)

# Retrieve list of authors with filtering options
@app.get("/api/authors/", description="Retrieve list of authors with filtering options. This endpoint is only accessible to admin.")
def get_authors(full_name_start: str = None, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user is not an admin")
    return author.get_authors_with_filter(db, full_name_start)


# Create client
@app.post("/api/clients/", description="Create client. This endpoint is only accessible to admin. Admin can directly create a client without registering.")
def create_client(client_data: client.ClientCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")    
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user is not an admin")
    return client.create_client(db, client_data)

# Retrieve list of clients with filtering options
@app.get("/api/clients/", description="Retrieve list of clients with filtering options. This endpoint is only accessible to admin.")
def get_clients(full_name_start: str = None, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if current_user["role"] != "admin":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user is not an admin")
    return client.get_clients_with_filter(db, full_name_start)


# Retrieve list of books borrowed by the client
@app.get("/api/clients/books/", description="Retrieve list of books borrowed by the client. This endpoint is only accessible to client.")
def get_books_borrowed_by_client(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")  
    if current_user["role"] != "client":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user is not an client")  
    return borrow.get_borrowed_books(db, current_user["id"])

# Link client to a book
@app.post("/api/clients/books/link/", description="Link client to a book. This endpoint is only accessible to client.")
def link_client_to_book(book_data: borrow.BorrowCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials") 
    if current_user["role"] != "client":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user is not an client")   
    print("Current user:", current_user)
    return borrow.create_borrow(db, book_data, current_user["id"])

# Unlink client from a book
@app.post("/api/clients/books/unlink/", description="Unlink client from a book. This endpoint is only accessible to client.")
def unlink_client_from_book(request: borrow.UnlinkRequest, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = get_current_user(token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")   
    if current_user["role"] != "client":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="This user is not a client") 

    return borrow.delete_borrow(db, request.borrow_id, current_user["id"])