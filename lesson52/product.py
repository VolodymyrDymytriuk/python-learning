from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

products = [
    {"id": 1, "name": "Milk", "price": 90},
    {"id": 2, "name": "Juice", "price": 120}
]

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

@app.get(
    "/products/{product_id}",
    response_model=ProductResponse
)
def get_product(product_id: int):
    for product in products:
    
         if product["id"] == product_id:
            return product
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )