from typing import Type
from abc import ABC


class BaseTaskTemplateClassLoader(ABC):
    """
    Task template class loaders return a list of task template classes to main module.
    """
    def load(self) -> list[Type]:
        raise NotImplementedError()
