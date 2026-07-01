from typing import Any

from pydantic import BaseModel, Field


class ModelInfo(BaseModel):
    id: str
    name: str
    can_think: bool = Field(default=False)
    can_vision: bool = Field(default=False)
    max_tokens: int | None = Field(default=None)
    max_input_tokens: int | None = Field(default=None)
    max_output_tokens: int | None = Field(default=None)
    input_cost_per_token: float | None = Field(default=None)
    output_cost_per_token: float | None = Field(default=None)
    provider: str = Field(default="")
    mode: str = Field(default="")
    can_function_call: bool = Field(default=False)
    can_tool_choice: bool = Field(default=False)
    can_prompt_cache: bool = Field(default=False)

    @classmethod
    def from_litellm(cls, model_id: str, litellm_info: Any) -> "ModelInfo":
        return cls(
            id=model_id,
            name=model_id,
            can_think=litellm_info.get("supports_reasoning") or False,
            can_vision=litellm_info.get("supports_vision") or False,
            max_tokens=litellm_info.get("max_tokens"),
            max_input_tokens=litellm_info.get("max_input_tokens"),
            max_output_tokens=litellm_info.get("max_output_tokens"),
            input_cost_per_token=litellm_info.get("input_cost_per_token"),
            output_cost_per_token=litellm_info.get("output_cost_per_token"),
            provider=litellm_info.get("litellm_provider", ""),
            mode=litellm_info.get("mode", ""),
            can_function_call=litellm_info.get("supports_function_calling") or False,
            can_tool_choice=litellm_info.get("supports_tool_choice") or False,
            can_prompt_cache=litellm_info.get("supports_prompt_caching") or False,
        )
