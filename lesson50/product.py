from fastapi import FastAPI, HTTPException, status

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 35000},
    {"id": 2, "name": "Mouse", "price": 800},
    {"id": 3, "name": "Keyboard", "price": 1500}
]


@app.get("/products")
def get_products():
    return products


@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for product in products:

        if product["id"] == product_id:

            products.remove(product)

            return {
                "message": "Product deleted"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )