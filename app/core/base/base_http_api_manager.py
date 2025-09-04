"""Base astratta per manager HTTP asincroni basati su httpx.

- Gestisce `AsyncClient` con base URL, auth e header di default.
- Espone `_make_request` e gestione errori standardizzata in `BaseResponse`.
"""

from abc import ABC  # Per definire classi astratte
from http import HTTPMethod

from httpx import AsyncClient, HTTPStatusError, Auth

from app.core.base.base_manager import BaseManager
from app.core.base.base_response import BaseResponse
from app.core.utils.logger import log_exception


class BaseHttpApiManager(ABC, BaseManager):
    """Classe base per integrazioni HTTP.

    Inizializza una sessione httpx con base URL, eventuale `Auth` e headers.
    """
    def __init__(self,
                 base_url: str,
                 auth: Auth|None=None,
                 default_headers: dict|None = None):
        self._init_http_client(base_url=base_url, auth=auth, default_headers=default_headers)

    def _init_http_client(self, base_url: str, auth: Auth|None=None, default_headers: dict|None =None):
        self._base_url = base_url
        self._session = AsyncClient(
            base_url=base_url,
            auth=auth,
            headers=default_headers or {"Content-Type": "application/json"}
        )

    # def __init__(self, base_url):
    #     self._base_url = base_url
    #     self._session = AsyncClient(headers=self._get_default_headers())
    #
    # @abstractmethod
    # async def _get_token(self) -> str:
    #     # Ogni sottoclasse deve implementarlo per settare il proprio token
    #     return ''


    # async def _get_default_headers(self) -> dict:
    #     # Effettuare l'override in caso di default header diverso
    #     token = await self._get_token()
    #     return {
    #         "Authorization": f"Bearer {token}",
    #         "Content-Type": "application/json"
    #     }

    async def _make_request(self, method: HTTPMethod, url=None, endpoint: str='', data=None, json=None, query_params=None, custom_headers=None) -> BaseResponse:
        """Esegue una richiesta HTTP e mappa la risposta in `BaseResponse`.

        Fornisce gestione errori comune e supporto a `data/json/params`.
        """
        if url is None:
            url = f"{self._base_url}{endpoint}"

        # Se sono presenti header custom, aggiorno la sessione temporaneamente
        if custom_headers:
            # TODO vedere se sovrascrive o aggiunge
            self._session.headers.update(custom_headers)

        request_payload = {
            key: value for key, value in {
                'data': data,
                'json': json,
                'params': query_params
            }.items() if value is not None  # Manteniamo solo i valori validi
        }

        response = None
        try:
            response = await self._session.request(method=method, url=url, timeout=20, **request_payload)
            response.raise_for_status()  # Solleva un'eccezione per errori HTTP

            # TODO Gestire il response, potrebbe non essere un json (solo text o byte)
            return self.base_success(payload=response.json())

        except HTTPStatusError:
            return self._handle_api_error(response)

        except RuntimeError as e:
            return self._handle_api_error(response)

        except Exception as e:
            log_exception(e)

    # TODO Wrappare funzioni tipo request_get, request_post ecc ecc

    def _handle_api_error(self, response) -> BaseResponse:
        """Mappa gli status HTTP più comuni in messaggi di errore standard."""
        if response.status_code == 400:
            return self.base_error(message="Bad request")

        if response.status_code == 401:
            return self.base_error(message="Unauthorized")

        if response.status_code == 403:
            return self.base_error(message="Authentication error")

        if response.status_code == 404:
            return self.base_error(message="Resource not found")

        if response.status_code == 429:  # Too Many Requests
            return self.base_error(message="Too Many Requests")

        elif response.status_code >= 500:  # Errore del server
            return self.base_error(message="Generic server error")

        return self.base_error(message=f"HTTP error: {response.status_code}")


    # TODO Funzione che fa una download da un chiamata GET

    # TODO FUnzione POST multipart
