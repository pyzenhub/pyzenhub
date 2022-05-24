"""Test ZenHub issues API."""
import os

import pytest

from zenhub import Zenhub, ZenhubError


TOKEN = os.environ.get("ZENHUB_TEST_TOKEN")
REPO_ID = 262640661


def test_get_issue_data():
    zh = Zenhub(TOKEN)
    data = zh.get_issue_data(REPO_ID, 1)
    assert list(data.keys()) == ["plus_ones", "is_epic", "pipelines", "pipeline"]


def test_get_issue_data_invalid():
    zh = Zenhub(TOKEN)
    with pytest.raises(ZenhubError):
        zh.get_issue_data(REPO_ID, 0)
