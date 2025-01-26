from .types import ConfigBuilderFn


_registry: list[ConfigBuilderFn] = []


def config_builder(fn: ConfigBuilderFn) -> ConfigBuilderFn:
    _registry.append(fn)
    return fn


def get_config_builders() -> ConfigBuilderFn:
    return _registry
