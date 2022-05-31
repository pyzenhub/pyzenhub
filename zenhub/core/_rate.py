"""ZenHub dependencies methods."""
import datetime
from typing import Dict, Optional, Union

from requests.structures import CaseInsensitiveDict

from ..exceptions import ZenhubError
from ..models import RateLimit
from ._base import BaseMixin


class RateMixin(BaseMixin):
    def _headers(self, repo_id: Optional[int] = None) -> CaseInsensitiveDict:
        """Return headers from example request.

        Parameters
        ----------
        repo_id : int, optional
            ID of the repository, not its full name. Default is `None`.

        Returns
        -------
        CaseInsensitiveDict
            Headers from request.
        """
        repo_id = repo_id or self._repo_id
        if repo_id is None:
            raise ZenhubError(
                "Need to make at least one request using the `repo_id` parameter!"
            )
        url = f'/p2/repositories/{repo_id}/workspaces'
        response = self._session.head(url=self._make_url(url))
        return response.headers

    def rate_limit(
        self, repo_id: Optional[int] = None
    ) -> Union[RateLimit, Dict[str, int]]:
        """API rate limit.

        A maximum of 100 requests per minute to the API.

        Parameters
        ----------
        repo_id : int, optional
            ID of the repository, not its full name. Default is ``None``.

        Returns
        -------
        :class:`zenhub.models.RateLimit` or :class:`dict`
            Dictionary with rate limit, available calls and time to reset
            limits in seconds. See example response below.

            .. code-block:: python

                {'used': 3, 'limit': 100, 'reset': 58}

        Note
        ----
        For more information visit the `ZenHub API Documentation <https://github.com/ZenHubIO/API#api-rate-limit>`_.
        """
        headers = self._headers(repo_id)
        limit_used_string = headers.get('X-RateLimit-Used', -1)
        limit_allowed_string = headers.get('X-RateLimit-Limit', -1)
        limit_reset_time_string = headers.get('X-RateLimit-Reset', -1)
        server_date_string = headers.get('Date', -1)
        try:
            limit_used = int(limit_used_string)
        except Exception:
            limit_used = -1

        try:
            limit_allowed = int(limit_allowed_string)
        except Exception:
            limit_allowed = -1

        try:
            limit_reset_time = int(limit_reset_time_string)
        except Exception:
            limit_reset_time = -1

        if limit_reset_time != -1 or server_date_string != -1:
            date_reset = datetime.datetime.fromtimestamp(
                limit_reset_time, tz=datetime.timezone.utc
            )
            date_format = (
                '%a, %d %B %Y %H:%M:%S %Z'  # Mon, 30 May 2022 22:43:37 GMT
            )
            date_machine = datetime.datetime.strptime(
                server_date_string, date_format
            ).replace(tzinfo=datetime.timezone.utc)
            limit_reset = (date_reset - date_machine).seconds
        else:
            limit_reset = -1

        model = RateLimit(
            limit=limit_allowed, used=limit_used, reset=limit_reset
        )
        return model if self._output_models else model.dict()
