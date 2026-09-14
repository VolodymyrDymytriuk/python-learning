from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field

app = FastAPI()

users = [
    {"id": 1, "name": "Ivan", "age": 21},
    {"id": 2, "name": "Olha", "age": 35}
]

class UserUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=1, le=120)

@app.put("/users/{user_id}")
def update_user(
    user: UserUpdate,
    user_id: int = Path(gt=0)
):
    for item in users:
        if item["id"] == user_id:
            item["name"] = user.name
            item["age"] = user.age
            return item
      
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
    
    

    
    

