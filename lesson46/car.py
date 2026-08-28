from fastapi import FastAPI, status
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
    
    
@app.post(
    "/cars",
    response_model=CarResponse,
    status_code=status.HTTP_201_CREATED
)

def create_car(car: CarCreate):
    return {
        "id": 10,
        "brand": car.brand,
        "year": car.year,
        "price": car.price
    }