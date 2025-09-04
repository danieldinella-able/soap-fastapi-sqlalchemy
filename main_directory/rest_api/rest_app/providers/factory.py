from main_directory.rest_api.rest_app.providers.soap.client import SoapBooksProvider
from main_directory.rest_api.rest_app.providers.base import IBooksProvider  # solo per typing


def get_books_provider() -> IBooksProvider:
    # Ora forziamo SOAP; quando vorrai il mock, qui leggerai BOOKS_PROVIDER
    return SoapBooksProvider()
