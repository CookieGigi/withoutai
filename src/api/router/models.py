from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from dependencies import APIDependencies
from models.models_info import ModelInfo
from services.llm_service import LLMService
from services.models_service import ModelsService


router = APIRouter()


@router.get("/models")
@inject
async def get_models_list(
    models_service: ModelsService = Depends(Provide[APIDependencies.models_service]),
) -> list[ModelInfo]:
    return models_service.get_models_list()


@router.get("/models/current")
@inject
async def get_current_models(
    llm_service: LLMService = Depends(Provide[APIDependencies.llm_service]),
) -> str:
    return llm_service.get_current_model()
