from pydantic import BaseModel

from ..task import Task


class BaseEvent(BaseModel):
    pass


class PreExecuteEvent(BaseEvent):
    task: Task


class PostExecuteEvent(BaseEvent):
    task: Task
