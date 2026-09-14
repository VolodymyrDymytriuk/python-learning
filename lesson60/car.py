from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field

app = FastAPI()

cars = [
    {"id": 1, "brand": "Jeep", "year": 2015, "price": 45000},
    {"id": 2, "brand": "Subaru", "year": 2020, "price": 40000}
]

class CarUpdate(BaseModel):
    brand: str = Field(min_length=2, max_length=30)
    year: int = Field(ge=1900, le=2030)
    price: float = Field(gt=0)

@app.put("/cars/{car_id}")
def update_car(
    car: CarUpdate,
    car_id: int = Path(gt=0)
):
    for item in cars:
        if item["id"] == car_id:
            item["brand"] = car.brand
            item["year"] = car.year
            item["price"] = car.price
            return item
      
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Car not found"
    )
    