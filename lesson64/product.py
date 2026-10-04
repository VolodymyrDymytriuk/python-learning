from fastapi import FastAPI, Query

app = FastAPI()

products = [
    {"id": 1, "name": "Milk", "price": 90},
    {"id": 2, "name": "Meat", "price": 250},
    {"id": 3, "name": "Juice", "price": 120},
    {"id": 4, "name": "Bread", "price": 50},
]

@app.get("/products")
def get_products(
    min_price: float | None = Query(
        default=None,
        gt=0
    ),
    max_price: float | None = Query(
        default=None,
        gt=0
    )
):
    result = products

    if min_price is not None:
        result = [
            product
            for product in result
            if product["price"] >= min_price
        ]

    if max_price is not None:
        result = [
            product
            for product in result
            if product["price"] <= max_price
        ]

    return result