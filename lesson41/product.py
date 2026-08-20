from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Product(BaseModel):
    name:str=Field(min_length=3, max_length=30)
    price:float=Field(gt=0, le=100000)
    in_stock:bool

@app.post("/products")
def create_product(product:Product):
    return product
