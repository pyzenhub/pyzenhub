import datetime
import random

from zenhub.utils import date_to_string

from .data import MILESTONE_ID, REPO_ID

DATE = datetime.datetime(2020, 4, 30) - datetime.timedelta(
    random.randint(20, 90)
)


def test_set_milestone_start_date(zh):
    data = zh.set_milestone_start_date(REPO_ID, MILESTONE_ID, start_date=DATE)
    assert data["start_date"] == date_to_string(DATE)


def test_get_repository_board(zh):
    data = zh.get_milestone_start_date(REPO_ID, MILESTONE_ID)
    assert data["start_date"] == date_to_string(DATE)
