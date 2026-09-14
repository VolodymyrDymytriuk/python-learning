from fastapi import FastAPI, status
from pydantic import BaseModel, Field, model_validator

app = FastAPI()

users = []


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=18, le=120)

    password: str = Field(min_length=6)
    password_repeat: str = Field(min_length=6)

    @model_validator(mode="after")
    def validate_passwords(self):
        if self.password != self.password_repeat:
            raise ValueError("Passwords do not match")

        # якщо password і password_repeat не однакові
        # викликати:
        #
        # raise ValueError("Passwords do not match")
        return self


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
