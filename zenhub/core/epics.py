"""ZenHub epics methods."""
from typing import Iterable

from ..models import Issue
from .base import BaseMixin


class EpicsMixin(BaseMixin):
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
