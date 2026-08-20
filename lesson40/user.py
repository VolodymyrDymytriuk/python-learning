from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name:str
    age:int
    email:str
    is_active:bool

@app.post("/users")
def create_user(users:User):
    return users
