from typing import Callable

from fastapi import FastAPI
import structlog
import logging
import sys
from api.middleware.logging_middleware import LoggingMiddleware
from api.router import defaultRouter, healthRouter
from dependency_injector import containers
from api.exceptions import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware
from configuration import Config

_structlog_initialized = False


def _configure_structlog(config: Config):

    global _structlog_initialized
    if _structlog_initialized:
        return  # idempotent for reloader process
    _structlog_initialized = True

    processors: list[Callable] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if config.log_format == "json" or config.env == "prod":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, config.effective_log_level.upper()),
    )

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, config.effective_log_level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # --- suppress uvicorn.access (middleware replaces it) ---
    uvicorn_access = logging.getLogger("uvicorn.access")
    uvicorn_access.handlers.clear()
    uvicorn_access.propagate = False
    uvicorn_access.addHandler(logging.NullHandler())

    # --- prevent uvicorn.error duplication ---
    # uvicorn already has its own handler. Don't let it also propagate to root.
    uvicorn_error = logging.getLogger("uvicorn.error")
    if uvicorn_error.handlers:
        uvicorn_error.propagate = False


def create_app(dependencies: containers.DeclarativeContainer) -> FastAPI:
    config = dependencies.config()
    _configure_structlog(config)

    app = FastAPI(debug=config.env == "dev")
    app.container = dependencies  # type: ignore
    register_exception_handlers(app)

    app.add_middleware(LoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
        allow_headers=["Authorization", "Content-Type"],
    )

    app.include_router(defaultRouter)
    app.include_router(healthRouter)

    return app
