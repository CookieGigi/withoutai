from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from .response import Model, Response
from containers import AppContainer
from app.services.ai_models.models import ModelsService

router = APIRouter(prefix="/models", tags=["OpenAI - models"])


@router.get("/")
@inject
def get_models(
    models: ModelsService = Depends(Provide[AppContainer.models_service]),
) -> Response:
    raw = models.get_model_list()

    res: list[Model] = []

    for model in raw:
        res.append(Model(id=model.name, created=0, owned_by=model.provider))

    return Response(data=res)
