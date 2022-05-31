"""ZenHub workspace methods."""
from typing import List, Union

from .._types import Base64String
from ..models import Board, Workspace
from ._base import BaseMixin


class WorkspacesMixin(BaseMixin):
    def get_workspaces(
        self, repo_id: int
    ) -> Union[List[dict], List[Workspace]]:
        """
        Gets all Workspaces containing ``repo_id``.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        :class:`list` of :class:`zenhub.models.Workspace` or :class:`list` of :class:`dict`
            Zenhub list of workspaces. See example dictionary below.

            .. code-block:: python

                [
                    {
                        "name": "Design and UX",
                        "description": None,
                        "id": "5d0a7a9741fd098f6b7f58ac",
                        "repositories": [12345678, 912345]
                    },
                    {
                        "name": "Roadmap",
                        "description": "Feature planning and enhancements",
                        "id": "5d0a7cea41fd098f6b7f58b8",
                        "repositories": [12345678]
                    }
                ]

        Note
        ----
        For more information visit the `ZenHub API Documentation <https://github.com/ZenHubIO/API#get-zenhub-workspaces-for-a-repository>`_.
        """
        self._repo_id = repo_id
        # GET /p2/repositories/:repo_id/workspaces
        url = f"/p2/repositories/{repo_id}/workspaces"
        data = self._get(url)
        if self._output_models:
            return [Workspace.parse_obj(workspace) for workspace in data]
        else:
            return [
                Workspace.parse_obj(workspace).dict(include=workspace.keys())
                for workspace in data
            ]

    def get_repository_board(
        self, workspace_id: Base64String, repo_id: int
    ) -> Union[dict, Board]:
        """
        Get ZenHub Board data for a repository (``repo_id``) within the
        Workspace (``workspace_id``).

        Parameters
        ----------
        workspace_id : Base64String
            Workspace unique string identifier.
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        :class:`zenhub.models.Board` or :class:`dict`
            Zenhub workspace board listing pipelines and issues. See example
            dictionary below.

            .. code-block:: python

                {
                    "pipelines": [
                        {
                            "id": "595d430add03f01d32460080",
                            "name": "New Issues",
                            "issues": [
                                {
                                    "issue_number": 279,
                                    "estimate": {"value": 40},
                                    "position": 0,
                                    "is_epic": true
                                },
                                {
                                    "issue_number": 142,
                                    "is_epic": False
                                }
                            ]
                        },
                        {
                            "id": "595d430add03f01d32460081",
                            "name": "Backlog",
                            "issues": [
                                {
                                    "issue_number": 303,
                                    "estimate": {"value": 40},
                                    "position": 3,
                                    "is_epic": False
                                }
                            ]
                            },
                        {
                            "id": "595d430add03f01d32460082",
                            "name": "To Do",
                            "issues": [
                                {
                                    "issue_number": 380,
                                    "estimate": {"value": 1},
                                    "position": 0,
                                    "is_epic": True
                                },
                                {
                                    "issue_number": 284,
                                    "position": 2,
                                    "is_epic": False
                                },
                                {
                                    "issue_number": 329,
                                    "estimate": {"value": 8},
                                    "position": 7,
                                    "is_epic": False
                                }
                            ]
                        }
                    ]
                }

        Note
        ----
        For more information visit the `ZenHub API Documentation <https://github.com/ZenHubIO/API#get-a-zenhub-board-for-a-repository>`_.
        """
        self._repo_id = repo_id
        # GET /p2/workspaces/:workspace_id/repositories/:repo_id/board
        url = f"/p2/workspaces/{workspace_id}/repositories/{repo_id}/board"
        data = self._get(url)
        model = Board.parse_obj(data)
        return (
            model
            if self._output_models
            else model.dict(include=data.keys(), exclude_none=True)
        )

    def get_oldest_repository_board(self, repo_id: int) -> Union[dict, Board]:
        """
        Get the oldest ZenHub board for a repository.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        :class:`zenhub.models.Board` or :class:`dict`
            Zenhub workspace board listing pipelines and issues. See example
            response below.

            .. code-block:: python

                {
                    "pipelines": [
                        {
                            "id": "595d430add03f01d32460080",
                            "name": "New Issues",
                            "issues": [
                                {
                                    "issue_number": 279,
                                    "estimate": {"value": 40},
                                    "position": 0,
                                    "is_epic": True
                                },
                                {
                                    "issue_number": 142,
                                    "is_epic": False
                                }
                            ]
                        },
                        {
                            "id": "595d430add03f01d32460081",
                            "name": "Backlog",
                            "issues": [
                                {
                                    "issue_number": 303,
                                    "estimate": {"value": 40},
                                    "position": 3,
                                    "is_epic": False
                                }
                            ]
                            },
                        {
                            "id": "595d430add03f01d32460082",
                            "name": "To Do",
                            "issues": [
                                {
                                    "issue_number": 380,
                                    "estimate": {"value": 1},
                                    "position": 0,
                                    "is_epic": True
                                },
                                {
                                    "issue_number": 284,
                                    "position": 2,
                                    "is_epic": False
                                },
                                {
                                    "issue_number": 329,
                                    "estimate": {"value": 8},
                                    "position": 7,
                                    "is_epic": False
                                }
                            ]
                        }
                    ]
                }

        Note
        ----
        For more information visit the `ZenHub API Documentation <https://github.com/ZenHubIO/API#get-the-oldest-zenhub-board-for-a-repository>`_.
        """
        self._repo_id = repo_id
        # GET /p1/repositories/:repo_id/board
        url = f"/p1/repositories/{repo_id}/board"
        data = self._get(url)
        model = Board.parse_obj(data)
        return (
            model
            if self._output_models
            else model.dict(include=data.keys(), exclude_none=True)
        )
