# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2022 Gonzalo Peña-Castellanos (@goanpeca)
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""ZenHub API."""

from typing import List, Union
from .core import Zenhub
from .exceptions import APILimitError, InvalidTokenError, NotFoundError, ZenhubError

__version__ = "0.2.2"


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
