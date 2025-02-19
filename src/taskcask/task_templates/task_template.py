from pydantic import BaseModel
from typing import Any


class BaseTaskTemplate(BaseModel):
    """
    A base class for task templates
    """
    kind: str
    """A discriminator. Determines which subclass will be loaded"""
    print_result: bool | None = None
    """An override for print_result config property on task level"""
    labels: dict[str, Any] | None = None
    """User-defined labels. These labels can be used for whatever purpose, like grouping taks in plugins"""
