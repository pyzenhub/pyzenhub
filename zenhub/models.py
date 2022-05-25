# -----------------------------------------------------------------------------
# Copyright (c) 2022 Gonzalo Peña-Castellanos (@goanpeca)
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""ZenHub API pydantic models."""
from typing import List, Optional

from pydantic import BaseModel

from .types import Base64String, ISO8601DateString


class PlusOnes(BaseModel):
    created_at: ISO8601DateString


class Pipeline(BaseModel):
    name: str
    pipeline_id: Base64String
    workspace_id: Base64String


class IssueEstimate(BaseModel):
    value: int


class IssueData(BaseModel):
    estimate: Optional[IssueEstimate]
    is_epic: bool
    plus_ones: List[PlusOnes]
    pipeline: Optional[Pipeline]
    pipelines: Optional[List[Pipeline]]


class Issue(BaseModel):
    repo_id: int
    issue_number: int


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
