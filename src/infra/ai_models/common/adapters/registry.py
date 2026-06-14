from domain.ai_models.ports import RegistryPort, ModelPort


class RegistryAdapter(RegistryPort):
    _map: dict[str, ModelPort] = {}

    def register(self, model: ModelPort):
        self._map[model.name] = model

    def list(self) -> list[ModelPort]:
        return list(self._map.values())
