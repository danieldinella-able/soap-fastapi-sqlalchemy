from typing import List
from main_directory.rest_api.rest_app.schemas.books import Book
from main_directory.rest_api.rest_app.providers.soap.client import SoapBooksProvider

class BookService:
    def __init__(self):
        self.book_provider = SoapBooksProvider()

    def get_books(self) -> List[Book]:
        raw = self.book_provider.list_books()
        return [Book(**b) for b in raw]
