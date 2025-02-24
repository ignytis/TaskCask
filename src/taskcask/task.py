from datetime import datetime
from typing import Any
from typing_extensions import Self
import uuid

from pydantic import BaseModel, model_validator

from .task_templates.task_template import BaseTaskTemplate


class Task(BaseModel):
    id: str | None = None
    template: BaseTaskTemplate
    args: list[str] = []

    execution_start: datetime | None = None
    execution_end: datetime | None = None

    result: Any = None

    @model_validator(mode="after")
    def _set_id(self) -> Self:
        if self.id is not None:  # already set
            return self
        self.id = uuid.uuid4()
        return self
