from fastapi import FastAPI, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

books = []

class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=60)
    price: float = Field(gt=0, le=10000)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        if value.isdigit():
            raise ValueError("Title name error")
        return value

class BookResponse(BaseModel):
    id: int
    title: str
    price: float


@app.post(
    "/books",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(book: BookCreate):

    new_id = max(
        (item["id"] for item in books),
        default=0
    ) + 1

    new_book = {
        "id": new_id,
        "title": book.title,
        "price": book.price
    }

    books.append(new_book)

    return new_book