from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Student(BaseModel):
    name: str
    grades: list[int]


@app.post("/students")
def create_student(student: Student):
    return student