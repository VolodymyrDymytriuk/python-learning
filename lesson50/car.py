from fastapi import FastAPI, HTTPException, status

app = FastAPI()

cars = [
    {"id": 1, "brand": "Jeep", "price": 51000},
    {"id": 2, "brand": "BMW", "price": 49000},
    {"id": 3, "brand": "Subaru", "price": 45000}
]


@app.get("/cars")
def get_cars():
    return cars


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