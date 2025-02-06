from typing import Any, Type


# Credits: https://stackoverflow.com/a/17246726
def get_all_subclasses[T](cls: Type[T]) -> list[Type[T]]:
    """
    Return all subclasses for provided class, considering possible multi-level inheritance
    """
    all_subclasses: list[Type[T]] = []
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


def is_scalar(value: Any) -> bool:
    return isinstance(value, (int, float, str, bool)) or value is None
