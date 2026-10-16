from fastapi import FastAPI, Query
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
    response_model=UserResponse
)
def create_user(user: UserCreate):
    new_user = {
        "id": len(users) + 1,
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


