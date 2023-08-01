"""ZenHub epics methods."""
from typing import Iterable, Union

from ..models import AddRemoveIssuesEpic, EpicData, Epics, Issue
from ._base import BaseMixin


class EpicsMixin(BaseMixin):
    def get_epics(self, repo_id: int) -> Union[Epics, dict]:
        """
        Get all Epics for a repository.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        :class:`zenhub.models.Epics` or :class:`dict`
            See example dictionary below.

            .. code-block:: python

                {
                  "epic_issues": [
                    {
                      "issue_number": 3953,
                      "repo_id": 1234567,
                      "issue_url":
                        "https://github.com/RepoOwner/RepoName/issues/3953"
                    },
                    {
                      "issue_number": 1342,
                      "repo_id": 1234567,
                      "issue_url":
                        "https://github.com/RepoOwner/RepoName/issues/1342"
                    }
                  ]
                }

        Note
        ----
        - The endpoint returns a list of the repository’s Epics. The issue
          number, repository ID, and GitHub issue URL is provided for each
          Epic.
        - If an issue is only an issue belonging to an Epic (and not a parent
          Epic), it is not considered an Epic and won’t be included in the list.

        For more information visit the `ZenHub API Documentation <https://github.com/ZenHubIO/API#get-epics-for-a-repository>`_.
        """
        self._repo_id = repo_id
        # GET /p1/repositories/:repo_id/epics
        url = f"/p1/repositories/{repo_id}/epics"
        data = self._get(url)
        model = Epics.parse_obj(data)
        return (
            model if self._output_models else model.dict(include=data.keys())
        )

    def get_epic_data(
        self, repo_id: int, epic_id: int
    ) -> Union[EpicData, dict]:
        """
        Get all Epics for a repository.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        epic_id : int
            Github issue number of the epic.

        Returns
        -------
        :class:`zenhub.models.EpicData` or :class:`dict`
            See example dictionary below.

            .. code-block:: python

                {
                    "total_epic_estimates": {"value": 60},
                    "estimate": {"value": 10},
                    "pipeline": {
                        "workspace_id": "5d0a7a9741fd098f6b7f58ac",
                        "name": "Backlog",
                        "pipeline_id": "5d0a7a9741fd098f6b7f58a8"
                    },
                    "pipelines": [
                        {
                            "workspace_id": "5d0a7a9741fd098f6b7f58ac",
                            "name": "Backlog",
                            "pipeline_id": "5d0a7a9741fd098f6b7f58a8"
                        },
                        {
                            "workspace_id": "5d0a7cea41fd098f6b7f58b8",
                            "name": "In Progress",
                            "pipeline_id": "5d0a7cea41fd098f6b7f58b5"
                        }
                    ],
                    "issues": [
                        {
                            "issue_number": 3161,
                            "is_epic": True,
                            "repo_id": 1099029,
                            "estimate": {"value": 40},
                            "pipelines": [
                                {
                                    "workspace_id": "5d0a7a9741fd098f6b7f58ac",
                                    "name": "Backlog",
                                    "pipeline_id": "5d0a7a9741fd098f6b7f58a8"
                                },
                                {
                                    "workspace_id": "5d0a7cea41fd098f6b7f58b8",
                                    "name": "In Progress",
                                    "pipeline_id": "5d0a7cea41fd098f6b7f58b5"
                                }
                            ],
                            "pipeline": {
                                "workspace_id": "5d0a7a9741fd098f6b7f58ac",
                                "name": "Backlog",
                                "pipeline_id": "5d0a7a9741fd098f6b7f58a8"
                            }
                        },
                        {
                            "issue_number": 2,
                            "is_epic": False,
                            "repo_id": 1234567,
                            "estimate": {"value": 10},
                            "pipelines": [
                                {
                                    "workspace_id": "5d0a7a9741fd098f6b7f58ac",
                                    "name": "Backlog",
                                    "pipeline_id": "5d0a7a9741fd098f6b7f58a8"
                                },
                                {
                                    "workspace_id": "5d0a7cea41fd098f6b7f58b8",
                                    "name": "In Progress",
                                    "pipeline_id": "5d0a7cea41fd098f6b7f58b5"
                                }
                            ],
                            "pipeline": {
                                "workspace_id": "5d0a7a9741fd098f6b7f58ac",
                                "name": "Backlog",
                                "pipeline_id": "5d0a7a9741fd098f6b7f58a8"
                            }
                        }
                    ]
                }

        Note
        ----
        For more information visit the `ZenHub API Documentation <https://github.com/ZenHubIO/API#get-epic-data>`_.
        """
        self._repo_id = repo_id
        # GET /p1/repositories/:repo_id/epics/:epic_id
        url = f"/p1/repositories/{repo_id}/epics/{epic_id}"
        data = self._get(url)
        model = EpicData.parse_obj(data)
        return (
            model if self._output_models else model.dict(include=data.keys())
        )

    def convert_epic_to_issue(self, repo_id: int, issue_number: int) -> bool:
        """
        Converts an Epic back to a regular issue.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        issue_number : int
            The number of the issue to be converted

        Returns
        -------
        :class:`bool`
            ``True`` if successful.

        Note
        ----
        For more information visit the `ZenHub API Documentation <https://github.com/ZenHubIO/API#convert-an-epic-to-an-issue>`_.
        """
        self._repo_id = repo_id
        # POST /p1/repositories/:repo_id/epics/:issue_number/convert_to_issue
        url = (
            f"/p1/repositories/{repo_id}/epics/{issue_number}/convert_to_issue"
        )
        data = self._post(url)
        return True if data == {} else False

    def convert_issue_to_epic(
        self, repo_id: int, issue_number: int, issues: Iterable[Issue] = ()
    ) -> bool:
        """
        Converts an issue to an Epic, along with any issues that should be
        part of it.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        issue_number : int
            The number of the issue to be converted
        issues: Iterable[Issue]
            Add issues to epic.

        Returns
        -------
        :class:`bool`
            ``True`` if successful.

        Note
        ----
        For more information visit the `ZenHub API Documentation <https://github.com/ZenHubIO/API#convert-issue-to-epic>`_.
        """
        self._repo_id = repo_id
        # POST /p1/repositories/:repo_id/issues/:issue_number/convert_to_epic
        url = (
            f"/p1/repositories/{repo_id}/issues/{issue_number}/convert_to_epic"
        )
        body = {"issues": issues}
        data = self._post(url, body=body)
        return bool(data)

    def add_or_remove_issues_to_epic(
        self,
        repo_id: int,
        issue_number: int,
        remove_issues: Iterable[Issue] = (),
        add_issues: Iterable[Issue] = (),
    ) -> Union[AddRemoveIssuesEpic, dict]:
        """
        Bulk add or remove issues to an Epic.

        The result returns which issue was added or removed from the Epic.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.
        issue_number : int
            The number of the epic.
        remove_issues: Iterable[Issue]
            Issues to remove from epic.
        add_issues: Iterable[Issue]
            Issues to add to epic.

        Returns
        -------
        :class:`zenhub.models.AddRemoveIssuesEpic` or :class:`dict`
            See example dictionary below.

            .. code-block:: python

                {
                    "removed_issues": [
                        {"repo_id": 3887883, "issue_number": 3}
                    ],
                    "added_issues": [
                        {"repo_id": 3887883, "issue_number": 2},
                        {"repo_id": 3887883, "issue_number": 1}
                    ]
                }

        Note
        ----
        For more information visit the `ZenHub API Documentation <https://github.com/ZenHubIO/API#add-or-remove-issues-to-epic>`_.
        """
        self._repo_id = repo_id
        # POST /p1/repositories/:repo_id/epics/:issue_number/update_issues
        url = f"/p1/repositories/{repo_id}/epics/{issue_number}/update_issues"
        body = {
            "remove_issues": list(remove_issues),
            "add_issues": list(add_issues),
        }
        data = self._post(url, body=body)
        model = AddRemoveIssuesEpic.parse_obj(data)
        return (
            model if self._output_models else model.dict(include=data.keys())
        )