from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0, le=120)


class UserResponse(BaseModel):
    id: int
    name: str
    age: int

users = [
    {"id": 1, "name": "Ivan", "age": 21},
    {"id": 2, "name": "Olha", "age": 35}
]

@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):

    new_id = max(
        (user["id"] for user in users),
        default=0
    ) + 1

    new_user = {
            "id": new_id,
            "name": user.name,
            "age": user.age
        }
    
    users.append(new_user)
    
    return new_user

@app.get(
    "/users/{user_id}",
    response_model=UserResponse
)
def get_user(user_id: int):
    for user in users:
    
         if user["id"] == user_id:
            return user
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

