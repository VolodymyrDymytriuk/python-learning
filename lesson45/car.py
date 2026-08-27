from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CarCreate(BaseModel):
    brand: str
    year: int
    price: float

class CarResponse(BaseModel):
    id: int
    brand: str
    year: int
    price: float

@app.post("/cars", response_model=CarResponse)
def create_car(car:CarCreate):
    return {
        "id":1,
        "brand":car.brand,
        "year":car.year,
        "price":car.price
    }