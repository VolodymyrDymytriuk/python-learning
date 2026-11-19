
from fastapi import APIRouter, HTTPException

from schemas.car import CarCreate, CarUpdate, CarResponse
from services import car_service


router = APIRouter(
    prefix="/cars",
    tags=["Cars"]
)


@router.get("", response_model=list[CarResponse])
def get_cars():
    return car_service.get_all_cars()


@router.get(
    "/{car_id}",
    response_model=CarResponse,
    responses={
        404: {"description": "Car not found"}
    }
)
def get_car(car_id: int):
    car = car_service.get_car_by_id(car_id)

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return car


@router.post("", response_model=CarResponse, status_code=201)
def create_car(car: CarCreate):
    return car_service.create_car(
        car.model_dump()
    )


@router.put("/{car_id}", response_model=CarResponse)
def put_car(car_id: int, car_data: CarCreate):
    car = car_service.update_car(
        car_id,
        car_data.model_dump()
    )

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return car


@router.patch("/{car_id}", response_model=CarResponse)
def patch_car(car_id: int, car_update: CarUpdate):
    data = car_update.model_dump(exclude_unset=True)

    if any(value is None for value in data.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null"
        )

    car = car_service.update_car(car_id, data)

    if car is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )

    return car


@router.delete("/{car_id}", status_code=204)
def delete_car(car_id: int):
    deleted = car_service.delete_car(car_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Car not found"
        )
