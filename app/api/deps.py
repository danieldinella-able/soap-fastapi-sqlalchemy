from typing import AsyncGenerator
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session_ro(request: Request) -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = request.app.state.sessionmaker
    async with SessionLocal() as session:
        yield session

async def get_session_rw(request: Request) -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = request.app.state.sessionmaker
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise 