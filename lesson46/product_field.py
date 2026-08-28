from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI()

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
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
    return {
        "id": 1,
        "name": product.name,
        "price": product.price
    }