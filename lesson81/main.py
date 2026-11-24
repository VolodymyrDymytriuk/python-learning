
from fastapi import FastAPI
from routers import cars, products

app = FastAPI(
    title="Car Management API",
    description="Modular FastAPI project - Lesson 78",
    version="1.0.0"
)

app.include_router(cars.router)
app.include_router(products.router)

@app.get("/")
def home():
    return {"message": "Welcome to Car Management API"}
