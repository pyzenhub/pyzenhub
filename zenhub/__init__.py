# -----------------------------------------------------------------------------
# Copyright (c) 2022 Gonzalo Peña-Castellanos (@goanpeca)
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""ZenHub API."""

from typing import List, Union

from .core import Zenhub
from .exceptions import (
    APILimitError,
    InvalidTokenError,
    NotFoundError,
    ZenhubError,
)

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"


def _to_version_info(version: str) -> tuple:
    """Convert a version string to a number and string tuple."""
    parts: List[Union[str, int]] = []
    for part in version.split("."):
        if part.isnumeric():
            part = int(part)  # type: ignore

        parts.append(part)

    return tuple(parts)


VERSION_INFO = _to_version_info(__version__)

__all__ = [
    "APILimitError",
    "InvalidTokenError",
    "NotFoundError",
    "Zenhub",
    "ZenhubError",
]
