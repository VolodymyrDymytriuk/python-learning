from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Product(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)


class Order(BaseModel):
    customer: str = Field(min_length=2)
    products: list[Product]


@app.post("/orders")
def create_order(order: Order):
    return order