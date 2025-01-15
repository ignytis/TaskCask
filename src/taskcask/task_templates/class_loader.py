from typing import List, Type
from abc import ABC


class BaseTaskTemplateClassLoader(ABC):
    """
    Task template class loaders return a list of task template classes to main module.
    """
    def load(self) -> List[Type]:
        raise NotImplementedError()
