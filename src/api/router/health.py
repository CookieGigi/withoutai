from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

from dependency_injector.wiring import inject, Provide
from dependencies import APIDependencies
from configuration import Config
from models.check import Check


router = APIRouter()


class HealthResponse(BaseModel):
    status: Literal["ok"] = Field(default="ok")
    version: str = Field(default="0.0.0")


@router.get("/health")
@inject
async def get_health(
    config: Config = Provide[APIDependencies.config],
) -> HealthResponse:
    return HealthResponse(version=config.version)


class ReadyResponse(BaseModel):
    status: Literal["ok", "degraded", "error"] = Field(default="ok")
    version: str = Field(default="0.0.0")
    checks: list[Check] = Field(default=[])


@router.get("/ready")
@inject
async def get_ready(
    config: Config = Provide[APIDependencies.config],
) -> ReadyResponse:
    return ReadyResponse(version=config.version)
