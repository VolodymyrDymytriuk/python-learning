from fastapi import FastAPI, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI()

products = []

class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=30)
    price: float = Field(gt=0)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):
        if value.lower() == "test":
            raise ValueError("Product name cannot be test")
        return value

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float


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
        "price": product.price
    }

    products.append(new_product)

    return new_product