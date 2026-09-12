from fastapi import FastAPI, HTTPException, Path, status

app = FastAPI()

books = [
    {"id": 1, "title": "Python", "price": 500},
    {"id": 2, "title": "FastAPI", "price": 450},
    {"id": 3, "title": "Backend", "price": 350}
]


@app.get("/books/{book_id}")
def get_book(
    book_id: int = Path(ge=1, le=100)
):
    for book in books:

        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=" Book not found"
    )
