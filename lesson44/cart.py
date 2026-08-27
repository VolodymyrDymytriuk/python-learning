from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Product(BaseModel):
    name: str = Field(min_length=2)
    price: float = Field(gt=0)

class Cart(BaseModel):
    owner: str
    products: list[Product]

@app.post("/cart")
def create_cart(cart: Cart):
    return cart