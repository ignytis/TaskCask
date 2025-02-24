from pydantic import BaseModel

from ..environments.environment import BaseEnvironment
from ..task import Task


class BaseEvent(BaseModel):
    """A base class for events"""
    pass


class GetTargetEnvironmentEvent(BaseEvent):
    """
    This event is invoked before calculation of target environment.
    """
    task: Task
    target_env: str | None


class PreExecuteEvent(BaseEvent):
    """
    This event is invoked before execution of task
    """
    environment: BaseEnvironment
    task: Task


class PostExecuteEvent(BaseEvent):
    """
    This event is invoked after execution of task
    """
    environment: BaseEnvironment
    task: Task
