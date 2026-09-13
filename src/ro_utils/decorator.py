import asyncio
import logging
import threading
import time
from collections.abc import Callable
from functools import wraps
from typing import Any

logger = logging.getLogger(__name__)


def continue_when_error(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Catch any exception during function execution, log it, and return None.
    """

    @wraps(func)
    def fn(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error("Error in %s: %s", func.__name__, e)

    return fn


def retry_when_error(
    func: Callable[..., Any] | None = None, *, reraise: bool = False
) -> Callable[..., Any]:
    """
    Retry when error occurs, default 3 times.
    """

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for k in range(3):
                try:
                    return fn(*args, **kwargs)
                except Exception:
                    if k == 2:
                        logger.exception("Failed after 3 retries in %s", fn.__name__)
                        if reraise:
                            raise
            return None

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


def async_retry_when_error(
    func: Callable[..., Any] | None = None, *, reraise: bool = False
) -> Callable[..., Any]:
    """
    Retry async function when error occurs, default 3 times.
    """

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(3):
                try:
                    return await fn(*args, **kwargs)
                except Exception:
                    if attempt == 2:
                        logger.exception("Failed after 3 retries in %s", fn.__name__)
                        if reraise:
                            raise
            return None

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


def async_retry_when_error_with_params(
    max_attempts: int = 3, backoff_factor: float = 1, reraise: bool = False
) -> Callable[..., Any]:
    """
    Retry async function with custom attempts, exponential backoff, and optional reraise.
    """

    def retry_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        logger.exception(
                            "Failed after %d attempts in %s", max_attempts, func.__name__
                        )
                        if reraise:
                            raise
                        return None
                    delay = backoff_factor * (2 ** (attempt - 1))
                    logger.warning(
                        "Caught exception %s in %s. Retrying in %s seconds...",
                        e,
                        func.__name__,
                        delay,
                    )
                    await asyncio.sleep(delay)
            return None

        return wrapper

    return retry_decorator


def retry_when_error_with_params(
    times: int = 5,
    delay: float = 0,
    reraise: bool = False,
    **kwargs: Any,
) -> Callable[..., Any]:
    """
    Retry when error occurs with custom times and delay between attempts.
    """
    times = int(kwargs.get("times", times))
    delay = float(kwargs.get("delay", delay))

    def retry_when_error_occur(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def fn(*args: Any, **kwargs: Any) -> Any:
            for k in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if k == times - 1:
                        logger.exception("Failed after %d attempts in %s", times, func.__name__)
                        if reraise:
                            raise
                        return None
                    if delay > 0:
                        time.sleep(delay)
            return None

        return fn

    return retry_when_error_occur


def retry_when_error_with_times(times: int, reraise: bool = False) -> Callable[..., Any]:
    """
    Retry when error occurs with specified times.
    """
    return retry_when_error_with_params(times=times, reraise=reraise)


def singleton(cls: type) -> Callable[..., Any]:
    """
    Thread-safe singleton class decorator.
    """
    instances: dict[type, Any] = {}
    lock = threading.Lock()

    @wraps(cls)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
