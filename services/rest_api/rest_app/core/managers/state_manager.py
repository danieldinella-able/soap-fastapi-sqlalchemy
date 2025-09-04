from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession


class AppStateManager:
    def __init__(self, app: FastAPI):
        self._app = app

    @property
    def db_engine(self) -> AsyncEngine:
        return getattr(self._app.state, "db_engine")

    @db_engine.setter
    def db_engine(self, engine: AsyncEngine):
        setattr(self._app.state, "db_engine", engine)

    @property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        return getattr(self._app.state, "sessionmaker")

    @sessionmaker.setter
    def sessionmaker(self, factory: async_sessionmaker[AsyncSession]):
        setattr(self._app.state, "sessionmaker", factory)
