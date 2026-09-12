from fastapi import FastAPI, Query

app = FastAPI()

books = [
    {"id": 1, "title": "Python", "price": 500},
    {"id": 2, "title": "FastAPI", "price": 450},
    {"id": 3, "title": "Backend", "price": 350}
]
@app.get("/books")
def get_books(
    max_price: float | None = Query(default=None, gt=0)
):
    result = []

    for book in books:

        if max_price is not None and book["price"] > max_price:
            continue

        result.append(book)

    return result