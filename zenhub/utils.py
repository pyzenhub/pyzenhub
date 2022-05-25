"""ZenHub API utilities."""
import datetime

import requests

from .exceptions import (
    APILimitError,
    InvalidTokenError,
    NotFoundError,
    ZenhubError,
)
from .types import ISO8601DateString


def date_to_string(date: datetime.datetime) -> ISO8601DateString:
    """Convert a datetime object to a ISO8601 date string."""
    return date.isoformat(timespec='milliseconds') + "Z"


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


def parse_response_contents(response: requests.Response) -> dict:
    """Parse response and convert to json if possible."""
    status_code = response.status_code
    try:
        contents = response.json()
    except Exception:
        contents = {}

    if status_code in [200, 204]:
        pass
    elif status_code == 401:
        raise InvalidTokenError("Invalid token!")
    elif status_code == 403:
        raise APILimitError(
            "Reached request limit to the API. See API Limits."
        )
    elif status_code == 404:
        raise NotFoundError("Not found!")
    else:
        message = contents.get("message", "Unknown error!")
        raise ZenhubError(message)

    return contents
