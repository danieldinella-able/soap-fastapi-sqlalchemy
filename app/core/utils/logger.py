"""Configurazione logging dell'applicazione.

- In locale: formato leggibile (VSCode) o JSON ben indentato (PyCharm).
- In altri ambienti: JSON compatto per log strutturati.
- Evitare di loggare dati sensibili.
"""

import logging
import os
from datetime import datetime, timezone
import traceback
from pythonjsonlogger import json

from app.core.config.settings import settings

root_logger = logging.getLogger()
app_logger = root_logger.getChild("app")
httpx_logger = logging.getLogger("httpx")

class CustomJsonFormatter(json.JsonFormatter):
    """Formatter JSON con timestamp ISO e stacktrace leggibile."""

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            # this doesn't use record.created, so it is slightly off
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname
        # Pretty‑format exceptions for easier reading in JSON logs
        if record.exc_info:
            exc_type, exc_value, exc_tb = record.exc_info
            log_record["exc_type"] = exc_type.__name__
            log_record["exc_message"] = str(exc_value)
            # strip the “\n” off each line so PyCharm doesn’t print the escapes
            log_record["stacktrace"] = [
                line for part in traceback.format_exception(exc_type, exc_value, exc_tb)
                for line in part.splitlines()  # split on *all* newlines
                if line  # and drop empty strings
            ]
            log_record.pop("exc_info", None)

class ColoredFormatter(logging.Formatter):
    """Formatter colorato per leggibilità in VSCode."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green  
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to level name
        level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        colored_level = f"{level_color}{record.levelname}{self.COLORS['RESET']}"
        
        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created, timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        
        # Create a nice formatted message
        formatted_msg = f"{timestamp} | {colored_level:<15} | {record.name:<10} | {record.getMessage()}"
        
        # Handle exceptions
        if record.exc_info:
            formatted_msg += f"\n{self.formatException(record.exc_info)}"
            
        return formatted_msg
        
def is_vscode_environment():
    """Rileva se il processo gira in VSCode."""
    return (
        os.getenv("VSCODE_PID") is not None or 
        os.getenv("TERM_PROGRAM") == "vscode" or
        "vscode" in os.getenv("TERM_PROGRAM_VERSION", "").lower()
    )


def configure():
    """Configura i logger root/app/httpx con il formatter più adatto all'ambiente."""
    payload = {}
    log_handler = logging.StreamHandler()
    
    # Choose formatter based on environment
    if os.getenv("PYCHARM_HOSTED"):
        # PyCharm: Pretty JSON
        payload['json_indent'] = 2
        formatter = CustomJsonFormatter("%(timestamp)s %(level)s %(name)s %(message)s", **payload)
    elif is_vscode_environment():
        # VSCode: Colored readable format
        formatter = ColoredFormatter()
    else:
        # Production/other: Compact JSON
        formatter = CustomJsonFormatter("%(timestamp)s %(level)s %(name)s %(message)s", **payload)
    
    log_handler.setFormatter(formatter)
    root_logger.addHandler(log_handler)
    root_logger.setLevel(settings.root_log_level)
    app_logger.setLevel(settings.log_level)
    httpx_logger.setLevel(logging.WARNING)


def log_info(message):
    """Log di livello INFO."""
    app_logger.info(message)

def log_error(message):
    """Log di livello ERROR."""
    app_logger.error(message)

def log_warning(message):
    """Log di livello WARNING."""
    app_logger.warning(message)

def log_exception(message):
    """Logga un'eccezione con stacktrace."""
    app_logger.exception(message)

def log_debug(message):
    """Log di livello DEBUG."""
    app_logger.debug(message)
