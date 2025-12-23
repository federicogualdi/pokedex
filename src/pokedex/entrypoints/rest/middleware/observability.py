"""Observability middleware."""

import time

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from pokedex.settings import get_logger

# logger
logger = get_logger()


def install_request_timing_middleware(app: FastAPI) -> None:
    """Install request timing middleware."""

    @app.middleware("http")
    async def request_timing_middleware(request: Request, call_next) -> Response:  # noqa: ANN001
        """Middleware.

        Args:
            request (Request): request to be processed
            call_next (Any): callable to forward the request to the right router

        Returns:
            Response: response to be returned to the user
        """
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.debug(f"Request: {request.url.path} process time: {process_time}")
        return response
