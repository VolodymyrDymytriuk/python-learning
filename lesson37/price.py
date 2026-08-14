from fastapi import FastAPI

app = FastAPI()

@app.get("/price")
def price(product:str, price:float):
    return {
        "product": product,
        "price": price
    }