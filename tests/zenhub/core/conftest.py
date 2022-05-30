"""Test ZenHub issues API."""
import time

import pytest
from zenhub import Zenhub

from .data import TOKEN


# Fixtures
# ----------------------------------------------------------------------------
@pytest.fixture
def zh():
    yield Zenhub(TOKEN)
    time.sleep(0.25)
