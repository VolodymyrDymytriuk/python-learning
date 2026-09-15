from fastapi import FastAPI, HTTPException, Path, status

app = FastAPI()

products = [
    {"id": 1, "name": "Milk", "price": 90},
    {"id": 2, "name": "Meat", "price": 250},
]

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int = Path(gt=0)
):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)

            return {
                "message": "Product deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )