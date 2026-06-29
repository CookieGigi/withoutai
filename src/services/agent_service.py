from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver


from models.agent_state import AgentState

from .llm_service import LLMService
from langgraph.graph import END, START, StateGraph


class AgentService:
    _llm_service: LLMService
    _graph: CompiledStateGraph

    def __init__(self, llm_service: LLMService):
        self._llm_service = llm_service

        workflow = StateGraph(AgentState)
        workflow.add_node("call_model", self._call_model)
        workflow.add_edge(START, "call_model")
        workflow.add_edge("call_model", END)

        self._graph = workflow.compile(checkpointer=MemorySaver())

    async def _call_model(self, state: AgentState) -> AgentState:
        response = await self._llm_service.chat(state.messages)
        return AgentState(messages=state.messages + [response])

    def get_agent(self) -> CompiledStateGraph:
        return self._graph
