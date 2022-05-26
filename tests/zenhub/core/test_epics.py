"""Test ZenHub epics API."""
import pytest

from zenhub import ZenhubError

from .data import EPIC_WITH_ISSUES, EPIC_WITHOUT_ISSUES, REPO_ID


def test_get_epics(zh):
    data = zh.get_epics(REPO_ID)
    assert data


@pytest.mark.parametrize('epic_id', [EPIC_WITH_ISSUES, EPIC_WITHOUT_ISSUES])
def test_get_epic_data(epic_id, zh) -> dict:
    data = zh.get_epic_data(REPO_ID, epic_id)
    assert data


def test_convert_epic_to_issue(zh):
    data = zh.convert_epic_to_issue(REPO_ID, EPIC_WITHOUT_ISSUES)
    assert data


def test_convert_issue_to_epic(zh):
    data = zh.convert_issue_to_epic(REPO_ID, EPIC_WITHOUT_ISSUES)
    assert data


def test_add_or_remove_issues_to_epic(zh):
    data = zh.add_or_remove_issues_to_epic(
        REPO_ID,
        EPIC_WITHOUT_ISSUES,
        remove_issues=[{"repo_id": REPO_ID, "issue_number": 1}],
    )
    assert data


def test_add_or_remove_issues_to_epic_invalid(zh):
    with pytest.raises(ZenhubError):
        zh.add_or_remove_issues_to_epic(
            REPO_ID,
            10000000,
            remove_issues=[{"repo_id": REPO_ID, "issue_number": 1}],
        )
