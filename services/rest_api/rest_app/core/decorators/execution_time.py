import inspect
import time
import functools

from app.core.utils.logger import log_info


def execution_time(func):
    # 1) Async generator (async def ... yield)
    if inspect.isasyncgenfunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                async for item in func(*args, **kwargs):
                    yield item
            finally:
                end = time.perf_counter()
                log_info(f"Tempo di esecuzione di '{func.__name__}': {end - start:.4f} secondi")
        return wrapper

    # 2) Coroutine (async def ... return)
    if inspect.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            end = time.perf_counter()
            log_info(f"Tempo di esecuzione di '{func.__name__}': {end - start:.4f} secondi")
            return result
        return wrapper

    # 3) Sync generator (def ... yield)
    if inspect.isgeneratorfunction(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                for item in func(*args, **kwargs):
                    yield item
            finally:
                end = time.perf_counter()
                log_info(f"Tempo di esecuzione di '{func.__name__}': {end - start:.4f} secondi")
        return wrapper

    # 4) Regular sync function
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        log_info(f"Tempo di esecuzione di '{func.__name__}': {end - start:.4f} secondi")
        return result
    return wrapper
