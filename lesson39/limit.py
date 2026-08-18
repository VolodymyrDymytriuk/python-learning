from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/products")
def products(limit:int=Query(default=10, ge=1, le=50)):
    return {
        "limit": limit
    }