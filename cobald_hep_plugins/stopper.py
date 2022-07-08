from cobald.interfaces import Pool, PoolDecorator

from cobald.utility import enforce

from tardis.interfaces.executor import Executor
from tardis.utilities.executors.shellexecutor import ShellExecutor

import asyncio

from cobald.daemon import service


@service(flavour=asyncio)
class Stopper(PoolDecorator):
    """
    Decorator that sets demand to 0 if there are no pending jobs

    :param target: the pool
    :param script: path to script that checks for pending jobs
    :param interval: interval in seconds between execution of the script
    :param executor: executor to run the script (default: ShellExecutor)

    If there are pending jobs on the partition, the demand is not modified.
    The demand is set to 0 as long as no pending jobs are detected.

    The default interval is 300 (5 minutes). The script has to be specified.
    """

    @property
    def demand(self) -> float:
        return self.target.demand

    @demand.setter
    def demand(self, value: float):
        self.target.demand = value if self.n_pend_jobs else 0

    async def run(self):
        """Retrieve the number of pending jobs"""
        while True:
            status = await self.executor.run_command(f"{self.script}")
            self.n_pend_jobs = int(status.stdout)
            await asyncio.sleep(self.interval)

    def __init__(
        self,
        target: Pool,
        script: str = "",
        interval: int = 300,
        executor: Executor = ShellExecutor(),
    ):
        super().__init__(target)
        enforce(interval > 0, ValueError("interval must be positive"))
        enforce(script != "", ValueError("script must be specified"))
        self.interval = interval
        self.n_pend_jobs = 0
        self.script = script
        self.executor = executor
