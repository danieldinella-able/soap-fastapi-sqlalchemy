from httpx import BasicAuth

from app.core.base.base_http_api_manager import BaseHttpApiManager


class BasicApiManager(BaseHttpApiManager):
    def __init__(self, base_url: str, username: str, password: str):
        super().__init__(base_url, auth=BasicAuth(username, password))