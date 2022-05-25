"""Test ZenHub issues API."""
import pytest

from zenhub import Zenhub

from .data import TOKEN

# Fixtures
# ----------------------------------------------------------------------------
@pytest.fixture
def zh():
    return Zenhub(TOKEN)
