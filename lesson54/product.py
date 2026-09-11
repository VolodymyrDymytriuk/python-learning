from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Milk", "price": 90},
    {"id": 2, "name": "Juice", "price": 120},
    {"id": 3, "name": "Meat", "price": 250}
]

@app.get("/products")
def get_products(min_price: float | None = None):

    if min_price is None:
        return products

    result = []

    for product in products:
        if product["price"] >= min_price:
            result.append(product)

    return result