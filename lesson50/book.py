from fastapi import FastAPI, HTTPException, status

app = FastAPI()

books = [
    {"id": 1, "title": "Python", "price": 500},
    {"id": 2, "title": "FastAPI", "price": 450},
    {"id": 3, "title": "Backend", "price": 350}
]


@app.get("/books")
def get_books():
    return books


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