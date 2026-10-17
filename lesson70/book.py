from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel


app = FastAPI()

books = [
    {"id": 1, "title": "Python", "price": 500},
    {"id": 2, "title": "FastAPI", "price": 450},
    {"id": 3, "title": "Django", "price": 600},
    {"id": 4, "title": "SQL", "price": 300},
]

class BookResponse(BaseModel):
    id: int
    title: str
    price: float


class BookListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: list[BookResponse]

class BookCreate(BaseModel):
    title: str
    price: float


@app.post(
    "/books",
    response_model=BookResponse
)
def create_book(book: BookCreate):
    new_book = {
        "id": len(books) + 1,
        "title": book.title,
        "price": book.price
    }

    books.append(new_book)

    return new_book   

@app.get("/books", response_model=BookListResponse)
def get_books(
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
    
    result = books

    if search is not None:
        result = [
            book
            for book in result
            if search.lower() in book["title"].lower()
        ]
        
    if min_price is not None:
        result = [
            book
            for book in result
            if book["price"] >= min_price
        ]
    
    if max_price is not None:
        result = [
            book
            for book in result
            if book["price"] <= max_price
        ]

    total = len(result)
        
    items = result[skip:skip + limit]
        
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "items": items
    }
@app.get(
    "/books/{book_id}",
    response_model=BookResponse
)
def get_book(book_id: int):

    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )