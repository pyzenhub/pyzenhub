"""Test ZenHub issues API."""
import random

import pytest

from zenhub import ZenhubError

from .data import REPO_ID


def test_get_issue_data(zh):
    data = zh.get_issue_data(REPO_ID, 1)
    assert data
    data = zh.get_issue_data(REPO_ID, 2)
    assert data


def test_get_issue_data_invalid_issue(zh):
    with pytest.raises(ZenhubError) as excinfo:
        zh.get_issue_data(REPO_ID, 10000)

    assert "Not found." in excinfo.value.args[0]


def test_get_issue_events(zh):
    data = zh.get_issue_events(REPO_ID, 1)
    assert len(data) >= 1


def test_set_issue_estimate(zh):
    estimate = random.randint(1, 10)
    data = zh.set_issue_estimate(REPO_ID, 1, estimate=estimate)
    assert data["estimate"] == estimate
