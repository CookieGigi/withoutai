from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage


class AgentState(BaseModel):
    messages: list[BaseMessage]
    model: str | None = Field(default=None)
