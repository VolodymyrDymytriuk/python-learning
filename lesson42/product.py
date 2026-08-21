from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Product(BaseModel):
    name:str=Field(min_length=3, max_length=50)
    price:float=Field(gt=0)
    description:str | None = None
    in_stock:bool=True

@app.post("/products")
def create_product(product:Product):
    return product
