from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_session_rw
from app.schemas.schemas import OrderOut, OrderIn
from app.services.orders_service import create_order_service

order_router = APIRouter()

@order_router.post("/", response_model=OrderOut, status_code=201)
async def create_order(body: OrderIn, session: AsyncSession = Depends(get_session_rw)):
    order = await create_order_service(session, body.isbn, body.qty)
    return OrderOut(id=order.id, isbn=order.isbn, qty=order.qty)