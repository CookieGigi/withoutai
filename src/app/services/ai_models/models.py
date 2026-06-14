from domain.ai_models.ports import RegistryPort, ModelPort


class ModelsService:
    _registry: RegistryPort

    def __init__(self, registry: RegistryPort):
        self._registry = registry

    def get_model_list(self) -> list[ModelPort]:
        return self._registry.list()
