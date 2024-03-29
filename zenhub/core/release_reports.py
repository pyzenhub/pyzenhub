"""ZenHub release reports methods."""
import datetime
from typing import Iterable, List, Optional, Union

from ..models import ReleaseReport
from ..types import Base64String, ReportState
from ..utils import check_dates, date_to_string
from .base import BaseMixin


class ReleaseReportsMixin(BaseMixin):
    def create_release_report(
        self,
        repo_id: int,
        title: str,
        start_date: datetime.datetime,
        desired_end_date: datetime.datetime,
        description: str = "",
        repositories: Iterable[int] = (),
    ) -> Union[ReleaseReport, dict]:
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
        ReleaseReport or dict
            The created Release Report. See example response below.

        .. code-block:: python
            {
                "release_id": "59dff4f508399a35a276a1ea",
                "title": "Great title",
                "description": "Amazing description",
                "start_date": "2007-01-01T00:00:00.000Z",
                "desired_end_date": "2007-01-01T00:00:00.000Z",
                "created_at": "2017-10-12T23:04:21.795Z",
                "closed_at": None,
                "state": "open",
                "repositories": [103707262]
            }

        Note
        ----
        https://github.com/ZenHubIO/API#create-a-release-report
        """
        self._repo_id = repo_id
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
            body["repositories"] = list(repositories)  # type: ignore [assignment]

        data = self._post(url, body)
        model = ReleaseReport.parse_obj(data)
        return (
            model if self._output_models else model.dict(include=data.keys())
        )

    def get_release_report(
        self, release_id: Base64String
    ) -> Union[ReleaseReport, dict]:
        """
        Get a Release Report.

        Parameters
        ----------
        release_id : Base64String
            The unique string identifier of the Release Report.

        Returns
        -------
        ReleaseReport or dict
            The requested Release Report. See example response below.

        .. code-block:: python
            {
                "release_id": "59d3cd520a430a6344fd3bdb",
                "title": "Test release",
                "description": "",
                "start_date": "2017-10-01T19:00:00.000Z",
                "desired_end_date": "2017-10-03T19:00:00.000Z",
                "created_at": "2017-10-03T17:48:02.701Z",
                "closed_at": None,
                "state": "open",
                "repositories": [105683718]
            }
        Note
        ----
        https://github.com/ZenHubIO/API#get-a-release-report
        """
        # GET /p1/reports/release/:release_id
        url = f"/p1/reports/release/{release_id}"
        data = self._get(url)
        model = ReleaseReport.parse_obj(data)
        return (
            model if self._output_models else model.dict(include=data.keys())
        )

    def get_release_reports(
        self, repo_id: int
    ) -> Union[List[ReleaseReport], List[dict]]:
        """
        Get Release Reports for a Repository.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        List of ReleaseReport or List of dict. See example response below.

        .. code-block:: python
            [
                {
                    "release_id": "59cbf2fde010f7a5207406e8",
                    "title": "Great title for release 1",
                    "description": "Great description for release",
                    "start_date": "2000-10-10T00:00:00.000Z",
                    "desired_end_date": "2010-10-10T00:00:00.000Z",
                    "created_at": "2017-09-27T18:50:37.418Z",
                    "closed_at": None,
                    "state": "open"
                },
                {
                    "release_id": "59cbf2fde010f7a5207406e8",
                    "title": "Great title for release 2",
                    "description": "Great description for release",
                    "start_date": "2000-10-10T00:00:00.000Z",
                    "desired_end_date": "2010-10-10T00:00:00.000Z",
                    "created_at": "2017-09-27T18:50:37.418Z",
                    "closed_at": None,
                    "state": "open"
                }
            ]

        Note
        ----
        https://github.com/ZenHubIO/API#get-release-reports-for-a-repository
        """
        self._repo_id = repo_id
        # GET /p1/repositories/:repo_id/reports/releases
        url = f"/p1/repositories/{repo_id}/reports/releases"
        if self._output_models:
            return [ReleaseReport.parse_obj(item) for item in self._get(url)]
        else:
            return [
                ReleaseReport.parse_obj(item).dict(include=item.keys())
                for item in self._get(url)
            ]

    def edit_release_report(
        self,
        release_id: Base64String,
        title: str,
        start_date: datetime.datetime,
        desired_end_date: datetime.datetime,
        description: str = '',
        state: Optional[ReportState] = None,
    ) -> Union[ReleaseReport, dict]:
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
        ReleaseReport or dict
            The created Release Report. See example response below.

        .. code-block:: python
            {
                "release_id": "59d3d6438b3f16667f9e7174",
                "title": "Amazing title",
                "description": "Amazing description",
                "start_date": "2007-01-01T00:00:00.000Z",
                "desired_end_date": "2007-01-01T00:00:00.000Z",
                "created_at": "2017-10-03T18:26:11.700Z",
                "closed_at": "2017-10-03T18:26:11.700Z",
                "state": "closed",
                "repositories": [105683567, 105683718]
            }

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

        data = self._patch(url, body)
        model = ReleaseReport.parse_obj(data)
        return (
            model if self._output_models else model.dict(include=data.keys())
        )

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
        bool
            ``True`` if successful.

        Note
        ----
        https://github.com/ZenHubIO/API#add-a-repository-to-a-release-report
        """
        self._repo_id = repo_id
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
        bool
            ``True`` if successful.

        Note
        ----
        A release must always have at least one repository.
        https://github.com/ZenHubIO/API#remove-a-repository-from-a-release-report
        """
        self._repo_id = repo_id
        # DELETE /p1/reports/release/:release_id/repository/:repo_id
        url = f"/p1/reports/release/{release_id}/repository/{repo_id}"
        return True if self._delete(url) == {} else False
