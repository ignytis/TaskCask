from functools import lru_cache
from pkg_resources import iter_entry_points
from typing import Generator, List, Type

from .executor import BaseExecutor
from .class_loader import BaseExecutorClassLoader


@lru_cache
def get_executor_classes() -> Generator[Type[BaseExecutor], None, None]:
    executor_classes: List[Type[BaseExecutor]] = []
    for entry_point in iter_entry_points("taskcask.executors.class_loaders"):
        cls = entry_point.load()
        loader: BaseExecutorClassLoader = cls()
        executor_classes += loader.load()
    return executor_classes
