from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.models import Base, BookORM

async def create_schema(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def seed_initial_data(session: AsyncSession) -> None:
    # idempotent: semina solo se vuoto
    existing = await session.execute(select(BookORM.isbn).limit(1))
    if existing.scalar_one_or_none():
        return
    session.add_all([
        BookORM(isbn="9780132350884", title="Clean Code", price=39.99),
        BookORM(isbn="9781492055020", title="Designing Data-Intensive Applications", price=54.90),
        BookORM(isbn="9781617294136", title="Spring in Action", price=44.00),
    ])
    await session.commit()