from typing import Literal
from abc import ABC


class ModelPort(ABC):
    name: str
    type: Literal["llm"]
    provider: str

    def __init__(self, name: str):
        self.name = name
