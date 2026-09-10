from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)

books = [
   {"id": 1, "title": "Python", "price": 500},
   {"id": 2, "title": "FastAPI", "price": 450}
]

@app.post(
    "/books",
    status_code=status.HTTP_201_CREATED
)
def create_book(book: BookCreate):

    new_book = {
        "id": len(books) + 1,
        "title": book.title,
        "price": book.price
    }

    books.append(new_book)

    return new_book

@app.get("/books")
def get_books():
    return books

@app.get("/books/{book_id}")
def get_books(book_id: int):

    for book in books:

        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )

@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookCreate):

    for item in books:

        if item["id"] == book_id:

            item["title"] = book.title
            item["price"] = book.price
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )

@app.delete("/books/{book_id}")
def delete_book(book_id: int):

    for book in books:

        if book["id"] == book_id:

            books.remove(book)

            return {
                "message": "Book deleted"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )