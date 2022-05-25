"""Test ZenHub issues API."""
import datetime
import json

import pytest

from zenhub import exceptions, utils


# Mocks
# ----------------------------------------------------------------------------
class MockResponse:
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return json.loads(self.json_data)


# Check date and date_string conversions
# ----------------------------------------------------------------------------
def test_date_to_string():
    date_string = utils.date_to_string(datetime.datetime(2020, 1, 1))
    assert date_string == "2020-01-01T00:00:00Z"


def test_string_to_date():
    date = utils.string_to_date("2020-01-01T00:00:00Z")
    assert date == datetime.datetime(2020, 1, 1)


# Check dates
# ----------------------------------------------------------------------------
def test_check_dates():
    start_date = datetime.datetime(2020, 1, 1)
    desired_end_date = datetime.datetime(2020, 1, 1) + datetime.timedelta(90)
    assert utils.check_dates(start_date, desired_end_date)


def test_check_dates_ivalid():
    start_date = datetime.datetime(2020, 1, 1) + datetime.timedelta(90)
    desired_end_date = datetime.datetime(2020, 1, 1)
    with pytest.raises(ValueError):
        utils.check_dates(start_date, desired_end_date)


# Check parse_response_contents_valid
# ----------------------------------------------------------------------------
@pytest.mark.parametrize('status_code', [200, 204])
def test_parse_response_contents_valid(status_code):
    data = '{"message": "Success!"}'
    response = MockResponse(status_code, data)
    result = utils.parse_response_contents(response)
    assert result == json.loads(data)


@pytest.mark.parametrize(
    'status_code,error_class',
    [
        (401, exceptions.InvalidTokenError),
        (403, exceptions.APILimitError),
        (404, exceptions.NotFoundError),
        (409, exceptions.ZenhubError),
    ],
)
def test_parse_response_contents_invalid(status_code, error_class):
    response = MockResponse(status_code, '{}')
    with pytest.raises(error_class):
        utils.parse_response_contents(response)


def test_parse_response_contents_invalid_parse_error():
    response = MockResponse(200, 'bb')
    result = utils.parse_response_contents(response)
    assert result == {}
