"""ZenHub workspace methods."""
from typing import List

from ..models import Board, Workspace
from ..types import Base64String
from .base import BaseMixin


class WorkspacesMixin(BaseMixin):
    def get_workspaces(self, repo_id: int) -> List[dict]:
        """
        Gets all Workspaces containing ``repo_id``.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        List of dict.
            Zenhub list of workspaces. See example response below.

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
        https://github.com/ZenHubIO/API#get-zenhub-workspaces-for-a-repository
        """
        # GET /p2/repositories/:repo_id/workspaces
        url = f"/p2/repositories/{repo_id}/workspaces"
        data = self._get(url)
        return [
            Workspace.parse_obj(workspace).dict(include=workspace.keys())
            for workspace in data
        ]

    def get_repository_board(
        self, workspace_id: Base64String, repo_id: int
    ) -> dict:
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
        Dictionary with board information.
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
        https://github.com/ZenHubIO/API#get-a-zenhub-board-for-a-repository
        """
        # GET /p2/workspaces/:workspace_id/repositories/:repo_id/board
        url = f"/p2/workspaces/{workspace_id}/repositories/{repo_id}/board"
        data = self._get(url)
        return Board.parse_obj(data).dict(
            include=data.keys(), exclude_none=True
        )

    def get_oldest_repository_board(self, repo_id: int) -> dict:
        """
        Get the oldest ZenHub board for a repository.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        Dictionary with board information.
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
        https://github.com/ZenHubIO/API#get-the-oldest-zenhub-board-for-a-repository
        """
        # GET /p1/repositories/:repo_id/board
        url = f"/p1/repositories/{repo_id}/board"
        data = self._get(url)
        return Board.parse_obj(data).dict(
            include=data.keys(), exclude_none=True
        )
