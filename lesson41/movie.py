from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Movie(BaseModel):
    title:str=Field(min_length=2, max_length=50)
    year:int=Field(ge=1900, le=2030)
    rating:int=Field(ge=0, le=10)

@app.post("/movies")
def create_movie(movie:Movie):
    return movie
