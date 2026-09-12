from fastapi import FastAPI, HTTPException, Path, status

app = FastAPI()

cars = [
    {"id": 1, "brand": "Jeep", "price": 45000},
    {"id": 2, "brand": "Subaru", "price": 40000},
    {"id": 3, "brand": "BMW", "price": 50000}
]


@app.get("/cars/{car_id}")
def get_car(
    car_id: int = Path(gt=0)
):
    for car in cars:

        if car["id"] == car_id:
            return car

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Car not found"
    )
