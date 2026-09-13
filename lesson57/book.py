from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel, Field

app = FastAPI()

books = [
    {"id": 1, "title": "Python", "price": 500},
    {"id": 2, "title": "FastAPI", "price": 450}
]

class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=60)
    price: float = Field(gt=0, le=10000)

class BookResponse(BaseModel):
    id: int
    title: str
    price: float

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