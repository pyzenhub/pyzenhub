"""Test ZenHub dependencies API."""
from .data import REPO_ID


def test_get_dependencies(zh):
    data = zh.get_dependencies(REPO_ID)
    assert data
    assert "dependencies" in data


def test_create_dependency(zh):
    data = zh.create_dependency(REPO_ID, 1, REPO_ID, 2)
    assert data


def test_remove_dependency(zh):
    data = zh.remove_dependency(REPO_ID, 1, REPO_ID, 2)
    assert data
