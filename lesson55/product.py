from fastapi import FastAPI, Query

app = FastAPI()

products = [
    {"id": 1, "name": "Milk", "price": 90},
    {"id": 2, "name": "Juice", "price": 120},
    {"id": 3, "name": "Meat", "price": 250}
]

@app.get("/products")
def get_products(
    min_price: float | None = Query(default=None, ge=0)
):
    result = []

    for product in products:

        if min_price is not None and product["price"] < min_price:
            continue

        result.append(product)

    return result