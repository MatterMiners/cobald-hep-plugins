import pytest

from cobald_hep_plugins.stopper import Stopper

from .utility import MockPool, cobald_yaml_config, get_cobald_config_section


class TestStopper(object):
    def test_init_enforcement(self):
        pool = MockPool()
        with pytest.raises(ValueError):
            Stopper(pool, script="test.sh", interval=-10)
        with pytest.raises(ValueError):
            Stopper(pool, script="")
        with pytest.raises(ValueError):
            Stopper(pool)

    def test_running(self):
        pool = MockPool()
        stopper = Stopper(pool, script="test.sh")

        for pend_jobs in (2, 7, 150, 5000):
            stopper.n_pend_jobs = pend_jobs
            for value in (0, 1, 5, 10, 1000):
                stopper.demand = value
                assert stopper.demand == value

    def test_idle(self):
        pool = MockPool()
        stopper = Stopper(pool, script="test.sh")

        stopper.n_pend_jobs = 0

        for value in (0, 1, 5, 10, 1000):
            stopper.demand = value
            assert stopper.demand == 0


def test_load_yaml_tag():
    """Test that the plugin can be loaded via a YAML !tag"""
    with cobald_yaml_config(
        """
pipeline:
    - !Stopper
      script: "test.sh"
    - !MockPool
        """
    ) as config:
        # the plugin should be the leading element of the `pipeline` section
        plugin_decorator = get_cobald_config_section(config, "pipeline")[0]
        assert isinstance(plugin_decorator, Stopper)
