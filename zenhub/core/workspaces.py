"""ZenHub release reports methods."""
import datetime
from typing import List

from ..types import Base64String, Board, MilestoneDate, Workspace
from ..utils import date_to_string
from .base import BaseMixin


class WorkspacesMixin(BaseMixin):
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
