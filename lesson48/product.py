from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI()

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)

products = [
    {"id": 1, "name": "Laptop", "price": 35000},
    {"id": 2, "name": "Mouse", "price": 800}
]

@app.post(
        "/products",
        status_code=status.HTTP_201_CREATED
)

def create_product(product: ProductCreate):
    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price
    }
    products.append(new_product)
    return new_product

@app.get("/products")
def get_products():
    return products