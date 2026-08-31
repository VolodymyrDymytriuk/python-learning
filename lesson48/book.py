from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI()

class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=30)
    author: str = Field(min_length=2, max_length=30)
    price: float = Field(gt=0)

books = [
    {"id": 1, "title": "Python", "author": "John", "price":500.0 },
    {"id": 2, "title": "Java", "author": "Sierra", "price":450.0 }
]

@app.post(
        "/books",
        status_code=status.HTTP_201_CREATED
)

def create_book(book: BookCreate):
    new_book = {
        "id": len(books) + 1,
        "title": book.title,
        "author": book.author,
        "price": book.price
    }
    books.append(new_book)
    return new_book

@app.get("/books")
def get_books():
    return books