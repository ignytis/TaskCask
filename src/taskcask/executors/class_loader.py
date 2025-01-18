from typing import Type
from abc import ABC


class BaseExecutorClassLoader(ABC):
    def load(self) -> list[Type]:
        raise NotImplementedError()
