from pydantic import BaseModel, Field, field_validator


def clean_brand(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Brand must be a string")

    value = value.strip()

    if len(value) < 2:
        raise ValueError("Brand must have at least 2 characters")

    if value.lower() == "unknown":
        raise ValueError("Brand cannot be Unknown")

    return value


def check_car_price(value: float) -> float:
    if value == 99999:
        raise ValueError("Price cannot be 99999")

    return value


class CarCreate(BaseModel):
    brand: str = Field(min_length=2, max_length=30)
    year: int = Field(ge=1900, le=2027)
    price: float = Field(gt=0, le=1000000)

    @field_validator("brand", mode="before")
    @classmethod
    def validate_brand(cls, value):
        return clean_brand(value)

    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        return check_car_price(value)


class CarUpdate(BaseModel):
    brand: str | None = Field(
        default=None, min_length=2, max_length=30
    )
    year: int | None = Field(
        default=None, ge=1900, le=2027
    )
    price: float | None = Field(
        default=None, gt=0, le=1000000
    )

    @field_validator("brand", mode="before")
    @classmethod
    def validate_brand(cls, value):
        if value is None:
            return None
        return clean_brand(value)

    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        if value is None:
            return None
        return check_car_price(value)


class CarResponse(BaseModel):
    id: int
    brand: str
    year: int
    price: float
