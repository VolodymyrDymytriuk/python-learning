from fastapi import FastAPI, HTTPException,status
from pydantic import BaseModel, Field

app = FastAPI()

cars = [
    {"id": 1, "brand": "Jeep", "year": 2015, "price": 45000},
    {"id": 2, "brand": "Subaru", "year": 2020, "price": 40000}
]

class CarCreate(BaseModel):
    brand: str = Field(min_length=2, max_length=30)
    year: int = Field(ge=1900, le=2030 )
    price: float = Field(gt=0)

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

    new_id = max(
        (car["id"] for car in cars),
        default=0
    ) + 1

    new_car = {
            "id": new_id,
            "brand": car.brand,
            "year": car.year,
            "price": car.price
        }
    
    cars.append(new_car)
    
    return new_car