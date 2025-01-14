from typing import List, Type
from abc import ABC


class BaseTaskTemplateClassLoader(ABC):
    def load(self) -> List[Type]:
        raise NotImplementedError()
