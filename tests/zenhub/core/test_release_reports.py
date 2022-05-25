import datetime
import random

import pytest

from zenhub import ZenhubError

from .data import RELEASE_REPORT, REPO_ID, RUN_CREATE_TESTS

RELEASE_REPORT_KEYS = [
    "release_id",
    "title",
    "description",
    "start_date",
    "desired_end_date",
    "created_at",
    "closed_at",
    "state",
    "repositories",
]


@pytest.mark.skipif(
    RUN_CREATE_TESTS, reason="Create tests are disabled by default."
)
def test_create_release_report(zh):
    title = "Test Release Report"
    description = "Some test description"
    data = zh.create_release_report(
        repo_id=REPO_ID,
        title=title,
        start_date=datetime.datetime.now(),
        desired_end_date=datetime.datetime.now() + datetime.timedelta(days=60),
        description=description,
        repositories=[],
    )
    assert list(data.keys()) == RELEASE_REPORT_KEYS
    assert data["title"] == title
    assert data["description"] == description


def test_create_release_report_invalid_dates(zh):
    title = "Test Release Report"
    description = "Some test description"
    with pytest.raises(ValueError):
        zh.create_release_report(
            repo_id=REPO_ID,
            title=title,
            start_date=datetime.datetime.now() + datetime.timedelta(days=60),
            desired_end_date=datetime.datetime.now(),
            description=description,
            repositories=[],
        )


def test_get_release_report(zh):
    data = zh.get_release_report(RELEASE_REPORT)
    assert list(data.keys()) == RELEASE_REPORT_KEYS
    print(data)
    assert data["title"] == "Test Release"


def test_get_release_reports(zh):
    RELEASE_REPORT_KEYS_NO_REPO = RELEASE_REPORT_KEYS[:]
    RELEASE_REPORT_KEYS_NO_REPO.remove("repositories")
    data = zh.get_release_reports(REPO_ID)
    assert len(data) >= 4
    for item in data:
        assert list(item.keys()) == RELEASE_REPORT_KEYS_NO_REPO


def test_edit_release_report(zh):
    description = f"New Description {random.randint(0, 1000)}"
    data = zh.edit_release_report(
        RELEASE_REPORT,
        title="Test Release",
        start_date=datetime.datetime.now(),
        desired_end_date=datetime.datetime.now() + datetime.timedelta(days=60),
        description=description,
        state="open",
    )
    assert list(data.keys()) == RELEASE_REPORT_KEYS
    assert data["description"] == description


def test_edit_release_report_invalid(zh):
    with pytest.raises(ValueError):
        zh.edit_release_report(
            RELEASE_REPORT,
            title="Test Release",
            start_date=datetime.datetime.now(),
            desired_end_date=datetime.datetime.now()
            + datetime.timedelta(days=60),
            state="BLAH",
        )


def test_edit_release_report_invalid_dates(zh):
    with pytest.raises(ValueError):
        zh.edit_release_report(
            RELEASE_REPORT,
            title="Test Release",
            start_date=datetime.datetime.now() + datetime.timedelta(days=60),
            desired_end_date=datetime.datetime.now(),
        )


def test_add_repo_to_release_report(zh):
    data = zh.add_repo_to_release_report(
        RELEASE_REPORT,
        REPO_ID,
    )
    assert data


def test_remove_repo_from_release_report(zh):
    with pytest.raises(ZenhubError) as excinfo:
        zh.remove_repo_from_release_report(
            RELEASE_REPORT,
            REPO_ID,
        )
    assert (
        "Validation failed: Release must have at least one repository"
        in excinfo.value.args[0]
    )
