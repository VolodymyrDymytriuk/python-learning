from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class BookCreate(BaseModel):
    title: str
    author: str
    price: float


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: float
   
    
@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)

def create_book(book: BookCreate):
    return {
        "id": 100,
        "title": book.title,
        "author": book.author,
        "price": book.price
    }