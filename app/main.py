"""Avvio dell'app FastAPI.

- Gestisce il ciclo di vita (lifespan) per inizializzare/chiudere DB.
- Configura CORS aperto per sviluppo.
- Espone router API e stato applicativo (engine/sessionmaker) tramite AppStateManager.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints.books_endpoint import books_router
from app.api.endpoints.order_endpoint import order_router
from app.core.managers.state_manager import AppStateManager
from app.core.managers.db_manager import PostgresDBManager
from app.core.utils import logger
from app.repositories.seed import create_schema, seed_initial_data

logger.configure()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inizializza risorse all'avvio e le rilascia alla chiusura.

    - Crea l'`AsyncEngine` PostgreSQL da `POSTGRES_URI`.
    - Imposta `sessionmaker` asincrono nell'app state.
    - Alla terminazione, chiude le connessioni del motore.
    """
    from app.core.utils.logger import log_info
    from app.core.config.settings import settings

    # Codice di inizializzazione
    log_info("Application is loading...")
    db_manager = PostgresDBManager()
    state.db_engine = db_manager.connect(uri=settings.postgres.uri)
    state.sessionmaker = db_manager.get_sessionmaker()

    # schema
    await create_schema(state.db_engine)

    #seed
    async with state.sessionmaker() as session:
        await seed_initial_data(session)

    log_info("Application started!")

    yield
    # Codice di chiusura
    log_info("Application ended!")
    await db_manager.disconnect()


app = FastAPI(lifespan=lifespan)
state = AppStateManager(app)

api_router = APIRouter()
api_router.include_router(books_router, prefix="/books", tags=["books"])
api_router.include_router(order_router, prefix="/orders", tags=["orders"])
# Lo monto su /api
app.include_router(api_router, prefix="/api")

# Configurazione che permette tutte le origini e tutti i metodi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consente tutte le origini
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
