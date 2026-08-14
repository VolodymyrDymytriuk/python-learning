from fastapi import FastAPI

app = FastAPI()

@app.get("/calculate")
def calculate(a:int, b:int):
    return {
        "result":a*b
    }