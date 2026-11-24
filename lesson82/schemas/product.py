from pydantic import BaseModel, Field, field_validator

def clean_product_name(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Product name must be a string")

    value = value.strip()

    if len(value) < 3:
        raise ValueError("Product name must have at least 3 characters")

    if value.lower() == "unknown":
        raise ValueError("Product name cannot be Unknown")

    return value


def check_product_price(value: float) -> float:
    if value == 9999:
        raise ValueError("Price cannot be 9999")

    return value


class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50, description="Product name")
    price: float = Field(gt=0, le=100000, description="Product price")

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        return clean_product_name(value)
    
    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        return check_product_price(value)
    
class ProductUpdate(BaseModel):
    name: str | None = Field(
        default = None,
        min_length=3,
        max_length=50
    )
    price: float | None = Field(
        default=None,
        gt=0,
        le=100000
    )

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if value is None:
            return None
        return  clean_product_name(value)
    
    @field_validator("price", mode="before")
    @classmethod
    def validate_price(cls, value):
        if value is None:
            return None
        return check_product_price(value)

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float

class ProductListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    has_next: bool
    items: list[ProductResponse]