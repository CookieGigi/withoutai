from .ai_models.deps import registry
from domain.ai_models.ports import RegistryPort


def get_ai_models_registry() -> RegistryPort:
    return registry
