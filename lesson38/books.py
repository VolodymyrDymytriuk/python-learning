from fastapi import FastAPI

app = FastAPI()

@app.get("/books")
def books(limit: int=5):
    return {
        "limit": limit
    }