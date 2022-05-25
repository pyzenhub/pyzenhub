"""ZenHub release reports methods."""
from ..models import Dependencies
from .base import BaseMixin


class DependenciesMixin(BaseMixin):
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
