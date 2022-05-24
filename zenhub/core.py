# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2022 Gonzalo Peña-Castellanos (@goanpeca)
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""ZenHub API."""
import datetime
from typing import NewType, TypedDict, List, Optional

import requests

# Constants
# -----------------------------------------------------------------------------
DEFAULT_BASE_URL = "https://api.zenhub.com"

# Types
# -----------------------------------------------------------------------------
URLString = NewType('URLString', str)


class Issue(TypedDict):
    repo_id : int
    issue_number : int


# Exceptions
# -----------------------------------------------------------------------------
class ZenhubError(Exception):
    pass


class InvalidTokenError(ZenhubError):
    pass


class APILimitError(ZenhubError):
    pass


class NotFoundError(ZenhubError):
    pass


class Zenhub:
    """Zenhub API wrapper."""

    _HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "ZenHub Python Client",
    }

    def __init__(
        self, token: str, base_url: URLString = DEFAULT_BASE_URL, enterprise: int = 2
    ):
        """ZenHub API wrapper."""
        self._session = requests.Session()
        if enterprise == 3 and base_url != DEFAULT_BASE_URL:
            if base_url.endswith("/"):
                base_url = base_url + "api"
            else:
                base_url = base_url + "/api"

        self._base_url = base_url

        # Setup
        self._session.headers.update(self._HEADERS)
        self._session.headers.update({"X-Authentication-Token": token})

    # --- Helpers
    # ------------------------------------------------------------------------
    @staticmethod
    def _parse_response_contents(response):
        """Parse response and convert to json if possible."""
        contents = {}
        status_code = response.status_code
        if status_code in [200, 204]:
            if response.text:
                try:
                    contents = response.json()
                except Exception as err:
                    print(err)
        elif status_code == 401:
            raise InvalidTokenError("Invalid token!")
        elif status_code == 403:
            raise APILimitError("Reached request limit to the API. See API Limits.")
        elif status_code == 404:
            raise NotFoundError("Not found!")
        else:
            raise ZenhubError("Unknown error!")

        return contents

    @staticmethod
    def _check_date(date):
        """Check date and transform to valid format."""
        if isinstance(date, datetime.datetime):
            date = date.replace(microsecond=0).isoformat() + "Z"

        return date

    def _make_url(self, url : URLString):
        """Create full api url."""
        return "{}{}".format(self._base_url, url)

    def _get(self, url : URLString):
        """Send GET request with given url."""
        response = self._session.get(url=self._make_url(url))
        return self._parse_response_contents(response)

    def _post(self, url : URLString, body={}):
        """Send POST request with given url and data."""
        response = self._session.post(url=self._make_url(url), json=body)
        return self._parse_response_contents(response)

    def _put(self, url : URLString, body):
        """Send PUT request with given url and data."""
        response = self._session.put(url=self._make_url(url), json=body)
        return self._parse_response_contents(response)

    def _delete(self, url : URLString, body={}):
        """Send DELETE request with given url and data."""
        response = self._session.delete(url=self._make_url(url), json=body)
        return self._parse_response_contents(response)

    def _patch(self, url : URLString, body):
        """Send PATCH request with given url and data."""
        response = self._session.patch(url=self._make_url(url), json=body)
        return self._parse_response_contents(response)

    # --- Issues
    # ------------------------------------------------------------------------
    def get_issue_data(self, repo_id : int, issue_number : int) -> dict:
        """
        Get the data for a specific issue.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        issue_number : int
            Reposirtory issue number.

        Returns
        -------
        dict

        See: https://github.com/ZenHubIO/API#get-issue-data
        """
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}"
        return self._get(url)

    def get_issue_events(self, repo_id: int, issue_number: int) -> dict:
        """
        Get the events for an issue.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        issue_number : int
            Reposirtory issue number.

        Returns
        -------
        dict

        Note
        ----
        https://github.com/ZenHubIO/API#get-issue-events
        """
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}/events"
        return self._get(url)

    def move_issue(self, workspace_id, repo_id, issue_number, pipeline_id, position):
        """
        Moves an issue between Pipelines in a Workspace.

        Parameters
        ----------
        workspace_id : int
            ID of the workspace.
        repo_id : int
            ID of the repository, not its full name.
        issue_number : int
            Reposirtory issue number.
        pipeline_id : int
            ID of the pipeline, not its full name.
        position FIXME:

        Note
        ----
        https://github.com/ZenHubIO/API#move-an-issue-between-pipelines
        """
        url = f"/p2/workspaces/{workspace_id}/repositories/{repo_id}/issues/{issue_number}/moves"
        body = {"pipeline_id": pipeline_id, "position": position}
        return self._post(url, body)

    def move_issue_in_oldest_workspace(
        self, repo_id, issue_number, pipeline_id, position
    ):
        """
        Moves an issue between Pipelines in a Workspace.

        Note
        ----
        https://github.com/ZenHubIO/API#move-an-issue-between-pipelines-in-the-oldest-workspace
        """
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}/moves"
        body = {"pipeline_id": pipeline_id, "position": position}
        return self._post(url, body)

    def set_issue_estimate(self, repo_id, issue_number, estimate):
        """
        Set Issue Estimate.

        Note
        ----
        https://github.com/ZenHubIO/API#set-issue-estimate
        """
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}/estimate"
        body = {"estimate": estimate}
        return self._put(url, body)

    # --- Epics
    # ------------------------------------------------------------------------
    def get_epics(self, repo_id):
        """
        Get all Epics for a repository.

        Note
        ----
        https://github.com/ZenHubIO/API#get-epics-for-a-repository
        """
        url = f"/p1/repositories/{repo_id}/epics"
        return self._get(url)

    def get_epic_data(self, repo_id, epic_id):
        """
        Get all Epics for a repository.

        Note
        ----
        https://github.com/ZenHubIO/API#get-epic-data
        """
        url = f"/p1/repositories/{repo_id}/epics/{epic_id}"
        return self._get(url)

    def convert_epic_to_issue(self, repo_id, issue_number):
        """
        Converts an Epic back to a regular issue.

        Note
        ----
        https://github.com/ZenHubIO/API#convert-an-epic-to-an-issue
        """
        url = f"/p1/repositories/{repo_id}/epics/{issue_number}/convert_to_issue"
        return self._post(url)

    def convert_issue_to_epic(self, repo_id, issue_number):
        """
        Converts an issue to an Epic, along with any issues that should be part of it.

        Note
        ----
        https://github.com/ZenHubIO/API#convert-issue-to-epic
        """
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}/convert_to_epic"
        return self._post(url)

    def add_or_remove_issues_to_epic(
        self, repo_id, issue_number, remove_issues=None, add_issues=None
    ):
        """
        Bulk add or remove issues to an Epic.

        The result returns which issue was added or removed from the Epic.

        remove_issues	[{repo_id: Number, issue_number: Number}]
        add_issues	[{repo_id: Number, issue_number: Number}]

        Note
        ----
        https://github.com/ZenHubIO/API#add-or-remove-issues-to-epic
        """
        url = f"/p1/repositories/{repo_id}/epics/{issue_number}/update_issues"
        body = {"remove_issues": remove_issues or [], "add_issues": add_issues or []}
        return self._post(url, body)

    # --- Workspaces
    # ------------------------------------------------------------------------
    def get_workspaces(self, repo_id):
        """
        Gets all Workspaces containing repo_id.

        Note
        ----
        https://github.com/ZenHubIO/API#get-zenhub-workspaces-for-a-repository
        """
        url = f"/p2/repositories/{repo_id}/workspaces"
        return self._get(url)

    def get_repository_board(self, workspace_id, repo_id):
        """
        Get ZenHub Board data for a repository (repo_id) within the Workspace (workspace_id).

        Note
        ----
        https://github.com/ZenHubIO/API#get-a-zenhub-board-for-a-repository
        """
        url = f"/p2/workspaces/{workspace_id}/repositories/{repo_id}/board"
        return self._get(url)

    def get_oldest_repository_board(self, repo_id):
        """
        Get the oldest ZenHub board for a repository.

        Note
        ----
        https://github.com/ZenHubIO/API#get-the-oldest-zenhub-board-for-a-repository
        """
        url = f"/p1/repositories/{repo_id}/board"
        return self._get(url)

    # --- Milestones
    # ------------------------------------------------------------------------
    def set_milestone_start_date(self, repo_id, milestone_number, start_date):
        """
        Set milestone start date.

        Note
        ----
        https://github.com/ZenHubIO/API#set-milestone-start-date
        """
        url = f"/p1/repositories/{repo_id}/milestones/{milestone_number}/start_date"
        body = {"start_date": self._check_date(start_date)}
        return self._post(url, body)

    def get_milestone_start_date(self, repo_id, milestone_number):
        """
        Get milestone start date.

        Note
        ----
        https://github.com/ZenHubIO/API#get-milestone-start-date
        """
        url = f"/p1/repositories/{repo_id}/milestones/{milestone_number}/start_date"
        return self._get(url)

    # --- Dependencies
    # ------------------------------------------------------------------------
    def get_dependencies(self, repo_id):
        """
        Get Dependencies for a Repository.

        Note
        ----
        https://github.com/ZenHubIO/API#get-dependencies-for-a-repository
        """
        url = f"/p1/repositories/{repo_id}/dependencies"
        return self._get(url)

    def create_dependency(
        self,
        blocking_repo_id,
        blocking_issue_number,
        blocked_repo_id,
        blocked_issue_number,
    ):
        """
        Create a dependency.

        Note
        ----
        https://github.com/ZenHubIO/API#create-a-dependency
        """
        url = "/p1/dependencies"
        body = {
            "blocking": {
                "repo_id": blocking_repo_id,
                "issue_number": blocking_issue_number,
            },
            "blocked": {
                "repo_id": blocked_repo_id,
                "issue_number": blocked_issue_number,
            },
        }
        return self._post(url, body)

    def remove_dependency(
        self,
        blocking_repo_id,
        blocking_issue_number,
        blocked_repo_id,
        blocked_issue_number,
    ):
        """
        Remove a dependency.

        Note
        ----
        https://github.com/ZenHubIO/API#remove-a-dependency
        """
        url = "/p1/dependencies"
        body = {
            "blocking": {
                "repo_id": blocking_repo_id,
                "issue_number": blocking_issue_number,
            },
            "blocked": {
                "repo_id": blocked_repo_id,
                "issue_number": blocked_issue_number,
            },
        }
        return self._delete(url, body)

    # --- Release Reports
    # ------------------------------------------------------------------------
    def create_release_report(
        self,
        repo_id,
        title,
        start_date,
        desired_end_date,
        description=None,
        repositories=None,
    ):
        """
        Create a Release Report.

        Note
        ----
        https://github.com/ZenHubIO/API#create-a-release-report
        """
        url = f"/p1/repositories/{repo_id}/reports/release"
        body = {
            "title": title,
            "start_date": self._check_date(start_date),
            "desired_end_date": self._check_date(desired_end_date),
        }
        if description:
            body["description"] = description

        if repositories:
            body["repositories"] = repositories

        return self._post(url, body)

    def get_release_report(self, release_id):
        """
        Get a Release Report.

        Note
        ----
        https://github.com/ZenHubIO/API#get-a-release-report
        """
        url = f"/p1/reports/release/{release_id}"
        return self._get(url)

    def get_release_reports(self, repo_id):
        """
        Get Release Reports for a Repository.

        Note
        ----
        https://github.com/ZenHubIO/API#get-release-reports-for-a-repository
        """
        url = f"/p1/repositories/{repo_id}/reports/releases"
        return self._get(url)

    def edit_release_report(
        self, release_id, title, description, start_date, desired_end_date, state=None
    ):
        """
        Edit a Release Report.

        Note
        ----
        https://github.com/ZenHubIO/API#edit-a-release-report
        """
        url = f"/p1/reports/release/{release_id}"
        body = {
            "title": title,
            "description": description,
            "start_date": self._check_date(start_date),
            "desired_end_date": self._check_date(desired_end_date),
        }
        if state is not None and state in ["open", "closed"]:
            body["state"] = state

        return self._patch(url, body)

    def add_repo_to_release_report(self, release_id, repo_id):
        """
        Add a Repository to a Release Report.

        Note
        ----
        https://github.com/ZenHubIO/API#add-a-repository-to-a-release-report
        """
        url = f"/p1/reports/release/{release_id}/repository/{repo_id}"
        return self._post(url)

    def remove_repo_from_release_report(self, release_id, repo_id):
        """
        Remove a Repository from a Release Report.

        Note
        ----
        https://github.com/ZenHubIO/API#remove-a-repository-from-a-release-report
        """
        url = f"/p1/reports/release/{release_id}/repository/{repo_id}"
        return self._delete(url)

    # --- Release Report Issues
    # ------------------------------------------------------------------------
    def get_release_report_issues(self, release_id):
        """
        Get all the Issues for a Release Report.

        Note
        ----
        https://github.com/ZenHubIO/API#get-all-the-issues-for-a-release-report
        """
        url = f"/p1/reports/release/{release_id}/issues"
        return self._get(url)

    def add_or_remove_issues_from_release_report(
        self, release_id : int, add_issues : Optional[List[Issue]] = None, remove_issues: Optional[List[Issue]]=None
    ):
        """
        Add or Remove Issues to or from a Release Report.

        Parameters
        ----------
        release_id : int
            The ID of the Release Report.
        add_issues :
            A list of dictionaries with ``repo_id`` and ``issue_number`` to
            add to the Release Report.
        remove_issues :
            A list of dictionaries with ``repo_id`` and ``issue_number`` to
            remove from the Release Report.

add_issues		Required, array of Objects with repo_id and issue_number
remove_issues	[{repo_id: Number, issue_number: Number}]	Required, array of Objects with repo_id and issue_number
        Note
        ----
        https://github.com/ZenHubIO/API#add-or-remove-issues-to-or-from-a-release-report
        """
        url = f"/p1/reports/release/{release_id}/issues"
        body = {"add_issues": add_issues or [], "remove_issues": remove_issues or []}
        return self._patch(url, body)
