from typing import Annotated, Union

from pydantic import BaseModel, Field, TypeAdapter

from ..utils.reflection import get_all_subclasses


class BaseEnvironment(BaseModel):
    kind: str

    @staticmethod
    def create_from_dict(d: dict) -> "BaseEnvironment":
        EnvironmentType = Annotated[Union[*get_all_subclasses(BaseEnvironment)], Field(discriminator="kind")]
        adapter = TypeAdapter(EnvironmentType)
        return adapter.validate_python(d)
