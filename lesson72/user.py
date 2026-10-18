from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

app = FastAPI()


users = [
    {"id": 1, "name": "Ivan", "age": 21},
    {"id": 2, "name": "Olha", "age": 35},
    {"id": 3, "name": "Petro", "age": 40},
    {"id": 4, "name": "Anna", "age": 28},
]


class UserResponse(BaseModel):
    id: int
    name: str
    age: int


class UserListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: list[UserResponse]

class UserCreate(BaseModel):
    name: str
    age: int

@app.post(
    "/users",
    response_model=UserResponse, status_code=201
)
def create_user(user: UserCreate):

    new_id = max((user["id"] 
                  for user in users),
                    default = 0
                ) + 1

    new_user = {
        "id": new_id,
        "name": user.name,
        "age": user.age
    }

    users.append(new_user)

    return new_user

@app.get(
    "/users",
    response_model=UserListResponse
)
def get_users(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=50
    ),
    min_age: int | None = Query(
        default=None,
        ge=1,
        le=120
    ),
    max_age: int | None = Query(
        default=None,
        ge=1,
        le=120
    ),
    skip: int = Query(
        default=0,
        ge=0
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100
    )
):
    result = users

    if search is not None:
        result = [
            user
            for user in result
            if search.lower() in user["name"].lower()
        ]

    if min_age is not None:
        result = [
            user
            for user in result
            if user["age"] >= min_age
        ]

    if max_age is not None:
        result = [
            user
            for user in result
            if user["age"] <= max_age
        ]

    total = len(result)

    items = result[skip:skip + limit]

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }

@app.get(
    "/users/{user_id}",
    response_model=UserResponse, responses={404:{"description":"User not found"}}
)
def get_user(user_id: int):

    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

@app.delete("/users/{user_id}", status_code=204, responses={404: {"description": "User not found"}})
def delete_user(user_id: int):

    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

@app.put(
    "/users/{user_id}",
    response_model=UserResponse,
    responses={404: {"description": "User not found"}}
)
def update_user(user_id: int, user_data: UserCreate):

    for user in users:
        if user["id"] == user_id:
            user["name"] = user_data.name
            user["age"] = user_data.age

            return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )