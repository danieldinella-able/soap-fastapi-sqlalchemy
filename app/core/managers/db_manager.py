"""Gestione connessione PostgreSQL asincrona con SQLAlchemy 2.x.

Offre metodi per creare l'`AsyncEngine`, ottenere un `async_sessionmaker`
e chiudere le risorse in modo sicuro alla terminazione dell'app.
"""

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
        """Crea l'engine asincrono per PostgreSQL (`asyncpg`)."""
        self.engine = create_async_engine(uri, pool_pre_ping=True)
        return self.engine

    def get_sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        """Restituisce un `async_sessionmaker` legato all'engine corrente.

        Solleva `RuntimeError` se l'engine non è stato ancora inizializzato.
        """
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
        """Chiude il connection pool dell'engine, se presente."""
        if self.engine:
            await self.engine.dispose()
