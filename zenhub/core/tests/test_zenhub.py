"""Test ZenHub issues API."""
import pytest

from zenhub import Zenhub
from zenhub.core import DEFAULT_BASE_URL

from .data import TOKEN


def test_cloud_api():
    zh = Zenhub(TOKEN)
    assert zh._base_url == DEFAULT_BASE_URL


@pytest.mark.parametrize(
    'enterprise,url,result',
    [
        (2, 'https://enterprise.com', 'https://enterprise.com'),
        (2, 'https://enterprise.com/', 'https://enterprise.com/'),
        (3, 'https://enterprise.com', 'https://enterprise.com/api'),
        (3, 'https://enterprise.com/', 'https://enterprise.com/api'),
    ],
)
def test_enterprise_api(enterprise, url, result):
    zh = Zenhub(TOKEN, base_url=url, enterprise=enterprise)
    assert zh._base_url == result


@pytest.mark.parametrize(
    'enterprise',
    [
        (2,),
        (3,),
    ],
)
def test_enterprise_api_change(enterprise):
    zh = Zenhub(TOKEN, enterprise=enterprise)
    assert zh._base_url == DEFAULT_BASE_URL
