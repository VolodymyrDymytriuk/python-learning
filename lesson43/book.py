from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Author(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int = Field(ge=18, le=100)

class Book(BaseModel):
    title: str = Field(min_length=2, max_length=100)
    price: float = Field(gt=0)
    author: Author

@app.post("/books")
def create_book(book:Book):
    return book
