"""Utils class for infrastructure tests."""

import json

from httpx import MockTransport
from httpx import Request
from httpx import Response


def transport_json(status_code: int, payload: dict) -> MockTransport:
    """Build a MockTransport that returns given status/payload."""

    def handler(request: Request) -> Response:
        content = json.dumps(payload).encode("utf-8")
        return Response(status_code=status_code, content=content, request=request)

    return MockTransport(handler)
