from fastapi import FastAPI

app = FastAPI()

users = [
    {"id": 1, "name": "Ivan", "age": 21},
    {"id": 2, "name": "Olha", "age": 35},
    {"id": 3, "name": "Petro", "age": 40}
]
@app.get("/users")
def get_users(min_age: int | None = None):

    if min_age is None:
        return users

    result = []

    for user in users:
        if user["age"] >= min_age:
            result.append(user)

    return result