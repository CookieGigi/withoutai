from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from dependencies import APIDependencies
from services.llm_service import LLMService


router = APIRouter()


@router.get("/models")
@inject
async def get_models_list(
    llm_service: LLMService = Depends(Provide[APIDependencies.llm_service]),
) -> list[str]:
    return llm_service.get_models_list()
