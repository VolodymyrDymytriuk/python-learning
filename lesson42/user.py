from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class User(BaseModel):
    name:str=Field(min_length=2, max_length=30)
    age:int=Field(ge=18, le=100)
    email:str | None = None
    is_active:bool=True

@app.post("/users")
def create_user(user:User):
    return user
