from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


class BookUpdate(BaseModel):
    title: str = Field(min_length=2, max_length=30)
    price: float = Field(gt=0)


books = [
    {"id": 1, "title": "Python", "price": 500},
    {"id": 2, "title": "FastAPI", "price": 450}
]



@app.get("/books")
def get_books():
    return books


@app.put("/books/{book_id}")
def update_book(book_id: int, book: BookUpdate):

    for item in books:

        if item["id"] == book_id:

            item["title"] = book.title
            item["price"] = book.price

            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )