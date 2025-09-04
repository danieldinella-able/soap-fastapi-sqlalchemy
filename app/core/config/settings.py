"""Impostazioni dell'applicazione basate su variabili d'ambiente.

- Carica `.env` in sviluppo tramite `python-dotenv`.
- Espone configurazioni per Uvicorn e PostgreSQL (uri asincrona `asyncpg`).
"""

from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class UvicornSettings(BaseSettings):
    """Configurazione Uvicorn.

    Legge prefisso `UVICORN_` (es. `UVICORN_PORT`, `UVICORN_RELOAD`).
    """
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    reload: bool = False
    reload_delay: int = 0

    class Config:
        env_prefix = "UVICORN_"

class PostgresSettings(BaseSettings):
    """Configurazione database PostgreSQL asincrono.

    Esempio URI: `postgresql+asyncpg://user:password@localhost:5432/dbname`
    """
    uri: str

    class Config:
        env_prefix = "POSTGRES_"


class AppSettings(BaseSettings):
    """Impostazioni principali dell'app.

    Comprende livelli di log e sottosezioni `uvicorn` e `postgres`.
    """
    log_level: str = "INFO"
    root_log_level: str = "INFO"

    uvicorn: UvicornSettings = UvicornSettings()
    postgres: PostgresSettings = PostgresSettings()

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> AppSettings:
    """Restituisce impostazioni singleton memorizzate in cache."""
    return AppSettings()

settings = get_settings()
