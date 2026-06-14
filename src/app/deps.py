from infra.deps import get_ai_models_registry
from domain.ai_models.ports import RegistryPort

from .services.ai_models.models import ModelsService

from fastapi import Depends


def get_models_service(registry: RegistryPort = Depends(get_ai_models_registry)):
    return ModelsService(registry)
