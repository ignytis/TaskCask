from pydantic import BaseModel

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
    task_template_loaders: dict[str, dict] = {}
    """Task template loader configuration. Key is loader ID, value is config"""
    misc: StringKeyDict = {}
    """User-defined values"""
