from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.repos import repo_get_book, repo_create_order

async def create_order_service(session: AsyncSession, isbn: str, qty: int):
    if qty <= 0:
        raise HTTPException(status_code=400, detail="Invalid quantity")
    book = await repo_get_book(session, isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    order = await repo_create_order(session, isbn, qty)
    return order