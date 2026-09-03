from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


class CarUpdate(BaseModel):
    brand: str = Field(min_length=2, max_length=30)
    price: float = Field(gt=0)


cars = [
    {"id": 1, "brand": "Jeep", "price": 51000},
    {"id": 2, "brand": "BMW", "price": 49000}
]



@app.get("/cars")
def get_cars():
    return cars


@app.put("/cars/{car_id}")
def update_car(car_id: int, car: CarUpdate):

    for item in cars:

        if item["id"] == car_id:

            item["brand"] = car.brand
            item["price"] = car.price

            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Car not found"
    )