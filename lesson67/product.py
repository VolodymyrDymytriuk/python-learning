from fastapi import FastAPI, Query

app = FastAPI()

products = [
    {"id": 1, "name": "Milk", "price": 90},
    {"id": 2, "name": "Meat", "price": 250},
    {"id": 3, "name": "Juice", "price": 120},
    {"id": 4, "name": "Bread", "price": 50},
]

@app.get("/products")
def get_products(
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=50
    ),
    min_price: float | None = Query(
            default=None,
            gt=0
    ),
    max_price: float | None = Query(
        default=None,
        gt=0
    ),
    skip: int = Query(
        default=0,
        ge=0
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100
    )

):
    
    result = products

    if search is not None:
        result = [
            product
            for product in result
            if search.lower() in product["name"].lower()
        ]
        
    if min_price is not None:
        result = [
            product
            for product in result
            if product["price"] >= min_price
        ]
    
    if max_price is not None:
        result = [
            product
            for product in result
            if product["price"] <= max_price
        ]

    total = len(result)
    
    items = result[skip:skip + limit]
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }
