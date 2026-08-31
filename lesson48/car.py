from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI()

class CarCreate(BaseModel):
    brand: str = Field(min_length=2, max_length=20)
    year: int = Field(gt=1950, le=2027)
    price: float = Field(gt=0)

cars = [
    {"id": 1, "brand": "Jeep", "year": 2026, "price":51000 },
    {"id": 2, "brand": "BMW", "year": 2025, "price":49000 }
]

@app.post(
        "/cars",
        status_code=status.HTTP_201_CREATED
)

def create_car(car: CarCreate):
    new_car = {
        "id": len(cars) + 1,
        "brand": car.brand,
        "year": car.year,
        "price": car.price
    }
    cars.append(new_car)
    return new_car

@app.get("/cars")
def get_cars():
    return cars