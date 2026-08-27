from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ProductCreate(BaseModel):
    name: str
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float


@app.post("/products", response_model=ProductResponse)
def create_product(product:ProductCreate):
    return {
        "id":1,
        "name":product.name,
        "price":product.price
    }