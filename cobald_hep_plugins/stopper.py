from cobald.interfaces import Pool, PoolDecorator

from ..utility import enforce

import asyncio

from cobald.daemon import service


@service(flavour=asyncio)
class Stopper(PoolDecorator):
    """
    Decorator that sets demand to 0 if the partition has no pending jobs

    :param target: the pool
    :param script: script that checks for pending jobs on the partition
    :param interval: interval in seconds between execution of the script

    If there are pending jobs on the partition, the demand is not modified.
    The demand is set to 0 as long as no pending jobs are detected.

    The default interval is 300 (5 minutes). The script has to be specified.
    """

    @property
    def demand(self) -> float:
        return self._demand

    @demand.setter
    def demand(self, value: float):
        self._demand = self._condition_slurm(value)
        self.target.demand = self._demand

    def _condition_slurm(self, value):
        """Return 0 if there are no pending jobs, otherwise pass `value`"""
        if self.n_pend_jobs == 0:
            return 0
        else:
            return value

    async def run(self):
        """Retrieve the number of pending jobs"""
        while True:
            proc = await asyncio.create_subprocess_shell(
                f". {self.script}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            self.n_pend_jobs = int(stdout.decode("ascii").strip())
            await asyncio.sleep(self.interval)

    def __init__(
        self,
        target: Pool,
        script: str = "",
        interval: int = 300,
    ):
        super().__init__(target)
        enforce(interval > 0, ValueError("interval must be positive"))
        enforce(script != "", ValueError("script must be specified"))
        self._demand = target.demand
        self.interval = interval
        self.n_pend_jobs = 0
        self.script = script
