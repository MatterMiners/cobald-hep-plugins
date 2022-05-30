import pytest

# the plugin we want to test
from cobald_hep_plugins import example

# test utilities used by several tests
from .utility import MockPool, cobald_yaml_config, get_cobald_config_section


# `parametrize` to run a test for multiple cases
@pytest.mark.parametrize("scale", [1, 15, 0.3])
def test_scale_integer(scale):
    pool = MockPool()
    decorator = example.DemandScale(pool, scale)
    # check conditions via `assert`
    assert decorator.demand == 0
    for demand in (5, 17, 0, 2567891):
        decorator.demand = demand
        assert decorator.demand == demand
        assert pool.demand == demand * scale


# tests can be defined unparametrized as well
def test_scale_invalid():
    pool = MockPool()
    with pytest.raises(ValueError):
        example.DemandScale(pool, 0)


def test_load_yaml_tag():
    """Test that the plugin can be loaded via a YAML !tag"""
    with cobald_yaml_config(
        """
pipeline:
    - !CobaldHepProjectExample
    - !MockPool
        """
    ) as config:
        # the plugin should be the leading element of the `pipeline` section
        plugin_decorator = get_cobald_config_section(config, "pipeline")[0]
        assert isinstance(plugin_decorator, example.DemandScale)
