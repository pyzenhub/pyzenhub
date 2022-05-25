"""Custom types."""
from typing import List

from typing_extensions import Literal, NotRequired, TypedDict

URLString = str
Base64String = str
ReportState = Literal["open", "closed"]
IssuePosition = Literal["top", "bottom"]
ISO8601DateString = str


class Workspace(TypedDict):
    name: str
    description: str
    id: Base64String
    repositories: List[int]


class MilestoneDate(TypedDict):
    start_date: ISO8601DateString


class Estimate(TypedDict):
    estimate: int


class PipelineIssue(TypedDict):
    issue_number: int
    estimate: dict  # IssueEstimate
    position: NotRequired[IssuePosition]
    is_epic: NotRequired[bool]


class BoardPipeline(TypedDict):
    id: Base64String
    name: str
    issues: List[PipelineIssue]


class Board(TypedDict):
    pipelines: List[BoardPipeline]
