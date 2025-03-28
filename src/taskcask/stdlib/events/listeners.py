from datetime import datetime
import logging

from taskcask_common.events.listeners import BaseTaskPreExecuteListener, BaseTaskPostExecuteListener
from taskcask_common.events.types import PreExecuteEvent, PostExecuteEvent


class ExecutionTimePreListener(BaseTaskPreExecuteListener):
    def handle(self, e: PreExecuteEvent) -> None:
        e.task.execution_start = datetime.now()

    def get_priority(cls) -> int:
        return 100


class ExecutionTimePostListener(BaseTaskPostExecuteListener):
    log = logging.getLogger(__name__)

    def handle(self, e: PostExecuteEvent) -> None:
        e.task.execution_end = datetime.now()
        duration = e.task.execution_end - e.task.execution_start

        self.log.info(f"Execution start time: {e.task.execution_start}")
        self.log.info(f"Execution end time: {e.task.execution_end}")
        self.log.info(f"Execution duration: {duration}")

    def get_priority(cls) -> int:
        return 100
