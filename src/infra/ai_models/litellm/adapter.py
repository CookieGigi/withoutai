from domain.ai_models.ports import ModelPort


class ModelAdapter(ModelPort):
    provider: str = "litellm"
