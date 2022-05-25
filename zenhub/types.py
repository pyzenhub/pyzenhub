"""Custom types."""
from typing_extensions import Literal

URLString = str
Base64String = str
ReportState = Literal["open", "closed"]
IssuePosition = Literal["top", "bottom"]
ISO8601DateString = str
