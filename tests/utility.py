from cobald.interfaces import Pool
from tempfile import NamedTemporaryFile
from contextlib import contextmanager

from cobald.daemon.core.config import load, COBalDLoader, yaml_constructor


class MockPool(Pool):
    __slots__ = ("supply", "demand", "utilisation", "allocation")

    def __init__(self, *, supply=0, demand=0, utilisation=1.0, allocation=1.0):
        self.supply = supply
        self.demand = demand
        self.utilisation = utilisation
        self.allocation = allocation


# allow loading the MockPool in YAML configurations
COBalDLoader.add_constructor(tag="!MockPool", constructor=yaml_constructor(MockPool))


def get_cobald_config_section(config: dict, section: str):
    """Given a loaded :py:mod:`cobald` configuration, return a specific `section`"""
    for plugin, content in config.items():
        if plugin.section == section:
            return content
    raise LookupError(f"No config section named {section}")


@contextmanager
def cobald_yaml_config(yaml_literal: str) -> dict:
    """Create and load a :py:mod:`cobald` YAML configuration from literal content"""
    with NamedTemporaryFile(suffix=".yaml") as config:
        with open(config.name, "w") as write_stream:
            write_stream.write(yaml_literal)
        with load(config.name) as content:
            yield content
