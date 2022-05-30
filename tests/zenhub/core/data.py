"""Test ZenHub issues API."""
import os

# Constants
# ----------------------------------------------------------------------------
TOKEN = os.environ.get("ZENHUB_TEST_TOKEN", "")
RUN_CREATE_TESTS = not bool(os.environ.get("RUN_CREATE_TESTS", ""))
REPO_ID = 262640661
RELEASE_REPORT = "Z2lkOi8vcmFwdG9yL1JlbGVhc2UvNzcyNTE"
WORKSPACE_ID = '628d3cf1efe1100011b89841'
MILESTONE_ID = 1
EPIC_WITHOUT_ISSUES = 13
EPIC_WITH_ISSUES = 14
LIMIT = 100
PIPELINE_NEW_ISSUES = 'Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzI3MTcwNTQ'
PIPELINE_BACKLOG = 'Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzI3MTcwNTc'
