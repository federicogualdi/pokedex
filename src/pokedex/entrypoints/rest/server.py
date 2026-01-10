"""REST API server."""

import json

from contextlib import asynccontextmanager

from fastapi import APIRouter
from fastapi import FastAPI

from pokedex.entrypoints.rest.middleware.exception_handler import install_error_handlers
from pokedex.entrypoints.rest.middleware.observability import install_request_timing_middleware
from pokedex.entrypoints.rest.routes import pokemon
from pokedex.infrastructure.cache.state import build_cache_state
from pokedex.infrastructure.http.http_client import build_async_http_client
from pokedex.settings import get_logger
from pokedex.settings import settings

# logger
logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager."""
    http = build_async_http_client(settings)
    app.state.http = http

    # cache state (process-local)
    app.state.cache = build_cache_state(settings)

    yield

    await http.aclose()


app = FastAPI(
    lifespan=lifespan,
    docs_url="/api/docs",
)

# base router
base_router = APIRouter(prefix="/api")
base_router.include_router(pokemon.router)
# register routers
app.include_router(base_router)

# middlewares
install_error_handlers(app)
install_request_timing_middleware(app)


# enable remote debugging if DEBUG env variable is set
# to enable debug during development on docker
if settings.debug:
    import debugpy

    logger.debug(json.dumps(settings.model_dump(), indent=2))

    debugpy.listen(("0.0.0.0", 5678))  # noqa S104
    logger.info("debugger listening on container port: 5678")

    if settings.wait_for_debugger_connected:
        logger.info("Waiting for debugger to attach...")
        debugpy.wait_for_client()
        logger.info("Debugger attached. Continuing execution.")
