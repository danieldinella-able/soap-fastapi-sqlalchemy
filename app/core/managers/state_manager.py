import asyncio

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient


class AppStateManager:
    def __init__(self, app: FastAPI):
        self._app = app

    @property
    def mongo_client(self) -> AsyncIOMotorClient:
        return getattr(self._app.state, "mongo_client")

    @mongo_client.setter
    def mongo_client(self, mongo_client: AsyncIOMotorClient):
        setattr(self._app.state, "mongo_client", mongo_client)

    @property
    def db(self) -> AsyncIOMotorDatabase:
        return getattr(self._app.state, "db")

    @db.setter
    def db(self, db: AsyncIOMotorDatabase):
        setattr(self._app.state, "db", db)
