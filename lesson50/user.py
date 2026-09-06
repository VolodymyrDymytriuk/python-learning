from fastapi import FastAPI, HTTPException, status

app = FastAPI()

users = [
    {"id": 1, "name": "Ivan", "age": 21},
    {"id": 2, "name": "Olha", "age": 35},
    {"id": 3, "name": "John", "age": 30}
]


@app.get("/users")
def get_users():
    return users


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