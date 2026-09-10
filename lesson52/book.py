from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)


class BookResponse(BaseModel):
    id: int
    title: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    

books = [
    {"id": 1, "title": "Python", "price": 450},
    {"id": 2, "title": "FastAPI", "price": 400}
]

@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(book: BookCreate):

    new_id = max(
        (book["id"] for book in books),
        default=0
    ) + 1

    new_book = {
            "id": new_id,
            "title": book.title,
            "price": book.price
        }
    
    books.append(new_book)
    
    return new_book

@app.get(
    "/books/{book_id}",
    response_model=BookResponse
)
def get_book(book_id: int):
    for book in books:
    
         if book["id"] == book_id:
            return book
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )