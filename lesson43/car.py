from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Engine(BaseModel):
    volume:float
    power:int

class Car(BaseModel):
    brand:str
    year:int
    engine:Engine

@app.post("/cars")
def create_car(car:Car):
    return car
