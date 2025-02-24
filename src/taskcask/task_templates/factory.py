from typing import Any, Union, Annotated

from pydantic import TypeAdapter, Discriminator

from .task_template import BaseTaskTemplate
from ..utils.reflection import get_all_subclasses


def get_task_template_from_dict(d: dict[str, Any], id: str) -> BaseTaskTemplate:
    return _get_type_adapter().validate_python({"id": id, **d})


def _get_type_adapter() -> TypeAdapter:
    kinds = []
    for cls in get_all_subclasses(BaseTaskTemplate):
        kinds += [cls]
    return TypeAdapter(Annotated[Union[*kinds], Discriminator("kind")])
