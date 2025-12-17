"""REST API server."""

from fastapi import FastAPI

from src.settings import get_logger

# logger
logger = get_logger()

app = FastAPI(
    docs_url="/api/docs",
)
