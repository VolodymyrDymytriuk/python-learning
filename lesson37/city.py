from fastapi import FastAPI

app = FastAPI()

@app.get("/weather")
def weather(city:str):
    return {
        "city": city
    }