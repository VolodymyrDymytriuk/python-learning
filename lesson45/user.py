from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str


@app.post("/users", response_model=UserResponse)
def create_user(user:UserCreate):
    return {
        "id":1,
        "name":user.name,
        "email":user.email
    }