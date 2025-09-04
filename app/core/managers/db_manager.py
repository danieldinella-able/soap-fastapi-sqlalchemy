import certifi
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBManager:
    def __init__(self):
        self.client: AsyncIOMotorClient | None = None

    def connect(self, uri: str):
        self.client = AsyncIOMotorClient(
            uri,
            tls=True,
            tlsCAFile=certifi.where()
        )
        return self.client

    def get_database(self, db_name: str):
        if not self.client:
            raise RuntimeError("Mongo client not initialized")
        return self.client[db_name]

    async def disconnect(self):
        if self.client:
            self.client.close()
