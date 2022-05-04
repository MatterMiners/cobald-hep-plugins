import pytest

# the plugin we want to test
from cobald_hep_plugins import example

# test utilities used by several tests
from .utility import MockPool


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
