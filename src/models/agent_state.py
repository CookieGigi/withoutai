from pydantic import BaseModel
from langchain_core.messages import BaseMessage


class AgentState(BaseModel):
    messages: list[BaseMessage]
