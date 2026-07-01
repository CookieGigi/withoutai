from langchain_core.messages import AIMessage, BaseMessage
from litellm.router import Router

from configuration import Config
from models.check_result import CheckResult
from langchain_litellm import ChatLiteLLMRouter
from interfaces.health_check import HealthCheck
from services.health_check_registry import HealthCheckRegistry

from services.logger_service import LoggerService
from services.models_service import ModelsService


class LLMService(HealthCheck):
    _config: Config
    _provider: ChatLiteLLMRouter
    _logger: LoggerService
    _models_service: ModelsService
    _current_model: str = "groq/openai/gpt-oss-120b"

    critical = False

    def __init__(
        self,
        config: Config,
        registry: HealthCheckRegistry,
        logger: LoggerService,
        models_service: ModelsService,
        default_model: str | None,
    ) -> None:
        self._config = config
        self._logger = logger

        self._models_service = models_service
        if default_model is not None:
            self._current_model = default_model

        router = Router(
            model_list=models_service.get_langchain_litellm_router_model_config()
        )

        self._provider = ChatLiteLLMRouter(router=router, model=self._current_model)

        registry.register(self)

    def get_model_provider(self) -> ChatLiteLLMRouter:
        return self._provider

    def set_model(self, model_name: str | None) -> None:
        if model_name is not None:
            self._provider.set_default_model(model_name)
            self._current_model = model_name

    def get_current_model(self) -> str:
        return self._current_model

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
