from typing import Any

from langchain_core.messages import AIMessage, BaseMessage
from litellm.router import Router
from litellm.utils import get_valid_models

from configuration import Config
from models.check_result import CheckResult
from langchain_litellm import ChatLiteLLMRouter
from interfaces.health_check import HealthCheck
from services.health_check_registry import HealthCheckRegistry

from services.logger_service import LoggerService


class LLMService(HealthCheck):
    _config: Config
    _provider: ChatLiteLLMRouter
    _model_dict: list[dict[str, Any]]
    _model_list: list[str]
    _logger: LoggerService

    critical = False

    def __init__(
        self, config: Config, registry: HealthCheckRegistry, logger: LoggerService
    ) -> None:
        self._config = config
        self._logger = logger

        self._init_model_list()

        router = Router(model_list=self._model_dict)

        self._provider = ChatLiteLLMRouter(router=router, model="gpt-oss-120b")

        registry.register(self)

    def _init_model_list(self):
        self._model_dict = []
        self._model_list = []

        for model in get_valid_models():
            self._model_list.append(model.split("/")[-1])
            self._model_dict.append(
                {"model_name": model.split("/")[-1], "litellm_params": {"model": model}}
            )

    def get_model_provider(self) -> ChatLiteLLMRouter:
        return self._provider

    def set_model(self, model_name: str) -> None:
        self._provider.set_default_model(model_name)

    async def chat(self, messages: list[BaseMessage]) -> AIMessage:
        return await self._provider.ainvoke(messages)

    async def check(self) -> CheckResult:
        try:
            await self._provider.ainvoke(
                [{"role": "user", "content": "ping"}],
                max_tokens=1,
            )
            return CheckResult(name="llm", status="ok", error=None)
        except Exception as e:
            return CheckResult(name="llm", status="error", error=str(e))

    def get_models_list(self) -> list[str]:
        return self._model_list
