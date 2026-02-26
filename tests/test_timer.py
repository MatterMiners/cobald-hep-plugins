import asyncio
import datetime
import pytest

import cobald_hep_plugins.timer as timer_patch

from asyncio import sleep as unpatched_sleep
from cobald_hep_plugins.timer import Timer
from .utility import MockPool

SCHEDULE = {
    "18:03": 30.0,
    "06:59": 10.0,
    "00:30": 0.0,
    "12:38": 20.0,
}


def test_schedule_parsing_and_ordering():
    timer = Timer(target=MockPool(), schedule=SCHEDULE)

    expected = {
        datetime.time(0, 30): 0.0,
        datetime.time(6, 59): 10.0,
        datetime.time(12, 38): 20.0,
        datetime.time(18, 3): 30.0,
    }
    assert timer.schedule == expected
    assert list(timer.schedule.keys()) == list(expected.keys())


def mock_time(time):
    """mocking datatime.datetime and datetime.date
    for test_timer_overrides_demand()"""

    fixed_datetime = datetime.datetime.combine(datetime.datetime(2025, 1, 1), time)

    class DateTimeMock(datetime.datetime):
        @classmethod
        def now(cls):
            return fixed_datetime

    class DateMock(datetime.date):
        @classmethod
        def today(cls):
            return fixed_datetime.date()

    return DateTimeMock, DateMock


async def fast_sleep(delay_seconds):
    """mock asyncio.sleep() for test_timer_overrides_demand()"""
    if delay_seconds > 0:
        raise asyncio.CancelledError()
    return await unpatched_sleep(0)


@pytest.mark.asyncio
async def test_timer_overrides_demand(monkeypatch):

    test_times = [
        datetime.time(0, 0),
        datetime.time(0, 31),
        datetime.time(7, 0),
        datetime.time(12, 39),
        datetime.time(18, 4),
    ]
    expected_demands = [99, 0.0, 10.0, 20.0, 30.0]

    monkeypatch.setattr(timer_patch.asyncio, "sleep", fast_sleep)

    for test_time, expected_demand in zip(test_times, expected_demands):  # noqa: B905

        pool = MockPool(demand=99)

        dt_mock, date_mock = mock_time(test_time)
        monkeypatch.setattr(timer_patch, "datetime", dt_mock)
        monkeypatch.setattr(timer_patch, "date", date_mock)

        timer = timer_patch.Timer(target=pool, schedule=SCHEDULE)
        with pytest.raises(asyncio.CancelledError):
            await timer.run()
        assert timer.target.demand == expected_demand


def test_schedule_rejects_empty():
    with pytest.raises(AssertionError):
        Timer(target=MockPool(), schedule={})


def test_schedule_rejects_negative_demand():
    schedule = {
        "10:00": -5.0,
    }
    with pytest.raises(AssertionError):
        Timer(target=MockPool(), schedule=schedule)


def test_schedule_rejects_invalid_time_strings():
    for invalid in ("invalid", "25:00", "12:60"):
        with pytest.raises(ValueError):
            Timer(target=MockPool(), schedule={invalid: 1.0})
