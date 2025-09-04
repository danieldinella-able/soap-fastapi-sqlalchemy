from soap_provider import SoapBooksProvider
from base import IBooksProvider  # solo per typing

def get_books_provider() -> IBooksProvider:
    # Ora forziamo SOAP; quando vorrai il mock, qui leggerai BOOKS_PROVIDER
    return SoapBooksProvider()