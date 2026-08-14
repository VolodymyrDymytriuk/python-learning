from fastapi import FastAPI

app = FastAPI()

@app.get("/profile/{name}")
def profile(name:str, age:int):
    return {
        "name": name,
        "age": age
    }