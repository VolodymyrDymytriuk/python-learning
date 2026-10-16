from fastapi import FastAPI, Query
from pydantic import BaseModel

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