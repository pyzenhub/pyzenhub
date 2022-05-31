"""ZenHub API."""
from typing import Optional

import requests

from .._types import URLString
from ._dependencies import DependenciesMixin
from ._epics import EpicsMixin
from ._issues import IssuesMixin
from ._milestones import MilestonesMixin
from ._rate import RateMixin
from ._release_report_issues import ReleaseReportIssuesMixin
from ._release_reports import ReleaseReportsMixin
from ._workspaces import WorkspacesMixin

# Constants
DEFAULT_BASE_URL: URLString = "https://api.zenhub.com"


class Zenhub(
    IssuesMixin,
    EpicsMixin,
    WorkspacesMixin,
    MilestonesMixin,
    DependenciesMixin,
    ReleaseReportsMixin,
    ReleaseReportIssuesMixin,
    RateMixin,
):
    """ZenHub API wrapper.

    Parameters
    ----------
    token : str
        ZenHub API token.
    base_url : URLString, optional
        Default is ``'https://api.zenhub.com'``.
    enterprise : int, optional
        Default is ``2``.
    return_models : bool, optional
        Default is ``False``.

    Note
    ----
    For more information visit the `ZenHub API Documentation <https://github.com/ZenHubIO/API>`_.
    """

    _HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "ZenHub Python Client",
    }

    def __init__(
        self,
        token: str,
        base_url: URLString = DEFAULT_BASE_URL,
        enterprise: int = 2,
        return_models: bool = False,
    ):
        """ZenHub API wrapper."""
        self._session = requests.Session()
        self._repo_id: Optional[int] = None

        if base_url == DEFAULT_BASE_URL:
            self._repo_id = 262640661  # Use ZenHub's default repo ID

        if enterprise == 3 and base_url != DEFAULT_BASE_URL:
            if base_url.endswith("/"):
                base_url = base_url + "api"
            else:
                base_url = base_url + "/api"

        self._base_url = base_url
        self._output_models = return_models

        # Setup
        self._session.headers.update(self._HEADERS)
        self._session.headers.update({"X-Authentication-Token": token})
