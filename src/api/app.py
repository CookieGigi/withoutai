from fastapi import FastAPI
from .router import defaultRouter
from dependency_injector import containers
from .exceptions import register_exception_handlers


def create_app(dependencies: containers.DeclarativeContainer) -> FastAPI:
    config = dependencies.config()
    app = FastAPI(debug=config.env == "dev")
    app.container = dependencies  # type: ignore
    register_exception_handlers(app)

    app.include_router(defaultRouter)

    return app
