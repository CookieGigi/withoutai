from domain.ai_models.ports.registry import RegistryPort
from litellm.utils import get_valid_models
from .adapter import ModelAdapter


def register(registry: RegistryPort):
    models = get_valid_models()

    for model in models:
        registry.register(ModelAdapter(name=model))
