from fastapi import FastAPI, HTTPException, Path, status

app = FastAPI()

products = [
    {"id": 1, "name": "Milk", "price": 90},
    {"id": 2, "name": "Juice", "price": 120},
    {"id": 3, "name": "Meat", "price": 250}
]


@app.get("/products/{product_id}")
def get_product(
    product_id: int = Path(ge=1)
):
    for product in products:

        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=" Product not found"
    )
