"""ZenHub API pydantic models."""
import datetime
from typing import List, Optional, Union

from pydantic import BaseModel

from .types import (
    Base64String,
    ISO8601DateString,
    IssueEventType,
    IssuePosition,
    Seconds,
    URLString,
)


class IssueEstimate(BaseModel):
    value: int


class PipelineName(BaseModel):
    name: str


class Event(BaseModel):
    user_id: int
    type: IssueEventType
    created_at: datetime.datetime


class EstimateIssueEvent(Event):
    from_estimate: Optional[IssueEstimate]
    to_estimate: Optional[IssueEstimate]


class TransferIssueEvent(Event):
    from_pipeline: Optional[PipelineName]
    to_pipeline: Optional[PipelineName]
    Workspace_id: Optional[Base64String]


class PlusOnes(BaseModel):
    created_at: ISO8601DateString


class Pipeline(BaseModel):
    name: str
    pipeline_id: Base64String
    workspace_id: Base64String


class IssueData(BaseModel):
    estimate: Optional[IssueEstimate]
    repo_id: Optional[int]
    is_epic: bool
    plus_ones: List[PlusOnes]
    pipeline: Optional[Pipeline]
    pipelines: Optional[List[Pipeline]]


class Issue(BaseModel):
    repo_id: int
    issue_number: int


class AddRemoveIssuesEpic(BaseModel):
    added_issues: List[Issue]
    removed_issues: List[Issue]


class AddRemoveIssue(BaseModel):
    added: List[Issue]
    removed: List[Issue]


class ReleaseReport(BaseModel):
    release_id: Base64String
    title: str
    description: str
    start_date: ISO8601DateString
    desired_end_date: ISO8601DateString
    created_at: ISO8601DateString
    closed_at: Optional[ISO8601DateString]
    state: str
    repositories: Optional[List[int]]


class Dependency(BaseModel):
    blocking: Issue
    blocked: Issue


class Dependencies(BaseModel):
    dependencies: List[Dependency]


class MilestoneDate(BaseModel):
    start_date: ISO8601DateString


class Workspace(BaseModel):
    name: str
    description: Optional[str]
    id: Base64String
    repositories: List[int]


class Estimate(BaseModel):
    estimate: int


class PipelineIssue(BaseModel):
    issue_number: int
    estimate: Optional[dict]  # FIXME: IssueEstimate
    position: Union[IssuePosition, int]
    is_epic: bool


class BoardPipeline(BaseModel):
    id: Base64String
    name: str
    issues: List[PipelineIssue]


class Board(BaseModel):
    pipelines: List[BoardPipeline]


class Epic(BaseModel):
    issue_number: int
    repo_id: int
    issue_url: URLString


class Epics(BaseModel):
    epic_issues: List[Epic]


class EpicData(BaseModel):
    total_epic_estimates: IssueEstimate
    estimate: Optional[IssueEstimate]
    pipeline: Pipeline
    pipelines: List[Pipeline]
    issues: List[Issue]


class RateLimit(BaseModel):
    limit: int
    used: int
    reset: Seconds
