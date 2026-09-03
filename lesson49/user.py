from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()


class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(gt=0, le=100)


users = [
    {"id": 1, "name": "Ivan", "age": 21},
    {"id": 2, "name": "Olha", "age": 35}
]



@app.get("/users")
def get_users():
    return users


@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):

    for item in users:

        if item["id"] == user_id:

            item["name"] = user.name
            item["age"] = user.age

            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )