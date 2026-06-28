import time
import uuid
from typing import Awaitable, Callable

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        start_time = time.perf_counter()

        response: Response = Response()

        try:
            response = await call_next(request)
        except Exception:
            structlog.get_logger().exception("request_failed")
            raise
        finally:
            duration_ms = (time.perf_counter() - start_time) * 1000
            status_code = getattr(response, "status_code", 500)

            structlog.get_logger().info(
                "request_completed",
                status_code=status_code,
                duration_ms=round(duration_ms, 2),
            )

            structlog.contextvars.clear_contextvars()

        response.headers["X-Request-ID"] = request_id
        return response
