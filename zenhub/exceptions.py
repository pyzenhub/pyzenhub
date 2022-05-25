# -----------------------------------------------------------------------------
# Copyright (c) 2022 Gonzalo Peña-Castellanos (@goanpeca)
#
# Licensed under the terms of the MIT License
# (See LICENSE.txt for details)
# -----------------------------------------------------------------------------
"""ZenHub API Custom Exeptions."""


class ZenhubError(Exception):
    pass


class InvalidTokenError(ZenhubError):
    pass


class APILimitError(ZenhubError):
    pass


class NotFoundError(ZenhubError):
    pass
