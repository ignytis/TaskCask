from typing import Callable

from pydantic import BaseModel

from ..environments.class_factory import EnvironmentType
from ..typedefs import StringKeyDict


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
    environments: dict[str, EnvironmentType] = {}  # type: ignore
    """Execution environments setup"""
    task_template_loaders: dict[str, dict] = {}
    """Task template loader configuration. Key is loader ID, value is config"""
    misc: StringKeyDict = {}
    """User-defined values"""


ConfigBuilderFn = Callable[[Config], None]
