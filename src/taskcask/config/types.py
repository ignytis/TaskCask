from typing import Callable
from pathlib import Path

from pydantic import BaseModel, model_validator

from ..typedefs import StringKeyDict


class Io(BaseModel):
    """
    Input/output configuration
    """
    print_result: bool = True
    """If set, the executor output will be printed. This value can be overridden in task"""


class SysConfig(BaseModel):
    """
    System configuration
    """
    cwd: str | None = None
    """Current working directory"""
    home: str | None = None
    """User's home directory"""

    @model_validator(mode="before")
    def validate_io(cls, values: dict):
        if not values.get("cwd"):
            values["cwd"] = str(Path.cwd())
        if not values.get("home"):
            values["home"] = str(Path.home())
        return values


class TaskTemplateConfig(BaseModel):
    lookup_dirs: list[str] = []


class Config(BaseModel):
    sys: SysConfig | None = None
    """System configuration"""
    environments: dict[str, StringKeyDict] = {}
    """Execution environments setup"""
    io: Io
    """Input / output"""
    params: StringKeyDict = {}
    """User-defined parameters"""
    task_templates: TaskTemplateConfig
    """Task template config"""

    @model_validator(mode="before")
    def validate_io(cls, values: dict):
        if not isinstance(values.get("io"), dict):
            values["io"] = Io()
        if not isinstance(values.get("io"), dict):
            values["sys"] = SysConfig()
        if not isinstance(values.get("task_templates"), dict):
            values["task_templates"] = TaskTemplateConfig()
        return values


ConfigBuilderFn = Callable[[Config], None]
