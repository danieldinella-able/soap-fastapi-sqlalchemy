from typing import Optional

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
    AsyncSession,
)


class PostgresDBManager:
    def __init__(self):
        self.engine: Optional[AsyncEngine] = None
        self.sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None

    def connect(self, uri: str) -> AsyncEngine:
        # Create async SQLAlchemy engine for PostgreSQL (asyncpg)
        self.engine = create_async_engine(uri, pool_pre_ping=True)
        return self.engine

    def get_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        if not self.engine:
            raise RuntimeError("Engine not initialized. Call connect() first.")
        if not self.sessionmaker:
            self.sessionmaker = async_sessionmaker(
                bind=self.engine,
                autoflush=False,
                expire_on_commit=False,
            )
        return self.sessionmaker

    async def disconnect(self):
        if self.engine:
            await self.engine.dispose()
