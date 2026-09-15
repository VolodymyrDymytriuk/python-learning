from fastapi import FastAPI, HTTPException, Path, status

app = FastAPI()

books = [
    {"id": 1, "title": "Python", "price": 500},
    {"id": 2, "title": "FastAPI", "price": 450},
]

@app.delete("/books/{book_id}")
def delete_book(
    book_id: int = Path(ge=1)
):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            return {
                "message": "Book deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )