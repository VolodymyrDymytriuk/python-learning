from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI()

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0, le=100)

users = [
    {"id": 1, "name": "Ivan", "age": 21},
    {"id": 2, "name": "Olha", "age":35 }
]

@app.post(
        "/users",
        status_code=status.HTTP_201_CREATED
)

def create_user(user: UserCreate):
    new_user = {
        "id": len(users) + 1,
        "name": user.name,
        "age": user.age
    }
    users.append(new_user)
    return new_user

@app.get("/users")
def get_users():
    return users