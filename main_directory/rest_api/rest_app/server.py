import uvicorn
import os

from app.core.config.settings import settings
from app.core.utils import logger


# Custom Logging Configuration Dictionary
def get_logging_config():
    """Get logging config based on environment"""

    # Base config structure
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {},
        "handlers": {
            "default": {
                "level": "INFO",
                "class": "logging.StreamHandler",
            },
            "access": {
                "level": "INFO",
                "class": "logging.StreamHandler",
            },
            "error": {
                "level": "INFO",
                "class": "logging.StreamHandler",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["access"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["error"],
                "level": "WARNING",
                "propagate": False,
            }
        },
    }

    # Choose formatter based on environment (same logic as in logger.py)
    if os.getenv("PYCHARM_HOSTED"):
        # PyCharm: Pretty JSON
        config["formatters"]["default"] = {
            "()": logger.CustomJsonFormatter,
            "format": "%(timestamp)s %(level)s %(name)s %(message)s",
            "json_indent": 2
        }
    elif logger.is_vscode_environment():
        # VSCode: Colored readable format
        config["formatters"]["default"] = {
            "()": logger.ColoredFormatter,
        }
    else:
        # Production/other: Compact JSON
        config["formatters"]["default"] = {
            "()": logger.CustomJsonFormatter,
            "format": "%(timestamp)s %(level)s %(name)s %(message)s",
        }

    # Apply the same formatter to all handlers
    for handler in config["handlers"].values():
        handler["formatter"] = "default"

    return config


if __name__ == "__main__":
    host = os.getenv("UVICORN_HOST", "0.0.0.0")
    port = int(os.getenv("UVICORN_PORT", 8000))
    workers = int(os.getenv("UVICORN_WORKERS", 10))

    uvicorn.run("app.main:app",
                loop="uvloop",
                host=settings.uvicorn.host,
                port=settings.uvicorn.port,
                log_config=get_logging_config(),
                workers=settings.uvicorn.workers,
                reload=settings.uvicorn.reload,
                reload_delay=settings.uvicorn.reload_delay
                )
