import pytest

from .utility import MockPool

from cobald_hep_plugins.stopper import Stopper


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
