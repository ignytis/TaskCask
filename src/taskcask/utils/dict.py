from ..typedefs import StringKeyDict


# Credits: https://stackoverflow.com/a/7205107
def dict_merge(a: dict, b: dict, path=[]):
    """
    Merges dict b into dict a
    """
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                dict_merge(a[key], b[key], path + [str(key)])
            else:
                a[key] = b[key]

        else:
            a[key] = b[key]
    return a


def dict_unflatten(data: StringKeyDict):
    """
    Unflattens a dictionary:
    {"a.b.c": "val"} -> {"a": {"b": {"c": "val"}}}
    """
    unflattened_dict = {}
    for key, value in data.items():
        sub_keys = key.split(".")
        current_dict = unflattened_dict
        for sub_key in sub_keys[:-1]:
            if sub_key not in current_dict:
                current_dict[sub_key] = {}
            current_dict = current_dict[sub_key]
        current_dict[sub_keys[-1]] = value
    return unflattened_dict
