from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel, Field

app = FastAPI()

products = [
    {"id": 1, "name": "Milk", "price": 90},
    {"id": 2, "name": "Juice", "price": 120}
]

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    price: float = Field(gt=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(product: ProductCreate):

    new_id = max(
        (product["id"] for product in products),
        default=0
    ) + 1

    new_product = {
            "id": new_id,
            "name": product.name,
            "price": product.price
        }
    
    products.append(new_product)
    
    return new_product