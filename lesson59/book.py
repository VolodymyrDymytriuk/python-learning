from fastapi import FastAPI, status
from pydantic import BaseModel, Field, model_validator

app = FastAPI()

books = []

class BookCreate(BaseModel):
    title: str = Field(min_length=2, max_length=60)
    pages: int = Field(gt=0)
    read_pages: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_pages(self):
        if self.read_pages > self.pages:
                    raise ValueError("Read pages cannot be greater than pages")

        return self

class BookResponse(BaseModel):
    id: int
    title: str
    pages: int
    read_pages: int


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
        "pages": book.pages,
        "read_pages": book.read_pages
    }

    books.append(new_book)

    return new_book

