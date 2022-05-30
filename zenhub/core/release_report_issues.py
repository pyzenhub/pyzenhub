"""ZenHub release report issues methods."""

from typing import Iterable, List, Union

from ..models import AddRemoveIssue, Issue
from ..types import Base64String
from .base import BaseMixin


class ReleaseReportIssuesMixin(BaseMixin):
    def get_release_report_issues(
        self, release_id: Base64String
    ) -> Union[List[Issue], List[dict]]:
        """
        Get all the Issues for a Release Report.

        Parameters
        ----------
        release_id : Base64String
            The unique string identifier of the Release Report.

        Returns
        -------
        List of Issue or List of dictionaries
            See example response below.

        .. code-block:: python
            [
                { "repo_id": 103707262, "issue_number": 2 },
                { "repo_id": 103707262, "issue_number": 3 },
            ]

        Note
        ----
        https://github.com/ZenHubIO/API#get-all-the-issues-for-a-release-report
        """
        # GET /p1/reports/release/:release_id/issues
        url = f"/p1/reports/release/{release_id}/issues"
        if self._output_models:
            return [Issue.parse_obj(item) for item in self._get(url)]
        else:
            return [
                Issue.parse_obj(item).dict(include=item.keys())
                for item in self._get(url)
            ]

    def add_or_remove_issues_from_release_report(
        self,
        release_id: Base64String,
        add_issues: Iterable[Issue] = (),
        remove_issues: Iterable[Issue] = (),
    ) -> Union[AddRemoveIssue, dict]:
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
        AddRemoveIssue or dict
            The added or removed issues. See example response below.

        .. code-block:: python
            {
                "added": [{ "repo_id": 103707262, "issue_number": 3 }],
                "removed": [],
            }

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
        data = self._patch(url, body=body)
        model = AddRemoveIssue.parse_obj(data)
        return (
            model if self._output_models else model.dict(include=data.keys())
        )
