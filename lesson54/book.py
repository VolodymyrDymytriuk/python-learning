from fastapi import FastAPI

app = FastAPI()


books = [
    {"id": 1, "title": "Python", "price": 500},
    {"id": 2, "title": "FastAPI", "price": 450},
    {"id": 3, "title": "Backend", "price": 350}
]

@app.get("/books")
def get_books(max_price: float | None = None):

    if max_price is None:
        return books

    result = []

    for book in books:
        if book["price"] <= max_price:
            result.append(book)

    return result