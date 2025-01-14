from typing import List, Type
from abc import ABC


class BaseExecutorClassLoader(ABC):
    def load(self) -> List[Type]:
        raise NotImplementedError()
