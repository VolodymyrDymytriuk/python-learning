from fastapi import FastAPI, Query

app = FastAPI()

users = [
    {"id": 1, "name": "Ivan", "age": 21},
    {"id": 2, "name": "Olha", "age": 35},
    {"id": 3, "name": "Petro", "age": 40},
    {"id": 4, "name": "Anna", "age": 28},
]

@app.get("/users")
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

    return result