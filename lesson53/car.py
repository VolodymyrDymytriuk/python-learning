from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class CarCreate(BaseModel):
    brand: str = Field(min_length=2, max_length=30)
    price: float = Field(gt=0)


class CarResponse(BaseModel):
    id: int
    brand: str
    price: float
    
class CarUpdate(BaseModel):
    brand: str | None = Field(default=None, min_length=2, max_length=30)
    price: float | None = Field(default=None, gt=0)

cars = [
    {"id": 1, "brand": "jeep", "price": 45000},
    {"id": 2, "brand": "Subaru", "price": 40000}
]

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
            "price": car.price
        }
    
    cars.append(new_car)
    
    return new_car

@app.get(
    "/cars/{car_id}",
    response_model=CarResponse
)
def get_car(car_id: int):
    for car in cars:
    
         if car["id"] == car_id:
            return car
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Car not found"
        )

@app.patch(
    "/cars/{car_id}",
    response_model=CarResponse
)
def update_car(car_id: int, car: CarUpdate):

    for item in cars:

        if item["id"] == car_id:

            if car.brand is not None:
                item["brand"] = car.brand

            if car.price is not None:
                item["price"] = car.price

            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Car not found"
    )