from fastapi import FastAPI, HTTPException, status

app = FastAPI()

cars = [
    {"id": 1, "brand": "Jeep"},
    {"id": 2, "brand": "Toyota"},
    {"id": 3, "brand": "Subaru"}
]

@app.get("/cars/{car_id}")
def get_car(car_id: int):

    for car in cars:
        if car["id"] == car_id:
            return car

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Car not found"
    )