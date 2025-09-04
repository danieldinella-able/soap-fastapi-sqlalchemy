"""Classe base per manager applicativi con helper di risposta standard."""

from app.core.base.base_response import BaseResponse


class BaseManager:
    def base_success(self, payload=None):
        """Componi una `BaseResponse` di successo."""
        return BaseResponse.success(payload=payload)


    def base_error(self, message: str = None, payload=None):
        """Componi una `BaseResponse` di errore con messaggio."""
        return BaseResponse.error(message=message, payload=payload)
