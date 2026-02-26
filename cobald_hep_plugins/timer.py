"""Time-based demand controller and helpers."""

from __future__ import annotations

import asyncio
from datetime import date, datetime, timedelta
from typing import Mapping

from cobald.daemon import service
from cobald.interfaces import Pool, Controller


@service(flavour=asyncio)
class Timer(Controller):
    """Control pool demand based on a daily time schedule."""

    def __init__(
        self,
        target: Pool,
        schedule: Mapping[str, float],
    ) -> None:
        """Create a timer controller.

        Args:
            target: Pool whose demand is controlled by this timer.
            schedule: Mapping of "HH:MM" to demand values.
        """
        super().__init__(target=target)
        schedule = {
            datetime.strptime(time, "%H:%M").time(): demand
            for time, demand in schedule.items()
        }
        schedule = dict(sorted(schedule.items(), key=lambda item: item[0]))
        assert len(schedule) > 0, "Schedule must contain at least one entry."
        assert all(
            demand >= 0 for demand in schedule.values()
        ), "All scheduled demands must be non-negative."
        self.schedule = schedule

    async def run(self) -> None:
        """Update the demand periodically according to the schedule."""
        today = date.today()
        while True:
            for start_time, demand in self.schedule.items():
                start_delta = datetime.combine(today, start_time) - datetime.now()
                await asyncio.sleep(start_delta.total_seconds())
                self.target.demand = demand
            today += timedelta(days=1)
