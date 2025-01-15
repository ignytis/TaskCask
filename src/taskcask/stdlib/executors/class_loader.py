from typing import List, Type

from ...executors.class_loader import BaseExecutorClassLoader
from ...stdlib.executors.system_command import SystemCommandExecutor


class ExecutorClassLoader(BaseExecutorClassLoader):
    def load(self) -> List[Type]:
        return [SystemCommandExecutor]
