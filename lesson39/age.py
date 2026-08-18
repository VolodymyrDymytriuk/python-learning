from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/user")
def user(age:int= Query(ge=18, le=100)):
    return {
        "age": age
    }