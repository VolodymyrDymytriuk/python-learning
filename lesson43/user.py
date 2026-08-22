from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Address(BaseModel):
    city:str
    country:str

class User(BaseModel):
    name:str
    age:int
    address:Address

@app.post("/users")
def create_user(user:User):
    return user
