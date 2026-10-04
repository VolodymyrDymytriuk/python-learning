from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, Field

app = FastAPI()

products = [
    {"id": 1, "name": "Milk", "price": 90},
    {"id": 2, "name": "Meat", "price": 250},
]

class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=30
    )
    price: float | None = Field(
        default=None,
        gt=0
    )


@app.patch("/products/{product_id}")
def update_product(
    product: ProductUpdate,
    product_id: int = Path(gt=0)
):
    for item in products:
        if item["id"] == product_id:

            update_data = product.model_dump(
                exclude_unset=True
            )

            item.update(update_data)

            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )