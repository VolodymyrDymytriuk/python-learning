from fastapi import FastAPI

app = FastAPI()

@app.get("/users")
def users(skip: int=0, limit: int=10):
    return {
        "skip":skip,
        "limit": limit
    }