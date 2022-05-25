"""Test ZenHub issues API."""
import datetime

import pytest

from zenhub import utils


def test_date_to_string():
    date_string = utils.date_to_string(datetime.datetime(2020, 1, 1))
    assert date_string == "2020-01-01T00:00:00Z"


def test_string_to_date():
    date = utils.string_to_date("2020-01-01T00:00:00Z")
    assert date == datetime.datetime(2020, 1, 1)


def test_check_dates():
    start_date = datetime.datetime(2020, 1, 1)
    desired_end_date = datetime.datetime(2020, 1, 1) + datetime.timedelta(90)
    assert utils.check_dates(start_date, desired_end_date)


def test_check_dates_ivalid():
    start_date = datetime.datetime(2020, 1, 1) + datetime.timedelta(90)
    desired_end_date = datetime.datetime(2020, 1, 1)
    with pytest.raises(ValueError):
        utils.check_dates(start_date, desired_end_date)
