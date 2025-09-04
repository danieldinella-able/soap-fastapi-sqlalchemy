from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class UvicornSettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    reload: bool = False
    reload_delay: int = 0

    class Config:
        env_prefix = "UVICORN_"

class MongoSettings(BaseSettings):
    uri: str
    db_name: str = "euroimmobiliare"

    class Config:
        env_prefix = "MONGO_"


class AppSettings(BaseSettings):
    log_level: str = "INFO"
    root_log_level: str = "INFO"

    uvicorn: UvicornSettings = UvicornSettings()
    mongo: MongoSettings = MongoSettings()

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> AppSettings:
    return AppSettings()

settings = get_settings()
