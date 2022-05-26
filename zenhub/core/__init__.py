"""ZenHub API."""
import requests

from ..types import URLString
from .dependencies import DependenciesMixin
from .epics import EpicsMixin
from .issues import IssuesMixin
from .milestones import MilestonesMixin
from .release_report_issues import ReleaseReportIssuesMixin
from .release_reports import ReleaseReportsMixin
from .workspaces import WorkspacesMixin

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
):
    """Zenhub API wrapper."""

    _HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": "ZenHub Python Client",
    }

    def __init__(
        self,
        token: str,
        base_url: URLString = DEFAULT_BASE_URL,
        enterprise: int = 2,
    ):
        """ZenHub API wrapper."""
        self._session = requests.Session()
        if enterprise == 3 and base_url != DEFAULT_BASE_URL:
            if base_url.endswith("/"):
                base_url = base_url + "api"
            else:
                base_url = base_url + "/api"

        self._base_url = base_url

        # Setup
        self._session.headers.update(self._HEADERS)
        self._session.headers.update({"X-Authentication-Token": token})
