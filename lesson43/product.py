from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Manufacturer(BaseModel):
    name:str
    country:str

class Product(BaseModel):
    name:str
    price:float
    manufacturer:Manufacturer

@app.post("/products")
def create_product(product:Product):
    return product
