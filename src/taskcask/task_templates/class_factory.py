from importlib.metadata import entry_points
from typing import Any

from pydantic import TypeAdapter

from .class_loader import BaseTaskTemplateClassLoader
from .task_template import BaseTaskTemplate


def get_task_template_from_dict(d: dict[str, Any]) -> BaseTaskTemplate:
    return _get_type_adapter().validate_python(d)


def _get_type_adapter() -> TypeAdapter:
    kinds = []
    for entry_point in entry_points(group="taskcask.task_templates.class_loaders"):
        cls = entry_point.load()
        loader: BaseTaskTemplateClassLoader = cls()
        kinds += loader.load()
    return TypeAdapter(*kinds)
