from fastapi import FastAPI, Query

app = FastAPI()

books = [
    {"id": 1, "title": "Python", "price": 500},
    {"id": 2, "title": "FastAPI", "price": 450},
    {"id": 3, "title": "Django", "price": 600},
    {"id": 4, "title": "SQL", "price": 300},
]

@app.get("/books")
def get_books(
    min_price: float | None = Query(
        default=None,
        gt=0
    ),
    max_price: float | None = Query(
        default=None,
        gt=0
    )
):
    result = books

    if min_price is not None:
        result = [
            book
            for book in result
            if book["price"] >= min_price
        ]

    if max_price is not None:
        result = [
            book
            for book in result
            if book["price"] <= max_price
        ]

    return result