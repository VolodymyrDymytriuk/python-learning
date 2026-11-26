
from typing import Annotated

from fastapi import Depends, HTTPException, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    skip: int
    limit: int


def get_pagination(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
) -> PaginationParams:
    print("1. get_pagination called")

    return PaginationParams(
        skip=skip,
        limit=limit
    )


def get_validated_pagination(
    pagination: Annotated[
        PaginationParams,
        Depends(get_pagination)
    ]
) -> PaginationParams:
    print("2. get_validated_pagination called")

    if pagination.skip > 1000:
        raise HTTPException(
            status_code=422,
            detail="skip cannot be greater than 1000"
        )

    return pagination
