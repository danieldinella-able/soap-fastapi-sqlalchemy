from typing import List
from app.schemas.books import Book
from app.providers.soap_provider import SoapBooksProvider

class BookService:
    def __init__(self):
        self.book_provider = SoapBooksProvider()

    def get_books(self) -> List[Book]:
        # Il tuo provider logga e in caso di errore ritorna [] → qui non serve try/except
        raw = self.book_provider.list_books()
        # Validazione/serializzazione verso il contratto REST
        return [Book(**b) for b in raw]