# -*- coding: utf-8 -*-
from __future__ import absolute_import
from typing import Union
import time
import datetime

import pytz
import arrow

from thundersnow.type import immutable


__all__ = (
    'utc_timestamp',
    'utcnow',
    'utcmax',
    'utctime',
    'delta',
)


# The largest datetime object that can be represented
_MAX_DATETIME = datetime.datetime(datetime.MAXYEAR, 12, 31, 23, 59, 59, 999999, tzinfo=pytz.UTC)
_ONE_SECOND = datetime.timedelta(seconds=1)
_ONE_MINUTE = datetime.timedelta(minutes=1)
_ONE_HOUR = datetime.timedelta(hours=1)
_ONE_DAY = datetime.timedelta(days=1)
_ONE_WEEK = 7 * _ONE_DAY

# Common time deltas
#
Delta = immutable(
    'Delta',
    one_second= datetime.timedelta(seconds=1),
    five_seconds= 5 * _ONE_SECOND,
    ten_seconds= 10 * _ONE_SECOND,
    fifteen_seconds= 15 * _ONE_SECOND,
    thirty_seconds= 30 * _ONE_SECOND,
    one_minute= _ONE_MINUTE,
    five_minutes= 5 * _ONE_MINUTE,
    ten_minutes= 10 * _ONE_MINUTE,
    fifteen_minutes= 15 * _ONE_MINUTE,
    thirty_minutes= 30 * _ONE_MINUTE,
    one_hour= _ONE_HOUR,
    one_day= _ONE_DAY,
    two_days= 2 * _ONE_DAY,
    three_days= 3 * _ONE_DAY,
    seven_days= _ONE_WEEK,
    one_week= _ONE_WEEK)


def utcmax():
    # type: () -> datetime.datetime
    """Return the max time in the future that datetime handles, in
    UTC. This is to prevent NULL datetime logic."""
    return _MAX_DATETIME


class DateTime(arrow.Arrow):

    def plus_seconds(self, seconds):
        # type: (int) -> arrow.Arrow
        return self + (seconds * Delta.one_second)

    def plus_minutes(self, minutes):
        # type: (int) -> arrow.Arrow
        return self + (minutes * Delta.one_minute)

    def plus_hours(self, hours):
        # type: (int) -> arrow.Arrow
        return self + (hours * Delta.one_hour)

    def plus_days(self, days):
        # type: (int) -> arrow.Arrow
        return self + (days * Delta.one_day)

    def plus_weeks(self, weeks):
        # type: (int) -> arrow.Arrow
        return self + (weeks * Delta.one_week)

    def is_before_now(self):
        # type: () -> bool
        return self < self.utcnow()

    def is_before(self, other):
        # type: (Union[arrow.Arrow, datetime.datetime]) -> bool
        return self < other

    def is_after_now(self):
        # type: () -> bool
        return self > self.utcnow()

    def is_after(self, other):
        # type: (Union[arrow.Arrow, datetime.datetime]) -> bool
        return self > other


class DateTimeFactory(arrow.ArrowFactory):

    @staticmethod
    def now():
        # type: () -> arrow.Arrow
        return utctime.utcnow()


utc = DateTimeFactory(DateTime)
