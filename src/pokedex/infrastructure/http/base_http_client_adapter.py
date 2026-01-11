"""Base Http client adapter."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any

import httpx

from pokedex.settings import get_logger
from pokedex.shared.exceptions import UpstreamClientError
from pokedex.shared.exceptions import UpstreamRequestError
from pokedex.shared.exceptions import UpstreamServerError
from pokedex.shared.exceptions import UpstreamTimeoutError

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
            raise UpstreamTimeoutError(
                service=self._prefix(),
                method=spec.method,
                path=spec.path,
                detail=str(e),
            ) from e

        except httpx.RequestError as e:
            raise UpstreamRequestError(
                service=self._prefix(),
                method=spec.method,
                path=spec.path,
                detail=str(e),
            ) from e

        except httpx.HTTPStatusError as e:
            raise self._map_status(e, spec) from e

        else:
            return r

    # ---------- Helpers ----------

    def _prefix(self) -> str:
        return self.client_name

    def _map_status(self, e: httpx.HTTPStatusError, spec: RequestSpec) -> Exception:
        status = e.response.status_code

        if status >= HTTPStatus.INTERNAL_SERVER_ERROR:
            return UpstreamServerError(
                service=self._prefix(),
                method=spec.method,
                path=spec.path,
                status_code=status,
                detail=str(e),
            )

        return UpstreamClientError(
            service=self._prefix(),
            method=spec.method,
            path=spec.path,
            status_code=status,
            detail=str(e),
        )
