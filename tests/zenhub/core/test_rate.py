import pytest

from zenhub.exceptions import ZenhubError

from .data import LIMIT, REPO_ID


def test_rate_limit(zh):
    data = zh.rate_limit()
    assert data['limit'] == LIMIT
    assert 0 <= data['used'] <= LIMIT
    assert 0 <= data['reset'] <= 60


def test_rate_limit_no_repo_id(zh):
    zh._repo_id = None
    data = zh.rate_limit(REPO_ID)
    assert data['limit'] == LIMIT
    assert 0 <= data['used'] <= LIMIT
    assert 0 <= data['reset'] <= 60


def test_rate_limit_no_repo_id_invalid(zh):
    zh._repo_id = None
    with pytest.raises(ZenhubError):
        zh.rate_limit()


def test_rate_limit_exceptions(zh):
    zh._headers = lambda x=None: {
        'X-RateLimit-Used': None,
        'X-RateLimit-Limit': -1,
        'X-RateLimit-Reset': -1,
        'Date': -1,
    }
    data = zh.rate_limit(REPO_ID)
    assert data['used'] == -1

    zh._headers = lambda x=None: {
        'X-RateLimit-Used': -1,
        'X-RateLimit-Limit': None,
        'X-RateLimit-Reset': -1,
        'Date': -1,
    }
    assert data['limit'] == -1

    zh._headers = lambda x=None: {
        'X-RateLimit-Used': -1,
        'X-RateLimit-Limit': -1,
        'X-RateLimit-Reset': None,
        'Date': None,
    }
    assert data['reset'] == -1
