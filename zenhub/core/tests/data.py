"""Test ZenHub issues API."""
import os

# Constants
# ----------------------------------------------------------------------------
TOKEN = os.environ.get("ZENHUB_TEST_TOKEN", "")
RUN_CREATE_TESTS = not bool(os.environ.get("RUN_CREATE_TESTS", ""))
REPO_ID = 262640661
RELEASE_REPORT = "Z2lkOi8vcmFwdG9yL1JlbGVhc2UvNzcyNTE"
WORKSPACE_ID = '628d3cf1efe1100011b89841'
