from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.core.managers.state_manager import AppStateManager
from app.core.managers.db_manager import PostgresDBManager
from app.core.utils import logger

logger.configure()

@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.core.utils.logger import log_info
    from app.core.config.settings import settings

    # Codice di inizializzazione
    log_info("Application is loading...")
    db_manager = PostgresDBManager()
    state.db_engine = db_manager.connect(uri=settings.postgres.uri)
    state.sessionmaker = db_manager.get_sessionmaker()

    log_info("Application started!")

    yield
    # Codice di chiusura
    log_info("Application ended!")
    await db_manager.disconnect()


app = FastAPI(lifespan=lifespan)
state = AppStateManager(app)

api_router = APIRouter()

# Lo monto su /api
app.include_router(api_router)

# Configurazione che permette tutte le origini e tutti i metodi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consente tutte le origini
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
