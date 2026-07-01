from litellm.types.router import DeploymentTypedDict, LiteLLMParamsTypedDict
from litellm.utils import get_model_info, get_valid_models

from models.models_info import ModelInfo


class ModelsService:
    _model_dict: dict[str, ModelInfo]

    def __init__(self):
        self._model_dict = {}

    def initalize_from_litellm(self):
        for model_id in get_valid_models():
            if not self.is_model_available(model_id):
                model_info = get_model_info(model_id)
                self._model_dict[model_id] = ModelInfo.from_litellm(
                    model_id, model_info
                )

    def is_model_available(self, id) -> bool:
        return self._model_dict.get(id) is not None

    def get_models_list(self) -> list[ModelInfo]:
        return list(self._model_dict.values())

    def get_langchain_litellm_router_model_config(self) -> list[DeploymentTypedDict]:
        res: list[DeploymentTypedDict] = []

        for model in self._model_dict:
            res.append(
                DeploymentTypedDict(
                    model_name=model, litellm_params=LiteLLMParamsTypedDict(model=model)
                )
            )

        return res
