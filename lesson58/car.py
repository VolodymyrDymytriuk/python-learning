from fastapi import FastAPI, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

cars = []

class CarCreate(BaseModel):
    brand: str = Field(min_length=2, max_length=30)
    year: int = Field(ge=1900, le=2030)
    price: float = Field(gt=0)

    @field_validator("brand")
    @classmethod
    def validate_brand(cls, value: str):
        if value.lower() == "unknown":
            raise ValueError("Brand name cannot be unknown")
        return value

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
        (item["id"] for item in cars),
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