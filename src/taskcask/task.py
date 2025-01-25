from datetime import datetime
from pydantic import BaseModel

from .task_templates.task_template import BaseTaskTemplate


class Task(BaseModel):
    template: BaseTaskTemplate
    args: list[str] = []

    execution_start: datetime | None = None
    execution_end: datetime | None = None
