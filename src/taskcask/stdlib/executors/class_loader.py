from typing import Type

from ...executors.class_loader import BaseExecutorClassLoader
from ...stdlib.executors.system_command import SystemCommandExecutor


class ExecutorClassLoader(BaseExecutorClassLoader):
    def load(self) -> list[Type]:
        return [SystemCommandExecutor]
