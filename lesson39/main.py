from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/profile/{name}")
def profile(name:str, age:int=Query(ge=18, le=100)):
    return {
        "name": name,
        "age":age
    }