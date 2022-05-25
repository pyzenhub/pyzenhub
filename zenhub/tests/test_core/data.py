"""Test ZenHub issues API."""
import datetime
import os
import random

import pytest

from zenhub import Zenhub, ZenhubError

# Constants
# ----------------------------------------------------------------------------
TOKEN = os.environ.get("ZENHUB_TEST_TOKEN", "")
RUN_CREATE_TESTS = not bool(os.environ.get("RUN_CREATE_TESTS", ""))
REPO_ID = 262640661
RELEASE_REPORT = "Z2lkOi8vcmFwdG9yL1JlbGVhc2UvNzcyNTE"
