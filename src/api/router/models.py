from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from dependencies import APIDependencies
from models.models_info import ModelInfo
from services.models_service import ModelsService


router = APIRouter()


@router.get("/models")
@inject
async def get_models_list(
    models_service: ModelsService = Depends(Provide[APIDependencies.models_service]),
) -> list[ModelInfo]:
    return models_service.get_models_list()
