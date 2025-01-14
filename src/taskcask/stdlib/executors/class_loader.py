from typing import List, Type

from ...executors.class_loader import BaseExecutorClassLoader


class ExecutorClassLoader(BaseExecutorClassLoader):
    def load(self) -> List[Type]:
        from ...stdlib.executors.system_command import SystemCommandExecutor

        return [SystemCommandExecutor]
