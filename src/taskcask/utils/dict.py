from ..typedefs import StringKeyDict


def dict_deep_merge(*dicts: StringKeyDict) -> StringKeyDict:
    """
    Deep merge multiple dictionaries recursively.
    Values in later dictionaries overwrite those in earlier ones.
    This function does not update any dictionary by reference.
    """
    def merge_two_dicts(d1: StringKeyDict, d2: StringKeyDict):
        merged = d1.copy()
        for key, value in d2.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = merge_two_dicts(merged[key], value)
            else:
                merged[key] = value
        return merged

    result = {}
    for d in dicts:
        result = merge_two_dicts(result, d)

    return result


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
