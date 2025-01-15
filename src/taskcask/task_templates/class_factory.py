from typing import Any, Dict
from pkg_resources import iter_entry_points

from pydantic import TypeAdapter

from .class_loader import BaseTaskTemplateClassLoader
from .task_template import BaseTaskTemplate


def get_task_template_from_dict(d: Dict[str, Any]) -> BaseTaskTemplate:
    return _get_type_adapter().validate_python(d)


def _get_type_adapter() -> TypeAdapter:
    kinds = []
    for entry_point in iter_entry_points("taskcask.task_templates.class_loaders"):
        cls = entry_point.load()
        loader: BaseTaskTemplateClassLoader = cls()
        kinds += loader.load()
    return TypeAdapter(*kinds)
