"""Test ZenHub issues API."""
import os

import pytest

from zenhub import Zenhub, ZenhubError


# Constants
# ----------------------------------------------------------------------------
TOKEN = os.environ.get("ZENHUB_TEST_TOKEN", "")
REPO_ID = 262640661
RELEASE_REPORT = 'Z2lkOi8vcmFwdG9yL1JlbGVhc2UvNzcyNTE'


# Fixtures
# ----------------------------------------------------------------------------
@pytest.fixture
def zh():
    return Zenhub(TOKEN)


# Issues
# ----------------------------------------------------------------------------
def test_get_issue_data(zh):
    data = zh.get_issue_data(REPO_ID, 1)
    assert list(data.keys()) == ["plus_ones", "is_epic", "pipelines", "pipeline"]


def test_get_issue_data_invalid_issue(zh):
    with pytest.raises(ZenhubError) as excinfo:
        zh.get_issue_data(REPO_ID, 10000)

    assert 'Not found.' in excinfo.value.args[0]

# Releases
# ----------------------------------------------------------------------------
def test_get_release_report_issues(zh):
    data = zh.get_release_report_issues(RELEASE_REPORT)
    assert isinstance(data, list)


def test_get_release_report_issues_invalid(zh):
    with pytest.raises(ZenhubError) as excinfo:
        zh.get_release_report_issues('invalid-id')

    assert excinfo.value.args[0] == 'invalid base64'


def test_add_or_remove_issues_from_release_report_empty(zh):
    data = zh.add_or_remove_issues_from_release_report(RELEASE_REPORT)
    assert data == {"added": [], "removed": []}
    

def test_add_or_remove_issues_from_release_report_add(zh):
    data = zh.add_or_remove_issues_from_release_report(RELEASE_REPORT, add_issues=[{'repo_id': REPO_ID, 'issue_number': 1}])
    assert data == {'added': [{'repo_id': REPO_ID, 'issue_number': 1}], 'removed': []}
    

def test_add_or_remove_issues_from_release_report_remove(zh):
    data = zh.add_or_remove_issues_from_release_report(RELEASE_REPORT, remove_issues=[{'repo_id': REPO_ID, 'issue_number': 1}])
    assert data == {'added': [], 'removed': [{'repo_id': REPO_ID, 'issue_number': 1}]}


def test_add_or_remove_issues_from_release_report_both(zh):
    data = zh.add_or_remove_issues_from_release_report(RELEASE_REPORT, add_issues=[{'repo_id': REPO_ID, 'issue_number': 2}], remove_issues=[{'repo_id': REPO_ID, 'issue_number': 1}])
    assert data == {'added': [{'repo_id': REPO_ID, 'issue_number': 2}], 'removed': [{'repo_id': REPO_ID, 'issue_number': 1}]}
