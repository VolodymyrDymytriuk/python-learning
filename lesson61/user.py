from fastapi import FastAPI, HTTPException, Path, status

app = FastAPI()

users = [
    {"id": 1, "name": "Ivan", "age": 21},
    {"id": 2, "name": "Olha", "age": 35},
]

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int = Path(gt=0)
):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)

            return {
                "message": "User deleted successfully"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
