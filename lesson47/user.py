from fastapi import FastAPI, HTTPException, status

app = FastAPI()

users = [
    {"id": 1, "name": "Ivan"},
    {"id": 2, "name": "Anna"},
    {"id": 3, "name": "John"}
]

@app.get("/users/{user_id}")
def get_user(user_id: int):

    for user in users:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )