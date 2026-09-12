from fastapi import FastAPI, HTTPException, Path, status

app = FastAPI()

users = [
    {"id": 1, "name": "Ivan", "age": 21},
    {"id": 2, "name": "Olha", "age": 35},
    {"id": 3, "name": "Petro", "age": 40}
]


@app.get("/users/{user_id}")
def get_user(
    user_id: int = Path(gt=0)
):
    for user in users:

        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
