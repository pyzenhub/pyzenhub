# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2022 Gonzalo Peña-Castellanos (@goanpeca)
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""ZenHub API."""
from .core import APILimitError, InvalidTokenError, NotFoundError, Zenhub, ZenhubError


__version__ = "0.2.2"


def _to_version_info(version):
    """Convert a version string to a number and string tuple."""
    parts = []
    for part in version.split("."):
        try:
            part = int(part)
        except ValueError:
            pass

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
