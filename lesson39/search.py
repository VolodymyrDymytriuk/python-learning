from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/search")
def search(query:str= Query(default="Python", min_length=3, max_length=20)):
    return {
        "query": query
    }