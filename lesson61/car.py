from fastapi import FastAPI, HTTPException, Path, status

app = FastAPI()

cars = [
    {"id": 1, "brand": "Jeep", "year": 2015, "price": 45000},
    {"id": 2, "brand": "Subaru", "year": 2020, "price": 40000},
]

@app.delete("/cars/{car_id}")
def delete_car(
    car_id: int = Path(gt=0)
):
    for car in cars:
        if car["id"] == car_id:
            cars.remove(car)

            return {
                "message": "Car deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Car not found"
    )