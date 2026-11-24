from fastapi import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    skip: int
    limit: int


def get_pagination(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
) -> PaginationParams:

    return PaginationParams(
        skip=skip,
        limit=limit
    )

class Pagination:
    def __init__(
        self,
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1, le=100)
    ):
        self.skip = skip
        self.limit = limit