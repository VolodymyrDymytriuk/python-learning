from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class BookCreate(BaseModel):
    title: str
    price: float
    author: str

class BookResponse(BaseModel):
    id: int
    title: str
    price: float
    author: str

@app.post("/books", response_model=BookResponse)
def create_book(book:BookCreate):
    return {
        "id":100,
        "title":book.title,
        "price":book.price,
        "author":book.author
    }