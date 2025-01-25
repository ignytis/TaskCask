from pydantic import BaseModel

from .task_templates.task_template import BaseTaskTemplate


class Task(BaseModel):
    template: BaseTaskTemplate
    args: list[str] = []
