from sqlalchemy import select, insert
from .models import BookORM, OrderORM
from sqlalchemy.ext.asyncio import AsyncSession

async def repo_list_books(session: AsyncSession):
    res = await session.execute(select(BookORM))
    return res.scalars().all()

async def repo_get_book(session: AsyncSession, isbn: str):
    res = await session.execute(select(BookORM).where(BookORM.isbn == isbn))
    return res.scalar_one_or_none()

async def repo_create_order(session: AsyncSession, isbn: str, qty: int) -> OrderORM:
    order = OrderORM(isbn=isbn, qty=qty)
    session.add(order)
    # commit gestito dalla dependency RW
    await session.flush()   # per avere l'id
    await session.refresh(order)
    return order