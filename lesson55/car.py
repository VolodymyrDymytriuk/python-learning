from fastapi import FastAPI, Query

app = FastAPI()

cars = [
    {"id": 1, "brand": "Jeep", "price": 45000},
    {"id": 2, "brand": "Subaru", "price": 40000},
    {"id": 3, "brand": "BMW", "price": 50000}
]

@app.get("/cars")
def get_cars(
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0)
):
    result = []

    for car in cars:

        if min_price is not None and car["price"] < min_price:
            continue
        if max_price is not None and car["price"] > max_price:
            continue

        result.append(car)

    return result