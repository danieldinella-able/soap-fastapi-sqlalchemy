"""Supporto OAuth per httpx con refresh automatico del token Bearer."""

import time

from httpx import Auth

from app.core.base.base_http_api_manager import BaseHttpApiManager


class BearerAuth(Auth):
    def __init__(self, manager: "OAuthApiManager"):
        self.manager = manager

    async def async_auth_flow(self, request):
        token = await self.manager._get_token()
        request.headers["Authorization"] = f"Bearer {token}"
        yield request

class OAuthApiManager(BaseHttpApiManager):
    """Base per API con OAuth Bearer.

    Gestisce cache del token ed anticipo di scadenza per sicurezza.
    """
    def __init__(self, base_url):
        super().__init__(base_url, auth=BearerAuth(self))
        self._token = None
        self._token_expires_at = 0.0

    async def _fetch_new_token(self) -> tuple[str, int]:
        """Da implementare nelle sottoclassi: ritorna `(token, expires_in_seconds)`."""
        ...

    async def _get_token(self) -> str:
        now = time.time()
        # se non ho token o è scaduto, ne prendo uno nuovo
        if self._token is None or now >= self._token_expires_at:
            token, expires_in = await self._fetch_new_token()
            self._token = token
            # salvo il timestamp di scadenza
            self._token_expires_at = now + expires_in - 10  # scade 10s prima per sicurezza
        return self._token
