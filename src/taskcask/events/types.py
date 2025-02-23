from pydantic import BaseModel

from ..environments.environment import BaseEnvironment
from ..task import Task


class BaseEvent(BaseModel):
    pass


class PreExecuteEvent(BaseEvent):
    environment: BaseEnvironment
    task: Task


class PostExecuteEvent(BaseEvent):
    environment: BaseEnvironment
    task: Task
