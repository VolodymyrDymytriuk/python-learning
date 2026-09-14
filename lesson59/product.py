from fastapi import FastAPI, status
from pydantic import BaseModel, Field, model_validator

app = FastAPI()

products = []


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    price: float = Field(gt=0)
    discount_price: float = Field(gt=0)

    @model_validator(mode="after")
    def validate_discount(self):
        if self.discount_price > self.price:
            raise ValueError("Discount price cannot be greater than price")
        # якщо discount_price > price:
        #     raise ValueError(...)

        return self

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    discount_price: float


@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(product: ProductCreate):

    new_id = max(
        (item["id"] for item in products),
        default=0
    ) + 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "discount_price": product.discount_price
    }

    products.append(new_product)

    return new_product