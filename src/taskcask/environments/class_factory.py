from importlib.metadata import entry_points
from typing import Annotated, Type, Union

from pydantic import Field


def _get_kinds() -> list[Type]:
    kinds = []
    for entry_point in entry_points(group="taskcask.environments.class_loaders"):
        load_fn = entry_point.load()
        kinds += load_fn()
    if len(kinds) == 0:
        raise Exception("No environments are registered in the application.")
    return kinds


EnvironmentType = Annotated[Union[*_get_kinds()], Field(discriminator="kind")]
