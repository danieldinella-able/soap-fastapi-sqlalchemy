from functools import lru_cache
from typing import List, Dict, Optional
from zeep import Client, Transport
from zeep.exceptions import Fault, TransportError
from app.core.config.settings import settings
from app.core.utils.logger import log_exception


@lru_cache(maxsize=1)
def _client() -> Client:
    # Zeep è sincrono; configuriamo il timeout del transport.
    return Client(wsdl=settings.soap.wsdl_url, transport=Transport(timeout=settings.soap.timeout))

def _normalize_book(b) -> Dict:
    return {
        "isbn": getattr(b, "isbn", None),
        "title": getattr(b, "title", None),
        "author": getattr(b, "author", None),
        "price": getattr(b, "price", None),
    }

class SoapBooksProvider:
    def list_books(self) -> List[Dict]:
        try:
            books = _client().service.ListBooks()
            return [_normalize_book(b) for b in (books or [])]
        except (Fault, TransportError, Exception) as e:
            log_exception(e)
            return []

    def get_book(self, isbn: str) -> Optional[Dict]:
        try:
            b = _client().service.GetBook(isbn)
            return None if not b else _normalize_book(b)
        except (Fault, TransportError, Exception) as e:
            log_exception(e)
            return None
