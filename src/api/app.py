from fastapi import FastAPI
from .router import defaultRouter
from .router import openaiRouter


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(defaultRouter)

    app.include_router(openaiRouter)

    return app
