
from fastapi import APIRouter, HTTPException

from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from services import product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("", response_model=list[ProductResponse])
def get_products():
    return product_service.get_all_products()


@router.get("/{product_id}", response_model=ProductResponse,  
            responses={404: {"description": "Car not found"}
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
