from typing import Any

from pydantic import BaseModel as PydanticBaseModel, ConfigDict as PydanticCofigDict

StringKeyDict = dict[str, Any]
StringKvDict = dict[str, str]

TaskTemplateDefinition = StringKeyDict
ConfigDict = StringKeyDict

EnvVars = StringKvDict


class BaseModel(PydanticBaseModel):
    """
    A base class for models which disallows extra values and uses values of enums.
    It's encouraged to use this class to fail fast in case of misformatted config.
    """
    model_config = PydanticCofigDict(extra="forbid", use_enum_values=True)
