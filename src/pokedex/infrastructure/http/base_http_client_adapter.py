"""Base Http client adapter."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any

import httpx

from pydantic import ValidationError
from pydantic.types import T

from pokedex.settings import get_logger
from pokedex.shared.exceptions import ExecutionError

# logger
logger = get_logger()


@dataclass(frozen=True)
class RequestSpec:
    """Request spec dataclass."""

    method: str
    url: str
    path: str


class BaseHttpClientAdapter:
    """Base http client adapter."""

    client_name: str = "HTTPClient"

    def __init__(self, http: httpx.AsyncClient, base_url: str):
        """Initialize the base client."""
        self._http = http
        self._base = base_url.rstrip("/")

    async def _request(
        self,
        *,
        method: str,
        path: str,
        json: Mapping[str, Any] | None = None,
        data: Mapping[str, Any] | None = None,
    ) -> httpx.Response:
        url = f"{self._base}/{path.lstrip('/')}"
        spec = RequestSpec(method=method.upper(), url=url, path=path)

        try:
            r = await self._http.request(spec.method, spec.url, json=json, data=data)
            r.raise_for_status()

        except httpx.TimeoutException as e:
            raise self._err("timeout", spec, e) from e

        except httpx.RequestError as e:
            raise self._err("request failed", spec, e) from e

        except httpx.HTTPStatusError as e:
            raise self._map_status(e, spec) from e

        else:
            return r

    def _parse(self, *, response: httpx.Response, model: type[T], spec: RequestSpec) -> T:
        try:
            payload = response.json()
        except ValueError as e:
            raise self._err("invalid JSON response", spec, e) from e

        try:
            return model.model_validate(payload)
        except ValidationError as e:
            raise self._err("invalid response schema", spec, e) from e

    # ---------- Helpers ----------

    def _prefix(self) -> str:
        return self.client_name

    def _err(self, what: str, spec: RequestSpec, cause: Exception | None = None) -> Exception:
        return ExecutionError(f"{self._prefix()}: {what} ({spec.method} {spec.path}). Cause: {cause}")

    def _map_status(self, e: httpx.HTTPStatusError, spec: RequestSpec) -> Exception:
        status = e.response.status_code
        if status >= HTTPStatus.INTERNAL_SERVER_ERROR:
            return ExecutionError(f"{self._prefix()}: server error ({status}) ({spec.method} {spec.path}). Cause: {e}")
        return ExecutionError(f"{self._prefix()}: client error ({status}) ({spec.method} {spec.path}). Cause: {e}")
