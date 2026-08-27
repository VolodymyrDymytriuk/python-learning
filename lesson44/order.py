from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    name: str
    price: float


class Order(BaseModel):
    customer: str
    products: list[Product]


@app.post("/orders")
def create_order(order: Order):
    return order