"""ZenHub milestone methods."""
import datetime
from typing import Union

from ..models import MilestoneDate
from ..utils import date_to_string
from .base import BaseMixin


class MilestonesMixin(BaseMixin):
    def set_milestone_start_date(
        self,
        repo_id: int,
        milestone_number: int,
        start_date: datetime.datetime,
    ) -> Union[MilestoneDate, dict]:
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
        MilestoneDate or dict
            The milestone with the new start date. See example below.

        .. code-block:: python
            {
                "start_date": "2010-11-13T01:38:56.842Z",
            }

        Note
        ----
        https://github.com/ZenHubIO/API#set-milestone-start-date
        """
        self._repo_id = repo_id
        # POST /p1/repositories/:repo_id/milestones/:milestone_number/start_date
        url = (
            f"/p1/repositories/{repo_id}/milestones/"
            f"{milestone_number}/start_date"
        )
        body = {"start_date": date_to_string(start_date)}
        data = self._post(url, body)
        model = MilestoneDate.parse_obj(data)
        return (
            model if self._output_models else model.dict(include=data.keys())
        )

    def get_milestone_start_date(
        self, repo_id: int, milestone_number: int
    ) -> Union[MilestoneDate, dict]:
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
        MilestoneDate or dict
            The milestone with the current start date. See example below.

        .. code-block:: python
            {
                "start_date": "2010-11-13T01:38:56.842Z",
            }

        Note
        ----
        https://github.com/ZenHubIO/API#get-milestone-start-date
        """
        self._repo_id = repo_id
        # GET /p1/repositories/:repo_id/milestones/:milestone_number/start_date
        url = (
            f"/p1/repositories/{repo_id}/milestones/"
            f"{milestone_number}/start_date"
        )
        data = self._get(url)
        model = MilestoneDate.parse_obj(data)
        return (
            model if self._output_models else model.dict(include=data.keys())
        )
