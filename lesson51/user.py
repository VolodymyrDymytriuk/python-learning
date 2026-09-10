from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0, le=120)

users = [
    {"id": 1, "name": "Ivan", "age": 21},
    {"id": 2, "name": "Olha", "age": 35}
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

@app.get("/users/{user_id}")
def get_users(user_id: int):

    for user in users:

        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserCreate):

    for item in users:

        if item["id"] == user_id:

            item["name"] = user.name
            item["age"] = user.age
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    for user in users:

        if user["id"] == user_id:

            users.remove(user)

            return {
                "message": "User deleted"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )