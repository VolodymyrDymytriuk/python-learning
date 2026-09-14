from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field

app = FastAPI()

books = [
    {"id": 1, "title": "Python", "price": 500},
    {"id": 2, "title": "FastAPI", "price": 450}
]

class BookUpdate(BaseModel):
    title: str = Field(min_length=2, max_length=60)
    price: float = Field(gt=0, le=10000)

@app.put("/books/{book_id}")
def update_book(
    book: BookUpdate,
    book_id: int = Path(ge=1)
):
    for item in books:
        if item["id"] == book_id:
            item["title"] = book.title
            item["price"] = book.price
            return item
      
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )
    