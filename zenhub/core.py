# -----------------------------------------------------------------------------
# Copyright (c) 2022 Gonzalo Peña-Castellanos (@goanpeca)
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""ZenHub API."""
import datetime
from typing import Iterable, List, Optional, Union

import requests
from typing_extensions import NotRequired, TypedDict

from .exceptions import (
    APILimitError,
    InvalidTokenError,
    NotFoundError,
    ZenhubError,
)
from .models import (
    AddRemoveIssue,
    Issue,
    ReleaseReport,
    ReleaseReportWithRepositories,
)
from .types import (
    Base64String,
    ISO8601DateString,
    IssuePosition,
    ReportState,
    URLString,
)
from .utils import check_dates, date_to_string


# Types
# -----------------------------------------------------------------------------
class Workspace(TypedDict):
    name: str
    description: str
    id: Base64String
    repositories: List[int]


class IssueEstimate(TypedDict):
    value: int


class Estimate(TypedDict):
    estimate: int


class PipelineIssue(TypedDict):
    issue_number: int
    estimate: IssueEstimate
    position: NotRequired[IssuePosition]
    is_epic: NotRequired[bool]


class BoardPipeline(TypedDict):
    id: Base64String
    name: str
    issues: List[PipelineIssue]


class Board(TypedDict):
    pipelines: List[BoardPipeline]


class MilestoneDate(TypedDict):
    start_date: ISO8601DateString


class Dependency(TypedDict):
    blocking: Issue
    blocked: Issue


class Dependencies(TypedDict):
    dependencies: List[Dependency]


class PlusOnes(TypedDict):
    created_at: ISO8601DateString


class Pipeline(TypedDict):
    name: str
    pipeline_id: Base64String
    workspace_id: Base64String


class IssueData(TypedDict):
    estimate: IssueEstimate
    is_epic: bool
    plus_ones: List[PlusOnes]
    pipeline: Pipeline
    pipelines: List[Pipeline]


# Constants
# -----------------------------------------------------------------------------
DEFAULT_BASE_URL: URLString = "https://api.zenhub.com"


class Zenhub:
    """Zenhub API wrapper."""

    _HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "ZenHub Python Client",
    }

    def __init__(
        self,
        token: str,
        base_url: URLString = DEFAULT_BASE_URL,
        enterprise: int = 2,
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
    def _parse_response_contents(response: requests.Response) -> dict:
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

    def _make_url(self, url: URLString) -> URLString:
        """Create full api url."""
        return f"{self._base_url}{url}"

    def _get(self, url: URLString) -> dict:
        """Send GET request with given url."""
        response = self._session.get(url=self._make_url(url))
        return self._parse_response_contents(response)

    def _post(self, url: URLString, body: dict = {}) -> dict:
        """Send POST request with given url and data."""
        response = self._session.post(url=self._make_url(url), json=body)
        return self._parse_response_contents(response)

    def _put(self, url: URLString, body: dict) -> dict:
        """Send PUT request with given url and data."""
        response = self._session.put(url=self._make_url(url), json=body)
        return self._parse_response_contents(response)

    def _delete(self, url: URLString, body: dict = {}) -> dict:
        """Send DELETE request with given url and data."""
        response = self._session.delete(url=self._make_url(url), json=body)
        return self._parse_response_contents(response)

    def _patch(self, url: URLString, body: dict) -> dict:
        """Send PATCH request with given url and data."""
        response = self._session.patch(url=self._make_url(url), json=body)
        return self._parse_response_contents(response)

    # --- Issues
    # ------------------------------------------------------------------------
    def get_issue_data(self, repo_id: int, issue_number: int) -> IssueData:
        """
        Get the data for a specific issue.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        issue_number : int
            Repository issue number.

        Returns
        -------
        IssueData

        Note
        ----
        - ``pipeline`` references the oldest Workspace pipeline this issue
          is in.
        - If an issue's status is closed, the pipeline value will describe the
          Pipeline that the issue was in prior to the issue being closed.
          The ZenHub API does not consider the "Closed" Pipeline to be a
          distinct Pipeline at this time and you should not use the Pipeline
          value to determine whether or not an issue is closed or open (use
          status instead).
        - Reopened issues might take up to one minute to show up in the
          correct Pipeline.
        - ``pipelines`` contains all pipelines in all Workspaces this issue
          is in.

        https://github.com/ZenHubIO/API#get-issue-data
        """
        # GET /p1/repositories/:repo_id/issues/:issue_number
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}"
        return self._get(url)  # type: ignore

    def get_issue_events(self, repo_id: int, issue_number: int) -> dict:
        """
        Get the events for an issue.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        issue_number : int
            Repository issue number.

        Returns
        -------
        dict

        Note
        ----
        https://github.com/ZenHubIO/API#get-issue-events
        """
        # GET /p1/repositories/:repo_id/issues/:issue_number/events
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}/events"
        return self._get(url)

    def move_issue(
        self,
        workspace_id: Base64String,
        repo_id: int,
        issue_number: int,
        pipeline_id: Base64String,
        position: Union[int, IssuePosition],
    ) -> dict:
        """
        Moves an issue between Pipelines in a Workspace.

        Parameters
        ----------
        workspace_id : Base64String
            ID of the workspace.
        repo_id : int
            ID of the repository, not its full name.
        issue_number : int
            Repository issue number.
        pipeline_id : Base64String
            ID of the pipeline, not its full name.
        position : int
            Can be specified as top or bottom, or a 0-based position in the
            Pipeline such as 1, which would be the second position in the
            Pipeline.

        Returns
        -------
        Empty dict if succesful.

        Note
        ----
        https://github.com/ZenHubIO/API#move-an-issue-between-pipelines
        """
        # POST /p2/workspaces/:workspace_id/repositories/:repo_id/issues/:issue_number/moves
        url = (
            f"/p2/workspaces/{workspace_id}/repositories/"
            f"{repo_id}/issues/{issue_number}/moves"
        )
        body = {"pipeline_id": pipeline_id, "position": position}
        return self._post(url, body)

    def move_issue_in_oldest_workspace(
        self,
        repo_id: int,
        issue_number: int,
        pipeline_id: Base64String,
        position: Union[int, IssuePosition],
    ) -> dict:
        """
        Moves an issue between Pipelines in a Workspace.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        issue_number : int
            Repository issue number.
        pipeline_id : Base64String
            ID of the pipeline, not its full name.
        position : int or IssuePosition
            Can be specified as top or bottom, or a 0-based position in the
            Pipeline such as 1, which would be the second position in the
            Pipeline.

        Returns
        -------
        Empty dict if succesful.

        Note
        ----
        https://github.com/ZenHubIO/API#move-an-issue-between-pipelines-in-the-oldest-workspace
        """
        # POST /p1/repositories/:repo_id/issues/:issue_number/moves
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}/moves"
        body = {"pipeline_id": pipeline_id, "position": position}
        return self._post(url, body)

    def set_issue_estimate(
        self, repo_id: int, issue_number: int, estimate: int
    ) -> Estimate:
        """
        Set Issue Estimate.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        issue_number : int
            Repository issue number.
        estimate : int
            The estimate for the issue.

        Returns
        -------
        Estimate

        Note
        ----
        https://github.com/ZenHubIO/API#set-issue-estimate
        """
        # PUT /p1/repositories/:repo_id/issues/:issue_number/estimate
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}/estimate"
        body = {"estimate": estimate}
        return self._put(url, body)  # type: ignore

    # --- Epics
    # ------------------------------------------------------------------------
    def get_epics(self, repo_id: int) -> dict:
        """
        Get all Epics for a repository.

        Note
        ----
        https://github.com/ZenHubIO/API#get-epics-for-a-repository
        """
        url = f"/p1/repositories/{repo_id}/epics"
        return self._get(url)

    def get_epic_data(self, repo_id: int, epic_id: int) -> dict:
        """
        Get all Epics for a repository.

        Note
        ----
        https://github.com/ZenHubIO/API#get-epic-data
        """
        url = f"/p1/repositories/{repo_id}/epics/{epic_id}"
        return self._get(url)

    def convert_epic_to_issue(self, repo_id: int, issue_number: int) -> dict:
        """
        Converts an Epic back to a regular issue.

        Note
        ----
        https://github.com/ZenHubIO/API#convert-an-epic-to-an-issue
        """
        url = (
            f"/p1/repositories/{repo_id}/epics/{issue_number}/convert_to_issue"
        )
        return self._post(url)

    def convert_issue_to_epic(self, repo_id: int, issue_number: int) -> dict:
        """
        Converts an issue to an Epic, along with any issues that should be
        part of it.

        Note
        ----
        https://github.com/ZenHubIO/API#convert-issue-to-epic
        """
        url = (
            f"/p1/repositories/{repo_id}/issues/{issue_number}/convert_to_epic"
        )
        return self._post(url)

    def add_or_remove_issues_to_epic(
        self,
        repo_id: int,
        issue_number: int,
        remove_issues: Iterable[Issue] = (),
        add_issues: Iterable[Issue] = (),
    ) -> dict:
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
        body = {
            "remove_issues": remove_issues or [],
            "add_issues": add_issues or [],
        }
        return self._post(url, body)

    # --- Workspaces
    # ------------------------------------------------------------------------
    def get_workspaces(self, repo_id: int) -> List[Workspace]:
        """
        Gets all Workspaces containing repo_id.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        List of Workspace.
            Zenhub list of workspaces.

        Note
        ----
        https://github.com/ZenHubIO/API#get-zenhub-workspaces-for-a-repository
        """
        # GET /p2/repositories/:repo_id/workspaces
        url = f"/p2/repositories/{repo_id}/workspaces"
        return self._get(url)  # type: ignore

    def get_repository_board(
        self, workspace_id: Base64String, repo_id: int
    ) -> Board:
        """
        Get ZenHub Board data for a repository (repo_id) within the Workspace
        (workspace_id).

        Parameters
        ----------
        workspace_id : Base64String
            Workspace unique string identifier.
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        Board
            Zenhub workspace board listing pipelines and issues.

        Note
        ----
        https://github.com/ZenHubIO/API#get-a-zenhub-board-for-a-repository
        """
        # GET /p2/workspaces/:workspace_id/repositories/:repo_id/board
        url = f"/p2/workspaces/{workspace_id}/repositories/{repo_id}/board"
        return self._get(url)  # type: ignore

    def get_oldest_repository_board(self, repo_id: int) -> Board:
        """
        Get the oldest ZenHub board for a repository.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        Board
            Zenhub workspace board listing pipelines and issues.

        Note
        ----
        https://github.com/ZenHubIO/API#get-the-oldest-zenhub-board-for-a-repository
        """
        # GET /p1/repositories/:repo_id/board
        url = f"/p1/repositories/{repo_id}/board"
        return self._get(url)  # type: ignore

    # --- Milestones
    # ------------------------------------------------------------------------
    def set_milestone_start_date(
        self,
        repo_id: int,
        milestone_number: int,
        start_date: datetime.datetime,
    ) -> MilestoneDate:
        """
        Set milestone start date.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        milestone_number : int
            ID of the milestone, not its full name.
        start_date : datetime.datetime
            Start date of the milestone.

        Returns
        -------
        MilestoneDate
            The milestone with the new start date.
        Note
        ----
        https://github.com/ZenHubIO/API#set-milestone-start-date
        """
        # POST /p1/repositories/:repo_id/milestones/:milestone_number/start_date
        url = (
            f"/p1/repositories/{repo_id}/milestones/"
            f"{milestone_number}/start_date"
        )
        body = {"start_date": date_to_string(start_date)}
        return self._post(url, body)  # type: ignore

    def get_milestone_start_date(
        self, repo_id: int, milestone_number: int
    ) -> MilestoneDate:
        """
        Get milestone start date.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        milestone_number : int
            ID of the milestone, not its full name.
        start_date : datetime.datetime
            Start date of the milestone.

        Returns
        -------
        MilestoneDate
            The milestone with the current start date.

        Note
        ----
        https://github.com/ZenHubIO/API#get-milestone-start-date
        """
        # GET /p1/repositories/:repo_id/milestones/:milestone_number/start_date
        url = (
            f"/p1/repositories/{repo_id}/milestones/"
            f"{milestone_number}/start_date"
        )
        return self._get(url)  # type: ignore

    # --- Dependencies
    # ------------------------------------------------------------------------
    def get_dependencies(self, repo_id: int) -> Dependencies:
        """
        Get Dependencies for a Repository.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.

        Note
        ----
        https://github.com/ZenHubIO/API#get-dependencies-for-a-repository
        """
        # GET /p1/repositories/:repo_id/dependencies
        url = f"/p1/repositories/{repo_id}/dependencies"
        return self._get(url)  # type: ignore

    def create_dependency(
        self,
        blocking_repo_id: int,
        blocking_issue_number: int,
        blocked_repo_id: int,
        blocked_issue_number: int,
    ) -> dict:
        """
        Create a dependency.

        Parameters
        ----------
        blocking_repo_id: int
            ID of the repository, not its full name of the blocking issue.
        blocking_issue_number: int
            Blocking issue number.
        blocked_repo_id: int
            ID of the repository, not its full name of the blocked issue.
        blocked_issue_number: int
            Blocked issue number.

        Returns
        -------
        Empty dictionary on success.

        Note
        ----
        https://github.com/ZenHubIO/API#create-a-dependency
        """
        # POST /p1/dependencies
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
        blocking_repo_id: int,
        blocking_issue_number: int,
        blocked_repo_id: int,
        blocked_issue_number: int,
    ) -> dict:
        """
        Remove a dependency.

        Parameters
        ----------
        blocking_repo_id: int
            ID of the repository, not its full name of the blocking issue.
        blocking_issue_number: int
            Blocking issue number.
        blocked_repo_id: int
            ID of the repository, not its full name of the blocked issue.
        blocked_issue_number: int
            Blocked issue number.

        Returns
        -------
        Empty dictionary on success.

        Note
        ----
        https://github.com/ZenHubIO/API#remove-a-dependency
        """
        # DELETE /p1/dependencies
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
        repo_id: int,
        title: str,
        start_date: datetime.datetime,
        desired_end_date: datetime.datetime,
        description: str = "",
        repositories: Iterable[int] = (),
    ) -> ReleaseReportWithRepositories:
        """
        Create a Release Report.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        title : str
            Title of the Release Report.
        start_date : datetime.datetime
            Start date of the Release Report.
        desired_end_date : datetime.datetime
            End date of the Release Report.
        description : str, optional
            Start date of the Release Report. The default is ''.
        repositories : Iterable of int, optional
            List of repository IDs to include in the Release Report.
            The default is ().

        Returns
        -------
        ReleaseReportWithRepositories
            The created Release Report.

        Note
        ----
        https://github.com/ZenHubIO/API#create-a-release-report
        """
        check_dates(start_date, desired_end_date)
        # POST /p1/repositories/:repo_id/reports/release
        url = f"/p1/repositories/{repo_id}/reports/release"
        body = {
            "title": title,
            "start_date": date_to_string(start_date),
            "desired_end_date": date_to_string(desired_end_date),
        }
        if description:
            body["description"] = description

        if repositories:
            body["repositories"] = list(repositories)  # type: ignore

        return ReleaseReportWithRepositories.parse_obj(self._post(url, body))

    def get_release_report(self, release_id: Base64String) -> dict:
        """
        Get a Release Report.

        Parameters
        ----------
        release_id : Base64String
            The unique string identifier of the Release Report.

        Returns
        -------
        dict
            The requested Release Report.

        Note
        ----
        https://github.com/ZenHubIO/API#get-a-release-report
        """
        # GET /p1/reports/release/:release_id
        url = f"/p1/reports/release/{release_id}"
        return ReleaseReportWithRepositories.parse_obj(self._get(url)).dict()

    def get_release_reports(self, repo_id: int) -> List[dict]:
        """
        Get Release Reports for a Repository.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        List of dictionaries.

        Note
        ----
        https://github.com/ZenHubIO/API#get-release-reports-for-a-repository
        """
        # GET /p1/repositories/:repo_id/reports/releases
        url = f"/p1/repositories/{repo_id}/reports/releases"
        data = [
            ReleaseReport.parse_obj(item).dict() for item in self._get(url)
        ]
        return data

    def edit_release_report(
        self,
        release_id: Base64String,
        title: str,
        start_date: datetime.datetime,
        desired_end_date: datetime.datetime,
        description: str = "",
        state: Optional[ReportState] = None,
    ) -> dict:
        """
        Edit a Release Report.

        Parameters
        ----------
        release_id : Base64String
            The unique string identifier of the Release Report.
        title : str
            Title of the Release Report.
        start_date : datetime.datetime
            Start date of the Release Report.
        desired_end_date : datetime.datetime
            End date of the Release Report.
        description : str, optional
            Start date of the Release Report. The default is ''.
        state : ReportState, optional
            The state the Release Report. The default is None.

        Returns
        -------
        dict
            The created Release Report.
        Note
        ----
        https://github.com/ZenHubIO/API#edit-a-release-report
        """
        check_dates(start_date, desired_end_date)
        # PATCH /p1/reports/release/:release_id
        url = f"/p1/reports/release/{release_id}"
        body = {
            "title": title,
            "description": description,
            "start_date": date_to_string(start_date),
            "desired_end_date": date_to_string(desired_end_date),
        }
        if state is not None:
            if state in ["open", "closed"]:
                body["state"] = state
            else:
                raise ValueError("`state` must be 'open' or 'closed'")

        return ReleaseReportWithRepositories.parse_obj(
            self._patch(url, body)
        ).dict()

    def add_repo_to_release_report(
        self, release_id: Base64String, repo_id: int
    ) -> bool:
        """
        Add a Repository to a Release Report.

        Parameters
        ----------
        release_id : Base64String
            The unique string identifier of the Release Report.
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        ``True`` if successful.

        Note
        ----
        https://github.com/ZenHubIO/API#add-a-repository-to-a-release-report
        """
        # POST /p1/reports/release/:release_id/repository/:repo_id
        url = f"/p1/reports/release/{release_id}/repository/{repo_id}"
        return True if self._post(url) == {} else False

    def remove_repo_from_release_report(
        self, release_id: Base64String, repo_id: int
    ) -> bool:
        """
        Remove a Repository from a Release Report.

        Parameters
        ----------
        release_id : Base64String
            The unique string identifier of the Release Report.
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        ``True`` if successful.

        Note
        ----
        A release must always have at least one repository.
        https://github.com/ZenHubIO/API#remove-a-repository-from-a-release-report
        """
        # DELETE /p1/reports/release/:release_id/repository/:repo_id
        url = f"/p1/reports/release/{release_id}/repository/{repo_id}"
        return True if self._delete(url) == {} else False

    # --- Release Report Issues
    # ------------------------------------------------------------------------
    def get_release_report_issues(
        self, release_id: Base64String
    ) -> List[dict]:
        """
        Get all the Issues for a Release Report.

        Parameters
        ----------
        release_id : Base64String
            The unique string identifier of the Release Report.

        Returns
        -------
        List of dictionaries.

        Note
        ----
        https://github.com/ZenHubIO/API#get-all-the-issues-for-a-release-report
        """
        # GET /p1/reports/release/:release_id/issues
        url = f"/p1/reports/release/{release_id}/issues"
        return [Issue.parse_obj(issue).dict() for issue in self._get(url)]

    def add_or_remove_issues_from_release_report(
        self,
        release_id: Base64String,
        add_issues: Iterable[Issue] = (),
        remove_issues: Iterable[Issue] = (),
    ) -> dict:
        """
        Add or Remove Issues to or from a Release Report.

        Adding and removing issues can be done in the same request by
        providing both ``add_issues`` and ``remove_issues`` parameters.

        Parameters
        ----------
        release_id : Base64String
            The unique string identifier of the Release Report.
        add_issues : Iterable of Issue
            An iterable of dictionaries with ``repo_id`` and ``issue_number``
            keys to add to the Release Report.
        remove_issues : Iterable of Issue
            An iterable of dictionaries with ``repo_id`` and ``issue_number``
            keys to remove from the Release Report.

        Returns
        -------
        dict
            The added or removed issues.

        Note
        ----
        https://github.com/ZenHubIO/API#add-or-remove-issues-to-or-from-a-release-report
        """
        # PATCH /p1/reports/release/:release_id/issues
        url = f"/p1/reports/release/{release_id}/issues"
        body = {
            'add_issues': list(add_issues),
            'remove_issues': list(remove_issues),
        }
        return AddRemoveIssue.parse_obj(self._patch(url, body)).dict()
