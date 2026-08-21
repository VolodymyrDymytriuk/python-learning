from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Book(BaseModel):
    name:str=Field(min_length=2, max_length=50)
    pages:int=Field(ge=1, le=5000)
    price:float=Field(gt=0)
    description:str | None = None

@app.post("/books")
def create_book(book:Book):
    return book
