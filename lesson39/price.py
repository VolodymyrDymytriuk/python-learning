from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/price")
def price(price:float= Query(gt=0, le=100000)):
    return {
        "price": price
    }