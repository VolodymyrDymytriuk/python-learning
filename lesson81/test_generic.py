from schemas.pagination import PaginatedResponse
from schemas.car import CarResponse

page = PaginatedResponse[CarResponse](
    total=1,
    skip=0,
    limit=10,
    has_next=False,
    items=[
        {
            "id": 1,
            "brand": "Jeep",
            "year": 2015,
            "price": 45000
        }
    ]
)

print(page.model_dump())