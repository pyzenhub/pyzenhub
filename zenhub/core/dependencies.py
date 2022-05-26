"""ZenHub dependencies methods."""
from ..models import Dependencies, Dependency
from .base import BaseMixin


class DependenciesMixin(BaseMixin):
    def get_dependencies(self, repo_id: int) -> dict:
        """
        Get Dependencies for a Repository.

        Parameters
        ----------
        repo_id : int
            ID of the repository, not its full name.

        Returns
        -------
        dict
            Dictionary of dependencies. See example below.

        .. code-block:: python
            {
                "dependencies": [
                    {
                        "blocking": {
                            "issue_number": 3953,
                            "repo_id": 1234567
                        },
                        "blocked": {
                            "issue_number": 1342,
                            "repo_id": 1234567
                        }
                    },
                    {
                        "blocking": {
                            "issue_number": 5,
                            "repo_id": 987
                        },
                        "blocked": {
                            "issue_number": 1342,
                            "repo_id": 1234567
                        }
                    }
                ]
            }

        Note
        ----
        https://github.com/ZenHubIO/API#get-dependencies-for-a-repository
        """
        # GET /p1/repositories/:repo_id/dependencies
        url = f"/p1/repositories/{repo_id}/dependencies"
        data = self._get(url)
        return Dependencies.parse_obj(data).dict(include=data.keys())

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
        dict
            Example response.

        .. code-block:: python
            {
                "blocking": {
                    "repo_id": 92563409,
                    "issue_number": 14
                },
                "blocked": {
                    "repo_id": 92563409,
                    "issue_number": 13
                }
            }

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
        data = self._post(url, body)
        return Dependency.parse_obj(data).dict(include=data.keys())

    def remove_dependency(
        self,
        blocking_repo_id: int,
        blocking_issue_number: int,
        blocked_repo_id: int,
        blocked_issue_number: int,
    ) -> bool:
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
        bool
            ``True`` if the dependency was removed.

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
        return True if self._delete(url, body) == {} else False
