from .model import ModelPort
from abc import ABC, abstractmethod


class RegistryPort(ABC):
    @abstractmethod
    def register(self, model: ModelPort):
        pass

    @abstractmethod
    def list(self) -> list[ModelPort]:
        pass
