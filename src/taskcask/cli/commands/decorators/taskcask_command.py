from ....config import types


def taskcask_command(orig_fn):
    """
    Adds config as a command argument.
    NB: This decorator must FOLLOW Click decorators
    """

    def wrap_fn(**kwargs):
        cfg = types.Config(
            runtime_params=types.RuntimeParams.from_kwargs(kwargs),
        )

        # TODO: go over Config Builders using endpoints
        # for builder in builders:
        #   builder.build(result)

        return orig_fn(config=cfg, **kwargs)

    return wrap_fn
