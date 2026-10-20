from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

cars = [
    {"id": 1, "brand": "Jeep", "year": 2015, "price": 45000},
    {"id": 2, "brand": "Subaru", "year": 2020, "price": 40000},
    {"id": 3, "brand": "BMW", "year": 2023, "price": 60000},
    {"id": 4, "brand": "Volvo", "year": 2018, "price": 35000},
]

class CarResponse(BaseModel):
    id: int
    brand: str
    year: int
    price: float


class CarListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: list[CarResponse]

class CarCreate(BaseModel):
    brand: str = Field(min_length=2, max_length=30, description="Car brand")
    year: int = Field(ge=1900, le=2027, description="Car year")
    price: float = Field(gt=0, le=1000000, description="Car price")

class CarUpdate(BaseModel):
    brand: str | None = Field(
        default=None,
        min_length=2,
        max_length=30
    )
    year: int | None = Field(
        default=None,
        ge=1900,
        le=2027
    )
    price: float | None = Field(
        default=None,
        gt=0,
        le=1000000
    )
    
@app.post(
    "/cars",
    response_model=CarResponse, status_code=201
)
def create_car(car: CarCreate):
    new_id = max((car["id"] for car in cars ),
                  default = 0
                  ) + 1
    new_car = {
        "id": new_id,
        "brand": car.brand,
        "year": car.year,
        "price": car.price
    }

    cars.append(new_car)

    return new_car  

@app.get("/cars", response_model=CarListResponse)
def get_cars(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=50
    ),
    min_year: int | None = Query(
            default=None,
            ge=1900,
            le=2027
    ),
    max_year: int | None = Query(
            default=None,
            ge=1900,
            le=2027
    ),
    skip: int = Query(
            default=0,
            ge=0
    ),
    limit: int = Query(
            default=10,
            ge=1,
            le=100
        )
):
    
    result = cars

    if search is not None:
        result = [
            car
            for car in result
            if search.lower() in car["brand"].lower()
        ]
        
    if min_year is not None:
        result = [
            car
            for car in result
            if car["year"] >= min_year
        ]
    
    if max_year is not None:
        result = [
            car
            for car in result
            if car["year"] <= max_year
        ]

    total = len(result)
            
    items = result[skip:skip + limit]
            
    return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "items": items
    }

@app.get(
    "/cars/{car_id}",
    response_model=CarResponse, responses={404:{"description":"Car not found"}}
)
def get_car(car_id: int):

    for car in cars:
        if car["id"] == car_id:
            return car

    raise HTTPException(
        status_code=404,
        detail="Car not found"
    )

@app.delete("/cars/{car_id}", status_code=204, responses={404: {"description": "Car not found"}})
def delete_car(car_id: int):

    for car in cars:
        if car["id"] == car_id:
            cars.remove(car)
            return

    raise HTTPException(
        status_code=404,
        detail="Car not found"
    )
@app.put(
    "/cars/{car_id}",
    response_model=CarResponse,
    responses={404: {"description": "Car not found"}}
)
def update_car(car_id: int, car_data: CarCreate):

    for car in cars:
        if car["id"] == car_id:
            car["brand"] = car_data.brand
            car["year"] = car_data.year
            car["price"] = car_data.price

            return car

    raise HTTPException(
        status_code=404,
        detail="Car not found"
    )

@app.patch(
    "/cars/{car_id}",
    response_model=CarResponse,
    responses={404: {"description": "Car not found"}}
)
def patch_car(car_id: int, car_update: CarUpdate):

    for car in cars:
        if car["id"] == car_id:

            update_data = car_update.model_dump(
                exclude_unset=True
            )

            if any(value is None for value in update_data.values()):
                raise HTTPException(
                    status_code=422,
                    detail="Fields cannot be null"
                )

            car.update(update_data)

            return car

    raise HTTPException(
        status_code=404,
        detail="Car not found"
    )