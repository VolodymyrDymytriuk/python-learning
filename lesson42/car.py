from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Car(BaseModel):
    brand:str=Field(min_length=2, max_length=30)
    year:int=Field(ge=1950, le=2030)
    price:float=Field(gt=0)
    color:str | None = None
    avaible:bool=True

@app.post("/cars")
def create_car(car:Car):
    return car
