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

    # Init
    log_info("Application is loading...")
    db_manager = PostgresDBManager()
    state.db_engine = db_manager.connect(uri=settings.postgres.uri)
    state.sessionmaker = db_manager.get_sessionmaker()

    log_info("Application started!")

    yield
    # Shutdown
    log_info("Application ended!")
    await db_manager.disconnect()


app = FastAPI(lifespan=lifespan)
state = AppStateManager(app)

api_router = APIRouter()

# Routers
from main_directory.rest_api.rest_app.api.routers import books as books_router  # noqa: E402
app.include_router(books_router.router, prefix="/api")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
