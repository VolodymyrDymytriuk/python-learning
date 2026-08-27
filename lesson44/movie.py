from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Movie(BaseModel):
    name: str 
    genres: list[str]

@app.post("/movies")
def create_movie(movie:Movie):
    return movie