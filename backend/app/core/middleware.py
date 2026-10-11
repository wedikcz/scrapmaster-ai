import time
import logging
from typing import Callable
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """Middleware to log request timing and performance metrics."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {process_time:.3f}s"
        )
        response.headers["X-Process-Time"] = str(process_time)
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Middleware to catch and log unhandled exceptions."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(
                f"Unhandled exception in {request.method} {request.url.path}: {str(e)}",
                exc_info=True,
            )
            raise
        return response
