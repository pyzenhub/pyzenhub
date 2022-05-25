import requests

from ..types import URLString
from ..utils import parse_response_contents


class BaseMixin:
    _session: requests.Session
    _base_url: URLString

    def _make_url(self, url: URLString) -> URLString:
        """Create full api url."""
        return f"{self._base_url}{url}"

    def _get(self, url: URLString) -> dict:
        """Send GET request with given url."""
        response = self._session.get(url=self._make_url(url))
        return parse_response_contents(response)

    def _post(self, url: URLString, body: dict = {}) -> dict:
        """Send POST request with given url and data."""
        response = self._session.post(url=self._make_url(url), json=body)
        return parse_response_contents(response)

    def _put(self, url: URLString, body: dict) -> dict:
        """Send PUT request with given url and data."""
        response = self._session.put(url=self._make_url(url), json=body)
        return parse_response_contents(response)

    def _delete(self, url: URLString, body: dict = {}) -> dict:
        """Send DELETE request with given url and data."""
        response = self._session.delete(url=self._make_url(url), json=body)
        return parse_response_contents(response)

    def _patch(self, url: URLString, body: dict) -> dict:
        """Send PATCH request with given url and data."""
        response = self._session.patch(url=self._make_url(url), json=body)
        return parse_response_contents(response)
