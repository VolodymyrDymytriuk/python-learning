from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


class ProductUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)


products = [
    {"id": 1, "name": "Laptop", "price": 35000},
    {"id": 2, "name": "Mouse", "price": 800},
    {"id": 3, "name": "Keyboard", "price": 1500}
]


@app.get("/products")
def get_products():
    return products


@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductUpdate):

    for item in products:

        if item["id"] == product_id:

            item["name"] = product.name
            item["price"] = product.price

            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )