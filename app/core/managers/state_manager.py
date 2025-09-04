"""Accessor semplice per lo stato condiviso dell'app FastAPI.

Conserva riferimenti a `db_engine` e `sessionmaker` nell'`app.state`.
"""

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession


class AppStateManager:
    def __init__(self, app: FastAPI):
        self._app = app

    @property
    def db_engine(self) -> AsyncEngine:
        """Restituisce l'`AsyncEngine` configurato nello stato dell'app."""
        return getattr(self._app.state, "db_engine")

    @db_engine.setter
    def db_engine(self, engine: AsyncEngine):
        """Imposta l'`AsyncEngine` nello stato dell'app."""
        setattr(self._app.state, "db_engine", engine)

    @property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        """Restituisce l'`async_sessionmaker` dallo stato dell'app."""
        return getattr(self._app.state, "sessionmaker")

    @sessionmaker.setter
    def sessionmaker(self, factory: async_sessionmaker[AsyncSession]):
        """Imposta l'`async_sessionmaker` nello stato dell'app."""
        setattr(self._app.state, "sessionmaker", factory)
