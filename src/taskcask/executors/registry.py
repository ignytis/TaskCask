from typing import Type

from .executor import BaseExecutor

_registry: list[Type[BaseExecutor]] = []


def executor(c: Type[BaseExecutor]) -> Type[BaseExecutor]:
    _registry.append(c)
    return c


def get_executor_classes() -> list[Type[BaseExecutor]]:
    return _registry
