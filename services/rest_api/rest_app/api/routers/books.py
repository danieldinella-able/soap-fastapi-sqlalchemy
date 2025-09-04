from typing import List
from fastapi import APIRouter
from rest_app.schemas.books import Book
from rest_app.services.books import BookService

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/list", response_model=List[Book])
def get_books():
    return BookService().get_books()
