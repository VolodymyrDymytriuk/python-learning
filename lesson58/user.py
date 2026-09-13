from fastapi import FastAPI, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

users = []

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=1, le=120)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if not value[0].isupper():
            raise ValueError("Name must start with uppercase letter")

        return value

class UserResponse(BaseModel):
    id: int
    name: str
    age: int


@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate):

    new_id = max(
        (item["id"] for item in users),
        default=0
    ) + 1

    new_user = {
        "id": new_id,
        "name": user.name,
        "age": user.age
    }

    users.append(new_user)

    return new_user