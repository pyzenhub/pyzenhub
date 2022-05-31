"""ZenHub issues methods."""
from typing import List, Optional, Union

from ..models import (
    Estimate,
    EstimateIssueEvent,
    Event,
    IssueData,
    TransferIssueEvent,
)
from ..types import Base64String, IssuePosition
from .base import BaseMixin


class IssuesMixin(BaseMixin):
    def get_issue_data(
        self, repo_id: int, issue_number: int
    ) -> Union[IssueData, dict]:
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
        IssueData or dict
            The issue data dictionary. See example response below.

        .. code-block:: python
            {
                "estimate": {
                    "value": 8
                },
                "plus_ones": [
                    {
                        "created_at": "2015-12-11T18:43:22.296Z"
                    }
                ],
                "pipeline": {
                    "name": "QA",
                    "pipeline_id": "5d0a7a9741fd098f6b7f58a7",
                    "workspace_id": "5d0a7a9741fd098f6b7f58ac"
                },
                "pipelines": [
                    {
                        "name": "QA",
                        "pipeline_id": "5d0a7a9741fd098f6b7f58a7",
                        "workspace_id": "5d0a7a9741fd098f6b7f58ac"
                    },
                    {
                        "name": "Done",
                        "pipeline_id": "5d0a7cea41fd098f6b7f58b7",
                        "workspace_id": "5d0a7cea41fd098f6b7f58b8"
                    }
                ],
                "is_epic": True
            }

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
        self._repo_id = repo_id
        # GET /p1/repositories/:repo_id/issues/:issue_number
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}"
        data = self._get(url)
        model = IssueData.parse_obj(data)
        return (
            model if self._output_models else model.dict(include=data.keys())
        )

    def get_issue_events(
        self, repo_id: int, issue_number: int
    ) -> Union[List[Event], List[dict]]:
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
        List of Event or List of dict
            See example response below.

        .. code-block:: python
            [
                {
                    "user_id": 16717,
                    "type": "estimateIssue",
                    "created_at": "2015-12-11T19:43:22.296Z",
                    "from_estimate": {
                        "value": 8
                    }
                },
                {
                    "user_id": 16717,
                    "type": "estimateIssue",
                    "created_at": "2015-12-11T18:43:22.296Z",
                    "from_estimate": {
                        "value": 4
                    },
                    "to_estimate": {
                        "value": 8
                    }
                },
                {
                    "user_id": 16717,
                    "type": "estimateIssue",
                    "created_at": "2015-12-11T13:43:22.296Z",
                    "to_estimate": {
                        "value": 4
                    }
                },
                {
                    "user_id": 16717,
                    "type": "transferIssue",
                    "created_at": "2015-12-11T12:43:22.296Z",
                    "from_pipeline": {
                        "name": "Backlog"
                    },
                    "to_pipeline": {
                        "name": "In progress"
                    },
                    "workspace_id": "5d0a7a9741fd098f6b7f58ac"
                },
                {
                    "user_id": 16717,
                    "type": "transferIssue",
                    "created_at": "2015-12-11T11:43:22.296Z",
                    "to_pipeline": {
                        "name": "Backlog"
                    }
                }
            ]

        Note
        ----
        - Returns issue events, sorted by creation time, most recent first.
        - Each event contains the User ID of the user who performed the
          change, the Creation Date of the event, and the event Type.
        - Type can be either estimateIssue or transferIssue. The values before
          and after the event are included in the event data.
        - transferIssue events include a workspace_id indicating in which
          Workspace the transfer occurred.

        https://github.com/ZenHubIO/API#get-issue-events
        """
        self._repo_id = repo_id
        # GET /p1/repositories/:repo_id/issues/:issue_number/events
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}/events"
        events: List[dict] = self._get(url)  # type: ignore
        event_models: List[Event] = []
        for event in events:
            event_model: Optional[Event] = None
            if event["type"] == "estimateIssue":
                event_model = EstimateIssueEvent.parse_obj(event)
            elif event["type"] == "transferIssue":
                event_model = TransferIssueEvent.parse_obj(event)

            if event_model:
                event_models.append(event_model)

        return event_models if self._output_models else events

    def move_issue(
        self,
        workspace_id: Base64String,
        repo_id: int,
        issue_number: int,
        pipeline_id: Base64String,
        position: Union[int, IssuePosition],
    ) -> bool:
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
        bool
            ``True`` if successful.

        Note
        ----
        https://github.com/ZenHubIO/API#move-an-issue-between-pipelines
        """
        self._repo_id = repo_id
        # POST /p2/workspaces/:workspace_id/repositories/:repo_id/issues/:issue_number/moves
        url = (
            f"/p2/workspaces/{workspace_id}/repositories/"
            f"{repo_id}/issues/{issue_number}/moves"
        )
        body = {"pipeline_id": pipeline_id, "position": position}
        return True if self._post(url, body) == {} else False

    def move_issue_in_oldest_workspace(
        self,
        repo_id: int,
        issue_number: int,
        pipeline_id: Base64String,
        position: Union[int, IssuePosition],
    ) -> bool:
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
        bool
            ``True`` if successful.

        Note
        ----
        https://github.com/ZenHubIO/API#move-an-issue-between-pipelines-in-the-oldest-workspace
        """
        self._repo_id = repo_id
        # POST /p1/repositories/:repo_id/issues/:issue_number/moves
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}/moves"
        body = {"pipeline_id": pipeline_id, "position": position}
        return True if self._post(url, body) == {} else False

    def set_issue_estimate(
        self, repo_id: int, issue_number: int, estimate: int
    ) -> Union[Estimate, dict]:
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
        Estimate or dict.
            See example response below.

        .. code-block:: python
            {
                "estimate": 15,
            }

        Note
        ----
        https://github.com/ZenHubIO/API#set-issue-estimate
        """
        self._repo_id = repo_id
        # PUT /p1/repositories/:repo_id/issues/:issue_number/estimate
        url = f"/p1/repositories/{repo_id}/issues/{issue_number}/estimate"
        body = {"estimate": estimate}
        data = self._put(url, body)
        model = Estimate.parse_obj(data)
        return (
            model if self._output_models else model.dict(include=data.keys())
        )
