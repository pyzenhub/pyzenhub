# -----------------------------------------------------------------------------
# Copyright (c) 2022 Gonzalo Peña-Castellanos (@goanpeca)
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""ZenHub API utilities."""
import datetime

ISO8601DateString = str


def date_to_string(date: datetime.datetime) -> ISO8601DateString:
    """Convert a datetime object to a ISO8601 date string."""
    return date.replace(microsecond=0).isoformat() + "Z"


def string_to_date(date_string: ISO8601DateString) -> datetime.datetime:
    """Convert a a ISO8601 date string to a datetime object."""
    if date_string.endswith("Z"):
        date_string = date_string[:-1]

    return datetime.datetime.fromisoformat(date_string)


def check_dates(
    start_date: datetime.datetime, desired_end_date: datetime.datetime
) -> bool:
    """Check ``desired_end_date`` comes after ``start_date``."""
    if start_date > desired_end_date:
        raise ValueError("Start date must be before end date.")
    return True
