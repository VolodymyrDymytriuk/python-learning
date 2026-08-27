from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Employee(BaseModel):
    name: str
    position: str

class Company(BaseModel):
    name: str
    employees: list[Employee]


@app.post("/companies")
def create_company(company: Company):
    return company