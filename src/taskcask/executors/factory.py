from functools import lru_cache
from importlib.metadata import entry_points
from typing import Generator, Type

from .executor import BaseExecutor
from .class_loader import BaseExecutorClassLoader


@lru_cache
def get_executor_classes() -> Generator[Type[BaseExecutor], None, None]:
    executor_classes: list[Type[BaseExecutor]] = []
    for entry_point in entry_points(group="taskcask.executors.class_loaders"):
        cls = entry_point.load()
        loader: BaseExecutorClassLoader = cls()
        executor_classes += loader.load()
    return executor_classes
