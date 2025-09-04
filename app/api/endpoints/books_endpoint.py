from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import BookOut
from app.api.deps import get_session_ro
from app.repositories.repos import repo_list_books

books_router = APIRouter()

@books_router.get("/", response_model=list[BookOut])
async def list_books(session: AsyncSession = Depends(get_session_ro)):
    books = await repo_list_books(session)
    return [BookOut.model_validate(b.__dict__) for b in books]