from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class CarCreate(BaseModel):
    brand: str = Field(min_length=2, max_length=30)
    price: float = Field(gt=0)

cars = [
    {"id": 1, "brand": "Jeep", "price": 51000},
    {"id": 2, "brand": "BMW", "price": 49000}
]

@app.post(
    "/cars",
    status_code=status.HTTP_201_CREATED
)
def create_car(car: CarCreate):

    new_car = {
        "id": len(cars) + 1,
        "brand": car.brand,
        "price": car.price
    }

    cars.append(new_car)

    return new_car

@app.get("/cars")
def get_cars():
    return cars

@app.get("/cars/{car_id}")
def get_cars(car_id: int):

    for car in cars:

        if car["id"] == car_id:
            return car

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Car not found"
    )

@app.put("/cars/{car_id}")
def update_car(car_id: int, car: CarCreate):

    for item in cars:

        if item["id"] == car_id:

            item["brand"] = car.brand
            item["price"] = car.price
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Car not found"
    )

@app.delete("/cars/{car_id}")
def delete_car(car_id: int):

    for car in cars:

        if car["id"] == car_id:

            cars.remove(car)

            return {
                "message": "Car deleted"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Car not found"
    )