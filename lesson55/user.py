from fastapi import FastAPI, Query

app = FastAPI()

users = [
    {"id": 1, "name": "Ivan", "age": 21},
    {"id": 2, "name": "Olha", "age": 35},
    {"id": 3, "name": "Petro", "age": 40}
]

@app.get("/users")
def get_users(
    min_age: int | None = Query(default=None, ge=0, le=120)
):
    result = []

    for user in users:

        if min_age is not None and user["age"] < min_age:
            continue

        result.append(user)

    return result