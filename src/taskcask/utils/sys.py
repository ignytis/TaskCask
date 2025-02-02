from ..typedefs import StringKvDict


def args_to_args_and_kwargs(args: list[str]) -> tuple[list[str], StringKvDict]:
    """
    Converts each input item into:
    1. kwargs - if the item has "=" as a separator i.e. key=value
    2. args - otherwise
    """
    out_args = []
    out_kwargs = {}
    for arg in args:
        i = arg.find("=")
        # Check if arg is not an empty string (or just '=')
        # Also check if '=' is not the first symbol
        if len(arg) > 1 and i > 0:
            k = arg[:i]
            v = arg[i+1:]
            out_kwargs[k] = v
        else:
            out_args.append(arg)
    return (out_args, out_kwargs)
