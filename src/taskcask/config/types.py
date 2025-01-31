from typing import Callable

from pydantic import BaseModel, model_validator

from ..typedefs import StringKeyDict


class Io(BaseModel):
    """
    Input/output configuration
    """
    print_output: bool = True
    """If set, the executor output will be printed. This value can be overridden in task"""


class SysConfig(BaseModel):
    """
    System configuration
    """
    cwd: str | None = None
    """Current working directory"""
    home: str | None = None
    """User's home directory"""


class Config(BaseModel):
    sys: SysConfig | None = None
    """System configuration"""
    environments: dict[str, StringKeyDict] = {}
    io: Io
    """Execution environments setup"""
    task_template_loaders: dict[str, dict] = {}
    """Task template loader configuration. Key is loader ID, value is config"""
    misc: StringKeyDict = {}
    """User-defined values"""

    @model_validator(mode="before")
    def validate_io(cls, values: dict):
        if not isinstance(values.get("io"), dict):
            values["io"] = Io()
        return values


ConfigBuilderFn = Callable[[Config], None]
