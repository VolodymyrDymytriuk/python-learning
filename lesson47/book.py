from fastapi import FastAPI, HTTPException, status

app = FastAPI()

books = [
    {"id": 1, "title": "Python"},
    {"id": 2, "title": "FastAPI"},
    {"id": 3, "title": "Backend"}
]

@app.get("/books/{book_id}")
def get_book(book_id: int):

    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
    )