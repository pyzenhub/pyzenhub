"""Test ZenHub issues API."""
import random

import pytest

from zenhub import ZenhubError

from .data import (
    EPIC_WITHOUT_ISSUES,
    PIPELINE_BACKLOG,
    PIPELINE_NEW_ISSUES,
    REPO_ID,
    WORKSPACE_ID,
)


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


@pytest.mark.parametrize(
    'pipeline,position',
    [
        (PIPELINE_BACKLOG, 'top'),
        (PIPELINE_BACKLOG, 'bottom'),
        (PIPELINE_BACKLOG, 0),
        (PIPELINE_BACKLOG, 1),
        (PIPELINE_NEW_ISSUES, 'top'),
        (PIPELINE_NEW_ISSUES, 'bottom'),
        (PIPELINE_NEW_ISSUES, 0),
        (PIPELINE_NEW_ISSUES, 1),
    ],
)
def test_move_issue(zh, pipeline, position):
    data = zh.move_issue(
        WORKSPACE_ID, REPO_ID, EPIC_WITHOUT_ISSUES, pipeline, position
    )
    assert data


@pytest.mark.parametrize(
    'pipeline,position',
    [
        (PIPELINE_BACKLOG, 'top'),
        (PIPELINE_BACKLOG, 'bottom'),
        (PIPELINE_BACKLOG, 0),
        (PIPELINE_BACKLOG, 1),
        (PIPELINE_NEW_ISSUES, 'top'),
        (PIPELINE_NEW_ISSUES, 'bottom'),
        (PIPELINE_NEW_ISSUES, 0),
        (PIPELINE_NEW_ISSUES, 1),
    ],
)
def test_move_issue_in_oldest_workspace(zh, pipeline, position):
    data = zh.move_issue_in_oldest_workspace(
        REPO_ID, EPIC_WITHOUT_ISSUES, pipeline, position
    )
    assert data


def test_set_issue_estimate(zh):
    estimate = random.randint(1, 10)
    data = zh.set_issue_estimate(REPO_ID, 1, estimate=estimate)
    assert data["estimate"] == estimate
