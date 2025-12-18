"""Exception handler middleware."""

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from pokedex.entrypoints.rest.schemas.shared import ErrorResponseSchema
from pokedex.settings import get_logger
from pokedex.shared.exceptions import InvalidArgumentError
from pokedex.shared.exceptions import NotFoundError

# logger
logger = get_logger()


def install_error_handlers(app: FastAPI) -> None:
    """Install error handlers."""

    @app.exception_handler(NotFoundError)
    async def not_found_handler(_: Request, exc: NotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponseSchema(details=str(exc)).model_dump(),
        )

    @app.exception_handler(InvalidArgumentError)
    async def bad_request_handler(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponseSchema(details=str(exc)).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponseSchema(details=str(exc)).model_dump(),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponseSchema(details=str(exc)).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unexpected_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponseSchema(details=str(exc)).model_dump(),
        )
