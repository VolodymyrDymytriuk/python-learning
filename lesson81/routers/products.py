
from fastapi import APIRouter, HTTPException, Query

from schemas.pagination import PaginatedResponse

from schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse
)
from services import product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get(
    "",
    response_model=PaginatedResponse[ProductResponse]
)
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

    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
        status_code=422,
        detail="min_price cannot be greater than max_price"
        )
    return product_service.get_all_products(
        search=search,
        min_price=min_price,
        max_price=max_price,
        skip=skip,
        limit=limit
        )


@router.get("/{product_id}", response_model=ProductResponse,  
            responses={404: {"description": "Product not found"}
    })
def get_product(product_id: int):
    product = product_service.get_product_by_id(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate):
    return product_service.create_product(
        product.model_dump()
    )


@router.put("/{product_id}", response_model=ProductResponse)
def put_product(product_id: int, product_data: ProductCreate):
    product = product_service.update_product(
        product_id,
        product_data.model_dump()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.patch("/{product_id}", response_model=ProductResponse)
def patch_product(product_id: int, product_update: ProductUpdate):
    data = product_update.model_dump(exclude_unset=True)

    if any(value is None for value in data.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null"
        )

    product = product_service.update_product(product_id, data)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int):
    deleted = product_service.delete_product(product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
