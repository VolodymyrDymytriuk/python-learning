from fastapi import FastAPI

app = FastAPI()

@app.get("/search")
def search(query: str="Python"):
    return {
        "query": query
    }