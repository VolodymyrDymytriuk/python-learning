from fastapi import FastAPI, status
from pydantic import BaseModel, Field, model_validator

app = FastAPI()

cars = []


class CarCreate(BaseModel):
    brand: str = Field(min_length=2, max_length=30)
    min_price: float = Field(gt=0)
    max_price: float = Field(gt=0)

    @model_validator(mode="after")
    def validate_prices(self):
        if self.min_price > self.max_price:
                raise ValueError("min_price cannot be greater than max_price")
        
        return self
        
class CarResponse(BaseModel):
    id: int
    brand: str
    min_price: float
    max_price: float
        
        
@app.post(
        "/cars",
        response_model=CarResponse,
        status_code=status.HTTP_201_CREATED
)
def create_car(car: CarCreate):
        
    new_id = max(
        (item["id"] for item in cars),
        default=0
    ) + 1
        
    new_car = {
        "id": new_id,
        "brand": car.brand,
        "min_price": car.min_price,
        "max_price": car.max_price
    }
        
    cars.append(new_car)
        
    return new_car

       