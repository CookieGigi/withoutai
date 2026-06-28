from langchain_core.messages import AIMessage, BaseMessage
from litellm.router import Router

from configuration import Config
from models.check_result import CheckResult
from langchain_litellm import ChatLiteLLMRouter
from interfaces.health_check import HealthCheck
from services.health_check_registry import HealthCheckRegistry


class LLMService(HealthCheck):
    _config: Config
    _provider: ChatLiteLLMRouter

    critical = False

    def __init__(self, config: Config, registry: HealthCheckRegistry) -> None:
        self._config = config

        model_list = [
            {
                "model_name": "compound-mini",
                "litellm_params": {
                    "model": "groq/groq/compound-mini",
                },
            },
            {
                "model_name": "compound",
                "litellm_params": {
                    "model": "groq/groq/compound",
                },
            },
            {
                "model_name": "qwen3.6-27b",
                "litellm_params": {
                    "model": "groq/qwen/qwen3.6-27b",
                },
            },
            {
                "model_name": "llama-prompt-guard-2-86m",
                "litellm_params": {
                    "model": "groq/meta-llama/llama-prompt-guard-2-86m",
                },
            },
            {
                "model_name": "gpt-oss-20b",
                "litellm_params": {
                    "model": "groq/openai/gpt-oss-20b",
                },
            },
            {
                "model_name": "orpheus-arabic-saudi",
                "litellm_params": {
                    "model": "groq/canopylabs/orpheus-arabic-saudi",
                },
            },
            {
                "model_name": "qwen3-32b",
                "litellm_params": {
                    "model": "groq/qwen/qwen3-32b",
                },
            },
            {
                "model_name": "gpt-oss-safeguard-20b",
                "litellm_params": {
                    "model": "groq/openai/gpt-oss-safeguard-20b",
                },
            },
            {
                "model_name": "llama-3.3-70b-versatile",
                "litellm_params": {
                    "model": "groq/llama-3.3-70b-versatile",
                },
            },
            {
                "model_name": "orpheus-v1-english",
                "litellm_params": {
                    "model": "groq/canopylabs/orpheus-v1-english",
                },
            },
            {
                "model_name": "whisper-large-v3",
                "litellm_params": {
                    "model": "groq/whisper-large-v3",
                },
            },
            {
                "model_name": "whisper-large-v3-turbo",
                "litellm_params": {
                    "model": "groq/whisper-large-v3-turbo",
                },
            },
            {
                "model_name": "allam-2-7b",
                "litellm_params": {
                    "model": "groq/allam-2-7b",
                },
            },
            {
                "model_name": "llama-prompt-guard-2-22m",
                "litellm_params": {
                    "model": "groq/meta-llama/llama-prompt-guard-2-22m",
                },
            },
            {
                "model_name": "gpt-oss-120b",
                "litellm_params": {
                    "model": "groq/openai/gpt-oss-120b",
                },
            },
            {
                "model_name": "llama-4-scout-17b-16e-instruct",
                "litellm_params": {
                    "model": "groq/meta-llama/llama-4-scout-17b-16e-instruct",
                },
            },
            {
                "model_name": "llama-3.1-8b-instant",
                "litellm_params": {
                    "model": "groq/llama-3.1-8b-instant",
                },
            },
        ]

        router = Router(model_list=model_list)

        self._provider = ChatLiteLLMRouter(
            router=router, model="groq/openai/gpt-oss-120b"
        )

        registry.register(self)

    def get_model(self) -> ChatLiteLLMRouter:
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
