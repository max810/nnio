from abc import ABC, abstractmethod

from .python_code_generator import PythonCodeGenerator
from models import NetworkModel


class FrameworkCodeGenerator(ABC):
    def __init__(self, model: NetworkModel, cg: PythonCodeGenerator):
        self.model = model
        self.cg = cg

    @abstractmethod
    def generate_code(self) -> str:
        pass
