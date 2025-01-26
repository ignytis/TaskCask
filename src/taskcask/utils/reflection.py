from typing import Type


# Credits: https://stackoverflow.com/a/17246726
def get_all_subclasses(cls) -> list[Type]:
    """
    Return all subclasses for provided class, considering possible multi-level inheritance
    """
    all_subclasses: list[Type] = []
    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses
