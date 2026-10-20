from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field


app = FastAPI()

products = [
    {"id": 1, "name": "Milk", "price": 90},
    {"id": 2, "name": "Meat", "price": 250},
    {"id": 3, "name": "Juice", "price": 120},
    {"id": 4, "name": "Bread", "price": 50},
]

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float


class ProductListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: list[ProductResponse]

class ProductCreate(BaseModel):
    name: str
    price: float

class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None


@app.post(
    "/products",
    response_model=ProductResponse, status_code=201
)
def create_product(product: ProductCreate):
    
    new_id = max((product["id"] 
                  for product in products ),
                    default = 0
                ) + 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price
    }

    products.append(new_product)

    return new_product

@app.get("/products", response_model=ProductListResponse)
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

@app.get(
    "/products/{product_id}",
    response_model=ProductResponse, responses={404:{"description":"Product not found"}}
)
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )
@app.delete("/products/{product_id}", status_code=204, responses={404: {"description": "Product not found"}})
def delete_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )

@app.put(
    "/products/{product_id}",
    response_model=ProductResponse,
    responses={404: {"description": "Product not found"}}
)
def update_product(product_id: int, product_data: ProductCreate):

    for product in products:
        if product["id"] == product_id:
            product["name"] = product_data.name
            product["price"] = product_data.price

            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )

@app.patch(
    "/products/{product_id}",
    response_model=ProductResponse,
    responses={404: {"description": "Product not found"}}
)
def patch_product(product_id: int, product_update: ProductUpdate):

    for product in products:
        if product["id"] == product_id:

            update_data = product_update.model_dump(
                exclude_unset=True
            )

            if any(value is None for value in update_data.values()):
                raise HTTPException(
                    status_code=422,
                    detail="Fields cannot be null"
                )

            product.update(update_data)

            return product

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )