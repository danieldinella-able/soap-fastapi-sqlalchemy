from typing import List
from fastapi import APIRouter
from app.schemas.books import Book
from app.services.books_service import BookService

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/list", response_model=List[Book])
def get_books():
    return BookService().get_books()