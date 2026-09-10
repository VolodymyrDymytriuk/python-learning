from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)


class BookResponse(BaseModel):
    id: int
    title: str
    price: float
    
class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=50)
    price: float | None = Field(default=None, gt=0)

books = [
    {"id": 1, "title": "Python", "price": 500},
    {"id": 2, "title": "FastAPI", "price": 450}
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
@app.patch(
    "/books/{book_id}",
    response_model=BookResponse
)
def update_book(book_id: int, book: BookUpdate):

    for item in books:

        if item["id"] == book_id:

            if book.title is not None:
                item["title"] = book.title

            if book.price is not None:
                item["price"] = book.price

            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )