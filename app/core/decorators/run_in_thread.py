"""Decorator per eseguire funzioni CPU/IO-bound in thread dal contesto async."""

import asyncio
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

def run_in_thread(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(executor, lambda: func(*args, **kwargs))
    return wrapper
