from pydantic import BaseModel


class BaseTaskTemplate(BaseModel):
    """
    A base class for task templates
    """
    kind: str
    """A discriminator. Determines which subclass will be loaded"""
    print_result: bool | None = None
    """An override for print_result config property on task level"""
